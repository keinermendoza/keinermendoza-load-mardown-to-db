from dataclasses import dataclass, field
from typing import Any, Dict
import frontmatter
import markdown

@dataclass
class MarkdownDocument:
    metadata: Dict[str, Any] = field(default_factory=dict)
    content_md: str = ""
    content_html: str = ""

    @classmethod
    def from_file(cls, filepath: str):
        post = frontmatter.load(filepath)
        html = markdown.markdown(post.content)

        return cls(
            metadata=post.metadata,
            content_md=post.content,
            content_html=html
        )

    def get(self, key: str, default=None):
        """Acceder fácilmente ao frontmatter"""
        return self.metadata.get(key, default)

    def __repr__(self):
        return f"<MarkdownDocument title={self.get('title')}>"