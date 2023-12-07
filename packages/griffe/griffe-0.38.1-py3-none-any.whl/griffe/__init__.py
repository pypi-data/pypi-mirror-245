"""griffe package.

Signatures for entire Python programs.
Extract the structure, the frame, the skeleton of your project,
to generate API documentation or find breaking changes in your API.
"""

from __future__ import annotations

from griffe.agents.nodes import ObjectNode
from griffe.dataclasses import Attribute, Class, Docstring, Function, Module, Object
from griffe.diff import find_breaking_changes
from griffe.docstrings.parsers import Parser, parse_google, parse_numpy, parse_sphinx
from griffe.extensions import Extension, load_extensions
from griffe.git import load_git
from griffe.importer import dynamic_import
from griffe.loader import load
from griffe.logger import get_logger

__all__: list[str] = [
    "Attribute",
    "Class",
    "Docstring",
    "dynamic_import",
    "Extension",
    "Function",
    "find_breaking_changes",
    "get_logger",
    "load",
    "load_extensions",
    "load_git",
    "Module",
    "Object",
    "ObjectNode",
    "Parser",
    "parse_google",
    "parse_numpy",
    "parse_sphinx",
]
