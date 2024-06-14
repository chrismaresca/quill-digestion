class PipelineException(Exception):
    """Base exception for all step-related errors."""
    pass

class StoreException(PipelineException):
    """Exception raised for errors in the store creation step."""
    pass

class MetadataCreationException(PipelineException):
    """Exception raised for errors in the metadata creation step."""
    pass

class FileServiceException(PipelineException):
    """Exception raised for errors in the file service step."""
    pass

class FileLoadingException(PipelineException):
    """Exception raised for errors in the file loading step."""
    pass

class NodeParsingException(PipelineException):
    """Exception raised for errors in the node parsing step."""
    pass

class NodeIngestionException(PipelineException):
    """Exception raised for errors in the node processing step."""
    pass

class StoreAdditionException(PipelineException):
    """Exception raised for errors in the store addition step."""
    pass

class PipelineStepException(PipelineException):
    """Exception raised for errors in the store addition step."""
    pass

