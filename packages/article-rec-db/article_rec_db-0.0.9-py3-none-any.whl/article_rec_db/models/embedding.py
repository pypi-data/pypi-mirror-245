from uuid import UUID

from pgvector.sqlalchemy import Vector  # type: ignore
from sqlmodel import Field, Relationship

from .article import Article
from .execution import Execution
from .helpers import AutoUUIDPrimaryKey, CreationTracked

# The maximum number of dimensions that the vector can have. Vectors with fewer dimensions will be padded with zeros.
MAX_EMBEDDING_DIMENSIONS = 384


class Embedding(AutoUUIDPrimaryKey, CreationTracked, table=True):
    article_id: UUID = Field(foreign_key="article.page_id")
    execution_id: UUID = Field(foreign_key="execution.id")
    vector: list[float] = Field(sa_type=Vector(MAX_EMBEDDING_DIMENSIONS))

    # An embedding always corresonds to an article
    article: Article = Relationship(back_populates="embeddings")

    # An embedding always corresponds to an execution
    execution: Execution = Relationship(back_populates="embeddings")
