from app.pipelines import VectorPipeline, GraphPipeline


def initialize_strategies(vector_strategies, graph_strategies):
    """
    Initialize all the pipeline strategies defined throughout the application.
    """
    for strategy in vector_strategies.values():
        VectorPipeline.create_pipeline(**strategy)

    for strategy in graph_strategies.values():
        VectorPipeline.create_pipeline(**strategy)
