import time
from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from uuid import UUID

import pydantic
import pytz
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema.agent import AgentAction, AgentFinish
from langchain.schema.messages import BaseMessage
from langchain.schema.output import LLMResult

from llm_monitor.schema.transaction import TransactionRecord, TransactionRecordType
from llm_monitor.utils.aggregator import (
    add_record_to_batch,
    initialize_api_client,
    start_aggregator_job,
)

# The id field of the serialized response contains a list of identifiers
# that represent the structure of that call like
# ['langchain', 'chat_models', 'openai', 'ChatOpenAI'].
# We want to store the specific constructor being ChatOpenAI
IDX_OF_CONSTRUCTOR = 3

is_pydantic_v1 = int(pydantic.__version__.split(".")[0]) == 1


class MonitorHandler(BaseCallbackHandler):
    timers: Dict[str, Dict[str, float]] = {}
    records: Dict[str, TransactionRecord] = {}

    def __init__(self, project_name: str, *args: Any, **kwargs: Any) -> None:
        """LangChain callbackbander for LLM Monitoring

        Parameters
        ----------
        project_name : str
            Name of the project to log to
        """
        initialize_api_client(project_name=project_name)
        start_aggregator_job()
        super().__init__(*args, **kwargs)

    def _start_new_node(
        self, run_id: UUID, parent_run_id: Optional[UUID]
    ) -> tuple[str, Optional[str]]:
        node_id = str(run_id)
        chain_id = str(parent_run_id) if parent_run_id else None
        if chain_id and self.records.get(chain_id):
            self.records[chain_id].has_children = True

        self.timers[node_id] = {}
        self.timers[node_id]["start"] = time.perf_counter()

        return node_id, chain_id

    def _finish_node(self, run_id: UUID) -> tuple[str, int]:
        node_id = str(run_id)

        self.timers[node_id]["stop"] = time.perf_counter()
        latency_ms = round(
            (self.timers[node_id]["stop"] - self.timers[node_id]["start"]) * 1000
        )
        del self.timers[node_id]

        return node_id, latency_ms

    def on_llm_start(
        self,
        serialized: Dict[str, Any],
        prompts: List[str],
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> Any:
        """Run when LLM starts running."""
        node_id, chain_id = self._start_new_node(run_id, parent_run_id)
        input_text = prompts[0]
        tags = kwargs.get("tags")
        metadata = kwargs.get("metadata")
        constructor = serialized["id"][IDX_OF_CONSTRUCTOR]
        model = kwargs["invocation_params"]["model_name"]
        temperature = kwargs["invocation_params"].get("temperature")
        self.records[node_id] = TransactionRecord(
            node_id=node_id,
            chain_id=chain_id,
            input_text=input_text,
            model=model,
            created_at=datetime.now(tz=pytz.utc).isoformat(),
            temperature=temperature,
            tags=tags,
            user_metadata=metadata,
            constructor=constructor,
            node_type=TransactionRecordType.llm.value,
        )

    def on_chat_model_start(
        self,
        serialized: Dict[str, Any],
        messages: List[List[BaseMessage]],
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> Any:
        """Run when Chat Model starts running."""
        node_id, chain_id = self._start_new_node(run_id, parent_run_id)
        input_text = messages[0][0].content
        tags = kwargs.get("tags")
        metadata = kwargs.get("metadata")
        constructor = serialized["id"][IDX_OF_CONSTRUCTOR]
        model = kwargs["invocation_params"]["model"]
        temperature = kwargs["invocation_params"].get("temperature")
        self.records[node_id] = TransactionRecord(
            node_id=node_id,
            chain_id=chain_id,
            input_text=input_text,
            model=model,
            created_at=datetime.now(tz=pytz.utc).isoformat(),
            temperature=temperature,
            tags=tags,
            user_metadata=metadata,
            constructor=constructor,
            node_type=TransactionRecordType.llm.value,
        )

    def on_llm_end(self, response: LLMResult, run_id: UUID, **kwargs: Any) -> Any:
        """Run when LLM ends running."""
        node_id, latency_ms = self._finish_node(run_id)

        generation = response.generations[0][0]
        if hasattr(generation, "message"):
            output_text = generation.message.content
        else:
            output_text = generation.text
        if response.llm_output:
            usage = response.llm_output.get("token_usage", {})
            num_input_tokens = usage.get("prompt_tokens", 0)
            num_output_tokens = usage.get("completion_tokens", 0)
            num_total_tokens = usage.get("total_tokens", 0)

        if generation.generation_info:
            finish_reason = generation.generation_info.get("finish_reason", "")

        if is_pydantic_v1:
            model_dict = self.records[node_id].dict()
        else:
            model_dict = self.records[node_id].model_dump()
        model_dict.update(
            output_text=output_text,
            num_input_tokens=num_input_tokens,
            num_output_tokens=num_output_tokens,
            num_total_tokens=num_total_tokens,
            finish_reason=finish_reason,
            latency_ms=latency_ms,
            status_code=200,
        )

        add_record_to_batch(TransactionRecord(**model_dict))
        del self.records[node_id]

    def on_llm_error(self, error: BaseException, run_id: UUID, **kwargs: Any) -> Any:
        """Run when LLM errors."""
        node_id, latency_ms = self._finish_node(run_id)

        if is_pydantic_v1:
            model_dict = self.records[node_id].dict()
        else:
            model_dict = self.records[node_id].model_dump()
        model_dict.update(
            output_text=f"ERROR: {error}",
            num_input_tokens=0,
            num_output_tokens=0,
            num_total_tokens=0,
            latency_ms=latency_ms,
            status_code=getattr(error, "http_status", 500),
        )

        add_record_to_batch(TransactionRecord(**model_dict))
        del self.records[node_id]

    def on_chain_start(
        self,
        serialized: Dict[str, Any],
        inputs: Dict[str, Any],
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> Any:
        """Run when chain starts running."""
        node_id, chain_id = self._start_new_node(run_id, parent_run_id)
        if serialized.get("kwargs", {}).get("prompt"):
            inputs = serialized["kwargs"]["prompt"]["kwargs"]
        tags = kwargs.get("tags")
        metadata = kwargs.get("metadata")
        constructor = serialized["id"][IDX_OF_CONSTRUCTOR]

        self.records[node_id] = TransactionRecord(
            node_id=node_id,
            chain_id=chain_id,
            input_text=str(inputs),
            created_at=datetime.now(tz=pytz.utc).isoformat(),
            tags=tags,
            user_metadata=metadata,
            node_type=TransactionRecordType.chain.value,
            constructor=constructor,
            children=[],
        )

    def on_chain_end(
        self,
        outputs: Union[str, Dict[str, Any]],
        run_id: UUID,
        **kwargs: Any,
    ) -> Any:
        """Run when chain ends running."""
        node_id, latency_ms = self._finish_node(run_id)

        if is_pydantic_v1:
            model_dict = self.records[node_id].dict()
        else:
            model_dict = self.records[node_id].model_dump()
        model_dict.update(
            output_text=str(outputs),
            finish_reason="chain_end",
            latency_ms=latency_ms,
            status_code=200,
        )

        add_record_to_batch(TransactionRecord(**model_dict))
        del self.records[node_id]

    def on_chain_error(self, error: BaseException, run_id: UUID, **kwargs: Any) -> Any:
        """Run when chain errors."""
        node_id, latency_ms = self._finish_node(run_id)

        if is_pydantic_v1:
            model_dict = self.records[node_id].dict()
        else:
            model_dict = self.records[node_id].model_dump()
        model_dict.update(
            output_text=f"ERROR: {error}",
            latency_ms=latency_ms,
            status_code=getattr(error, "http_status", 500),
        )

        add_record_to_batch(TransactionRecord(**model_dict))
        del self.records[node_id]

    def on_agent_action(self, action: AgentAction, **kwargs: Any) -> Any:
        """Run on agent action."""
        pass

    def on_agent_finish(self, finish: AgentFinish, **kwargs: Any) -> Any:
        """Run on agent end."""
        pass

    def on_tool_start(
        self, serialized: Dict[str, Any], input_str: str, **kwargs: Any
    ) -> Any:
        """Run when tool starts running."""
        pass

    def on_tool_end(self, output: str, **kwargs: Any) -> Any:
        """Run when tool ends running."""
        pass

    def on_tool_error(self, error: BaseException, **kwargs: Any) -> Any:
        """Run when tool errors."""
        pass

    # Streaming support
    def on_llm_new_token(self, token: str, **kwargs: Any) -> Any:
        """Run on new LLM token. Only available when streaming is enabled."""
        pass
