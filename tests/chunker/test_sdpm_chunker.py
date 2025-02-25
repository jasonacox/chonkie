import pytest
from sentence_transformers import SentenceTransformer

from chonkie.chunker.sdpm import SDPMChunker
from chonkie.chunker.semantic import SemanticChunk

@pytest.fixture
def sample_text():
    text = """The process of text chunking in RAG applications represents a delicate balance between competing requirements. On one side, we have the need for semantic coherence – ensuring that each chunk maintains meaningful context that can be understood and processed independently. On the other, we must optimize for information density, ensuring that each chunk carries sufficient signal without excessive noise that might impede retrieval accuracy. In this post, we explore the challenges of text chunking in RAG applications and propose a novel approach that leverages recent advances in transformer-based language models to achieve a more effective balance between these competing requirements."""
    return text


@pytest.fixture
def embedding_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


def test_spdm_chunker_initialization(embedding_model):
    """Test that the SPDMChunker can be initialized with required parameters."""
    chunker = SDPMChunker(
        embedding_model=embedding_model,
        max_chunk_size=512,
        similarity_threshold=0.5,
        skip_window=2,
    )

    assert chunker is not None
    assert chunker.max_chunk_size == 512
    assert chunker.similarity_threshold == 0.5
    assert chunker.initial_sentences == 1
    assert chunker.skip_window == 2


def test_spdm_chunker_chunking(embedding_model, sample_text):
    """Test that the SPDMChunker can chunk a sample text."""
    chunker = SDPMChunker(
        embedding_model=embedding_model,
        max_chunk_size=512,
        similarity_threshold=0.5,
    )
    chunks = chunker.chunk(sample_text)

    assert len(chunks) > 0
    assert isinstance(chunks[0], SemanticChunk)
    assert all([chunk.token_count <= 512 for chunk in chunks])
    assert all([chunk.token_count > 0 for chunk in chunks])
    assert all([chunk.text is not None for chunk in chunks])
    assert all([chunk.start_index is not None for chunk in chunks])
    assert all([chunk.end_index is not None for chunk in chunks])
    assert all([chunk.sentences is not None for chunk in chunks])


def test_spdm_chunker_empty_text(embedding_model):
    """Test that the SPDMChunker can handle empty text input."""
    chunker = SDPMChunker(
        embedding_model=embedding_model,
        max_chunk_size=512,
        similarity_threshold=0.5,
    )
    chunks = chunker.chunk("")

    assert len(chunks) == 0


def test_spdm_chunker_single_sentence(embedding_model):
    """Test that the SPDMChunker can handle text with a single sentence."""
    chunker = SDPMChunker(
        embedding_model=embedding_model,
        max_chunk_size=512,
        similarity_threshold=0.5,
    )
    chunks = chunker.chunk("This is a single sentence.")

    assert len(chunks) == 1
    assert chunks[0].text == "This is a single sentence."
    assert len(chunks[0].sentences) == 1


def test_spdm_chunker_repr(embedding_model):
    """Test that the SPDMChunker has a string representation."""
    chunker = SDPMChunker(
        embedding_model=embedding_model,
        max_chunk_size=512,
        similarity_threshold=0.5,
        skip_window=2,
    )

    expected = (
        "SPDMChunker(max_chunk_size=512, similarity_threshold=0.5, "
        "initial_sentences=1, skip_window=2)"
    )
    assert repr(chunker) == expected


if __name__ == "__main__":
    pytest.main()
