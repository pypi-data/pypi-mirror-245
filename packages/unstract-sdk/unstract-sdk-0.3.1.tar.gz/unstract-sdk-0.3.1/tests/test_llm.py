import unittest
from typing import Any

from llama_index import ServiceContext, set_global_service_context
from unstract.sdk.tool.base import UnstractAbstractTool

from sdks.unstract_sdk.llm import UnstractToolLLM


class UnstractToolLLMTest(unittest.TestCase):
    class MockTool(UnstractAbstractTool):
        def run(
            self,
            params: dict[str, Any] = {},
            settings: dict[str, Any] = {},
            workflow_id: str = "",
        ) -> None:
            # self.stream_log("Mock tool running")
            pass

    @classmethod
    def setUpClass(cls):
        cls.tool = cls.MockTool()

    def test_azure_openai(self):
        tool_llm = UnstractToolLLM(tool=self.tool, llm_id="Azure OpenAI")
        llm = tool_llm.get_llm()
        self.assertIsNotNone(llm)
        cb = tool_llm.get_callback_manager()
        service_context = ServiceContext.from_defaults(llm=llm, callback_manager=cb)
        set_global_service_context(service_context)
        response = llm.complete(
            "The capital of Tamilnadu is ",
            max_tokens=50,
            temperature=0.0,
            stop=[".", "\n"],
        )
        self.assertEqual(response.text, "Chennai")
        print(response)
        print(tool_llm.get_usage_counts())
        tool_llm.reset_usage_counts()
        response = llm.complete(
            "The capital of Karnataka is ",
            max_tokens=50,
            temperature=0.0,
            stop=[".", "\n"],
        )
        print(tool_llm.get_usage_counts())


if __name__ == "__main__":
    unittest.main()
