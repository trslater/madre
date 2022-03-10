from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from typing import Union
from urllib.parse import urlsplit

import markdown


@dataclass(frozen=True)
class Document:
    """Represents a single document in the project"""

    md_path: Path
    md_dir: Path
    md_str: str
    html_dir: Path
    
    @cached_property
    def html_path(self) -> Path:
        return self.html_dir/(self.md_path
                              .relative_to(self.md_dir)
                              .with_suffix(".html"))

    @cached_property
    def html_str(self) -> str:
        return markdown.markdown(self.md_str,
                                 output_format="html5",
                                 tab_length=2)

    @classmethod
    def from_file(cls,
                  md_path: Union[Path, str],
                  md_dir: Union[Path, str]=".",
                  html_dir: Union[Path, str]="public"):
        
        if isinstance(md_path, str):
            md_path = Path(md_path)
        
        if isinstance(md_dir, str):
            md_dir = Path(md_dir)
        
        if isinstance(html_dir, str):
            html_dir = Path(html_dir)

        return cls(md_path, md_dir, md_path.read_text(), html_dir)

    @classmethod
    def from_uri(cls,
                 url: str,
                 md_dir: Union[Path, str]=".",
                 html_dir: Union[Path, str]="public"):

        if isinstance(md_dir, str):
            md_dir = Path(md_dir)

        if isinstance(html_dir, str):
            html_dir = Path(html_dir)

        rel_path = urlsplit(url).path
        
        # If starts with '/', remove it
        if rel_path and rel_path[0] == "/":
            rel_path = rel_path[1:]

        rel_path = Path(rel_path)

        if rel_path.suffix not in (".html", ".htm"):
            rel_path = rel_path/"index.html"

        md_path = md_dir/rel_path.with_suffix(".md")

        return cls(md_path, md_dir, md_path.read_text(), html_dir)

    def save_html(self) -> None:
        self.html_path.write_text(self.html_str)
