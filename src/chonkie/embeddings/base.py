from typing import List, Union, TYPE_CHECKING
from abc import ABC, abstractmethod

# import importlib

# if importlib.util.find_spec("numpy") is not None:
#     import numpy as np
# else:
#     np = None

# for type checking
if TYPE_CHECKING:
    import numpy as np

class BaseEmbeddings(ABC):
    """Abstract base class for all embeddings implementations.
    
    All embeddings implementations should inherit from this class and implement
    the embed() and similarity() methods according to their specific embedding strategy.
    """

    def __init__(self):
        """Initialize the BaseEmbeddings class.
        
        This class should be inherited by all embeddings classes and implement the
        abstract methods for embedding text and computing similarity between embeddings.

        It doesn't impose any specific requirements on the embedding model, because
        it can be used for embeddings providers that work via REST APIs or other means.

        Raises:
            NotImplementedError: If any of the abstract methods are not implemented
        """
        pass

    @abstractmethod
    def embed(self, text: str) -> 'np.ndarray':
        """Embed a text string into a vector representation.
        
        This method should be implemented for all embeddings models.

        Args:
            text (str): Text string to embed
        
        Returns:
            np.ndarray: Embedding vector for the text string
        """
        raise NotImplementedError
    
    @abstractmethod
    def embed_batch(self, texts: List[str]) -> List['np.ndarray']:
        """Embed a list of text strings into vector representations.
        
        This method should be implemented for embeddings models that support batch processing.

        By default, it calls the embed() method for each text in the list.

        Args:
            texts (List[str]): List of text strings to embed
        
        Returns:
            List[np.ndarray]: List of embedding vectors for each text in the list
        """
        return [self.embed(text) for text in texts]
    
    @abstractmethod
    def count_tokens(self, text: str) -> int:
        """Count the number of tokens in a text string.
        
        This method should be implemented for embeddings models that require tokenization
        before embedding.

        Args:
            text (str): Text string to count tokens for
        
        Returns:
            int: Number of tokens in the text string
        """
        raise NotImplementedError

    @abstractmethod
    def count_tokens_batch(self, texts: List[str]) -> List[int]:
        """Count the number of tokens in a list of text strings.
    
        Args:
            texts (List[str]): List of text strings to count tokens for
        
        Returns:
            List[int]: List of token counts for each text in the list
        """
        return [self.count_tokens(text) for text in texts]

    @abstractmethod
    def similarity(self, u: 'np.ndarray', v: 'np.ndarray') -> float:
        """Compute the similarity between two embeddings.
        
        Most embeddings models will use cosine similarity for this purpose. However,
        other similarity metrics can be implemented as well. Some embeddings models
        may support a similarity() method that computes the similarity between two
        embeddings via dot product or other means.

        Args:
            u (np.ndarray): First embedding vector
            v (np.ndarray): Second embedding vector
        
        Returns:
            float: Similarity score between the two embeddings
        """
        raise NotImplementedError
    
    @property
    @abstractmethod
    def dimension(self) -> int:
        """Return the dimension of the embedding vectors.
        
        This property should be implemented for embeddings models that have a fixed
        dimension for their embedding vectors.

        Returns:
            int: Dimension of the embedding vectors
        """
        raise NotImplementedError

    @classmethod
    def is_available(cls) -> bool:
        """
        Check if this embeddings implementation is available (dependencies installed).
        Override this method to add custom dependency checks.

        Returns:
            bool: True if the embeddings implementation is available, False otherwise
        """
        return True

    def __repr__(self):
        return self.__class__.__name__ + "()"

    def __call__(self, text: Union[str, List[str]]) -> Union['np.ndarray', List['np.ndarray']]:
        """Embed a text string into a vector representation.
        
        This method allows the embeddings object to be called directly with a text string
        or a list of text strings. It will call the embed() or embed_batch() method
        depending on the input type.

        Args:
            text (Union[str, List[str]]): Input text string or list of text strings

        Returns:
            Union[np.ndarray, List[np.ndarray]]: Single or list of embedding vectors
        """
        if isinstance(text, str):
            return self.embed(text)
        elif isinstance(text, list):
            return self.embed_batch(text)
        else:
            raise ValueError("Input must be a string or list of strings")