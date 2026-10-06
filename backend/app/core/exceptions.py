"""Custom exception classes for MITRA application."""


class MITRAError(Exception):
    """Base exception for MITRA application errors."""
    pass


class DatabaseError(MITRAError):
    """Exception raised for database-related errors."""
    pass


class KnowledgeNotFoundError(MITRAError):
    """Exception raised when requested knowledge is not found."""
    pass


class InvalidQueryError(MITRAError):
    """Exception raised for invalid user queries."""
    pass


class NLPProcessingError(MITRAError):
    """Exception raised during NLP processing."""
    pass


class ConfigurationError(MITRAError):
    """Exception raised for configuration-related errors."""
    pass
