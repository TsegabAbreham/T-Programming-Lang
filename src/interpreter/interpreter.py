"""Interpreter shim: re-export run from executor module."""

from .executor import run

__all__ = ["run"]
