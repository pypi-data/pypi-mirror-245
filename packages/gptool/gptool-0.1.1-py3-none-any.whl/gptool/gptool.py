import json
from typing import Any, Dict, Optional, Tuple, Type

from gptool.config import LogLevel, get_config, get_function_map, set_config
from gptool.services.openai_service import OpenAIService
from gptool.types.abstract_vectordb import AbstractVectorDB
from gptool.utils.inspection_utilities import get_input_parameter_type
from gptool.utils.openai_utilities import get_latest_user_message


class Gptool:
    def __init__(
        self,
        *,
        openai_key: str,
        openai_url: str,
        functions_directory: Optional[str] = None,
        vectordb: Optional[Type[AbstractVectorDB]] = None,
        log_level: Optional[LogLevel] = None,
    ):
        if openai_key is None:
            raise Exception("No OpenAI key provided.")

        if openai_url is None:
            openai_url = "https://api.openai.com/v1"

        config_args = {"openai_key": openai_key, "openai_url": openai_url}

        if functions_directory is not None:
            config_args["functions_directory"] = functions_directory
        if vectordb is not None:
            config_args["vectordb"] = vectordb
        if log_level is not None:
            config_args["log_level"] = LogLevel(log_level)

        set_config(**config_args)
        self.config = get_config()

        self.openai = OpenAIService()
        self.vectordb = self.config.vectordb()

    def index(self):
        self.vectordb.index()

    def chat(self, *args, **kwargs) -> Dict[str, Any]:
        merged = {i: v for i, v in enumerate(args)}
        merged.update(kwargs)

        top_n = merged.pop("top_n") if "top_n" in merged else None

        if merged.get("model") is None:
            raise Exception("No model provided.")

        if merged.get("messages") is None:
            raise Exception("No messages provided.")

        if top_n is None:
            raise Exception("No top_n provided.")

        latest_user_message = get_latest_user_message(merged.get("messages"))
        if latest_user_message is None:
            raise Exception("No user message found.")

        top_functions = self.get_top_n_functions(
            query=latest_user_message["content"], top_n=top_n
        )

        openai_result = self.call_openai(merged, top_functions)
        if not openai_result.tool_calls:
            return openai_result.model_dump_json(indent=2, exclude_unset=True)

        messages = merged.get("messages")
        for tool_call in openai_result.tool_calls:
            tool_call_id = tool_call.id
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)

            function_response = self.run_function(
                name=function_name, args=function_args
            )

            if "error" not in function_response:
                messages.append(openai_result)
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call_id,
                        "content": json.dumps(function_response),
                    }
                )

        merged.update({"messages": messages})
        # second call
        response = self.call_openai_no_function(merged)
        return response.model_dump_json(indent=2, exclude_unset=True)

    def get_top_n_functions(self, *, query: str, top_n: int):
        return self.vectordb.search_impl(query=query, top_n=top_n)

    def call_openai(
        self, openai_args: Dict[str, Any], top_functions: list[Dict[str, Any]]
    ) -> Tuple[str, Dict[str, Any]]:
        tools = []
        for top_function in top_functions:
            tools.append({"type": "function", "function": top_function})
        openai_result = self.openai.chat(**openai_args, tools=tools)

        return openai_result

    def call_openai_no_function(
        self, openai_args: Dict[str, Any]
    ) -> Tuple[str, Dict[str, Any]]:
        openai_result = self.openai.chat(**openai_args)

        return openai_result

    @staticmethod
    def run_function(*, name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        try:
            function_map = get_function_map()
            func = function_map[name]
            function_input_type = get_input_parameter_type(func.function)
            func_args = function_input_type(**args)
            func_result = func(func_args)
            return func_result.dict()
        except Exception as e:
            return dict(error=str(e))
