from typing import Any

from models.tool_parameter import ToolParameter
from retrieval.semantic_retriever import SemanticRetriever
from tools.tool import Tool


class RetrieverTool(Tool):

    def __init__(
        self,
        semantic_retriever: SemanticRetriever
    ):
        super().__init__(
            name="retriever",
            description="Searches the enterprise knowledge base.",
            input_schema=[
                ToolParameter(
                    name="query",
                    description="The search query.",
                    type=str,
                    required=True
                )
            ]
        )

        self.semantic_retriever = semantic_retriever

    def execute(
        self,
        arguments: dict[str, Any]
    ):

        query = arguments["query"]

        return self.semantic_retriever.search(query)
