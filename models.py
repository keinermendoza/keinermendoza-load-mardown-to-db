from sqlalchemy import Table, Column, DateTime, Boolean, BigInteger, String, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

Base = declarative_base()

### Secondary tables
tags_posts = Table(
    "tags_posts",
    Base.metadata,
    Column("post_id", BigInteger, ForeignKey("posts.id"), primary_key=True),
    Column("tag_id", BigInteger, ForeignKey("tags.id"), primary_key=True),
)

tags_projects = Table(
    "tags_projects",
    Base.metadata,
    Column("project_id", BigInteger, ForeignKey("projects.id"), primary_key=True),
    Column("tag_id", BigInteger, ForeignKey("tags.id"), primary_key=True),
)

# entities
class Post(Base):
    __tablename__ = "posts"

    id = Column(BigInteger, primary_key=True)
    title = Column(String(200), nullable=False)
    slug = Column(String(200), unique=True, nullable=False)
    image = Column(String(200), nullable=True)
    content = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    tags = relationship(
        "Tag",
        secondary=tags_posts,
        back_populates="posts"
    )

class Project(Base):
    __tablename__ = "projects"

    id = Column(BigInteger, primary_key=True)
    title = Column(String(200), nullable=False)
    slug = Column(String(200), unique=True, nullable=False)
    image = Column(String(200), nullable=True)
    content = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    tags = relationship(
        "Tag",
        secondary=tags_projects,
        back_populates="projects"
    )

class Tag(Base):
    __tablename__ = "tags"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    slug = Column(String(255), unique=True, nullable=False)
    image = Column(String(255), nullable=True)
    is_public = Column(Boolean, default=False)

    posts = relationship(
        "Post",
        secondary=tags_posts,
        back_populates="tags"
    )

    projects = relationship(
        "Project",
        secondary=tags_projects,
        back_populates="tags"
    )
