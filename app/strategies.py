from app.common.llama import *
from app.clients import OpenAIClient, PineconeClient


vector_strategies = {
    "strategy_1": {
        "strategy_name": "strategy_1",
        "ai_client": OpenAIClient(model_name='gpt-3.5-turbo'),
        "file_parser": LlamaParse(),
        "node_parser": NodeParser(),
        "transformations": [TransformComponent()],
    },
    "strategy_2": {
        "strategy_name": "strategy_2",
        "ai_client": OpenAIClient(model_name='gpt-4'),
        "file_parser": BaseReader(),
        "node_parser": NodeParser(),
        "transformations": [TransformComponent()],
    }
}

graph_strategies = {
    "strategy_3": {
        "strategy_name": "strategy_3",
        "ai_client": OpenAIClient(model_name='gpt-3.5-turbo'),
        "file_parser": BaseReader(),
        "node_parser": NodeParser(),
        "transformations": [TransformComponent()],
    },
    "strategy_4": {
        "strategy_name": "strategy_4",
        "ai_client": OpenAIClient(model_name='gpt-4-turbo'),
        "file_parser": BaseReader(),
        "node_parser": NodeParser(),
        "transformations": [TransformComponent()],
    }
}
