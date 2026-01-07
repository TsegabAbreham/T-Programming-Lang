"""
error.py

Utilities and exception classes to use with your parser/lexer/interpreter.

Features:
- ParseError, LexerError, InterpreterError (subclasses of Exception) with rich metadata
- TokenInfo helper to normalize token tuples like (TYPE, VALUE) or (TYPE, VALUE, line, col)
- Reporter class to collect multiple errors and print them nicely
- Convenience functions: raise_parse_error, unexpected_token, assert_token, format_error

Example usage in your parser (short):

    from error import unexpected_token, Reporter

    errs = Reporter()
    if parser.current()[0] != 'EQUAL':
        raise unexpected_token(parser)

    # or collect instead of raising
    errs.add(unexpected_token(parser))
    errs.raise_if_any()

The parser provided by you doesn't currently store line/col in tokens, so the helpers
work whether tokens are (TYPE, VALUE) or (TYPE, VALUE, LINE, COL). The message
format is intentionally simple and friendly for debugging while being flexible
for later extension.
"""

from typing import Optional, Any, Tuple, List
import sys


class BaseError(Exception):
    """Base class for errors produced by the language toolchain.

    Attributes:
        message: human readable message
        token: the token tuple that triggered the error (if any)
        pos: parser position index (if provided)
        filename: optional filename or source name
        hint: optional quick fix hint
    """

    def __init__(self, message: str, token: Optional[Tuple[Any, ...]] = None,
                 pos: Optional[int] = None, filename: Optional[str] = None,
                 hint: Optional[str] = None):
        super().__init__(message)
        self.message = message
        self.token = token
        self.pos = pos
        self.filename = filename
        self.hint = hint

    def __str__(self) -> str:
        return format_error(self)


class ParseError(BaseError):
    """Raised on parse-time problems (unexpected token, bad syntax)."""


class LexerError(BaseError):
    """Raised by the tokenizer/lexer when encountering invalid input."""


class InterpreterError(BaseError):
    """Raised at runtime when evaluating the AST (e.g. undefined var, type error)."""


def _normalize_token(token: Optional[Tuple[Any, ...]]):
    """Normalize token tuples into a dict with keys: type, value, line, col.

    Supported incoming shapes:
      (TYPE, VALUE)
      (TYPE, VALUE, LINE, COL)
      None

    """
    if token is None:
        return {"type": None, "value": None, "line": None, "col": None}
    if not isinstance(token, (list, tuple)):
        # allow passing Token objects by mistake; fall back to string
        return {"type": str(token), "value": None, "line": None, "col": None}

    if len(token) >= 4:
        ttype, value, line, col = token[0], token[1], token[2], token[3]
        return {"type": ttype, "value": value, "line": line, "col": col}
    if len(token) == 2:
        ttype, value = token
        return {"type": ttype, "value": value, "line": None, "col": None}

    # otherwise try best-effort
    return {"type": token[0] if len(token) > 0 else None,
            "value": token[1] if len(token) > 1 else None,
            "line": None, "col": None}


def format_error(err: BaseError) -> str:
    """Create a readable one-line or multi-line error message for an error object.

    This function keeps output small but includes token type/value and location
    when available.
    """
    t = _normalize_token(err.token)
    loc = ""
    if err.filename:
        loc += f"{err.filename}"
    if t.get("line") is not None:
        loc += f":{t['line']}"
        if t.get("col") is not None:
            loc += f":{t['col']}"
    elif err.pos is not None:
        loc += f" (pos={err.pos})"

    token_info = ""
    if t.get("type") is not None:
        token_info = f"token={t['type']}"
        if t.get("value") is not None:
            token_info += f"({repr(t['value'])})"

    parts = [f"Error: {err.message}"]
    if token_info:
        parts.append(token_info)
    if loc:
        parts.append(loc)
    if err.hint:
        parts.append(f"Hint: {err.hint}")

    return " — ".join(parts)


# Convenience helper functions -------------------------------------------------


def raise_parse_error(message: str, token: Optional[Tuple[Any, ...]] = None,
                      pos: Optional[int] = None, filename: Optional[str] = None,
                      hint: Optional[str] = None) -> ParseError:
    """Create and return a ParseError (caller may raise it).

    This keeps the error construction consistent across the project.
    """
    return ParseError(message, token=token, pos=pos, filename=filename, hint=hint)


def unexpected_token(parser_or_token: Any, expected: Optional[str] = None,
                     hint: Optional[str] = None) -> ParseError:
    """Create a ParseError for an unexpected token.

    Accepts either a parser-like object with .current() and .pos, or a token tuple.
    If a parser is passed the function tries to extract a token and position.

    Example:
        # inside Parser methods
        if self.current()[0] != 'EQUAL':
            raise unexpected_token(self, expected="'='")
    """
    token = None
    pos = None
    filename = None

    # parser-like object
    if hasattr(parser_or_token, "current"):
        try:
            token = parser_or_token.current()
        except Exception:
            token = None
        pos = getattr(parser_or_token, "pos", None)
        filename = getattr(parser_or_token, "filename", None)
    else:
        token = parser_or_token

    t = _normalize_token(token)
    found = f"{t.get('type') or '<EOF>'}"
    if t.get("value") is not None:
        found += f"({t['value']})"

    msg = f"Unexpected token: found {found}"
    if expected:
        msg += f", expected {expected}"

    return raise_parse_error(msg, token=token, pos=pos, filename=filename, hint=hint)


def assert_token(parser, expected_type: str, expected_name: Optional[str] = None,
                 hint: Optional[str] = None) -> None:
    """Assert that the parser.current() token is expected_type, otherwise raise.

    This helper is handy to keep parser code smaller:

        assert_token(self, 'LPAREN', hint='function calls need ()')
    """
    type_, value = parser.current()
    if type_ != expected_type:
        raise unexpected_token(parser, expected=expected_name or expected_type, hint=hint)


# Reporter to collect multiple errors -----------------------------------------


class Reporter:
    """Collects multiple errors and prints them at once.

    Use this when you want to collect and show a list of errors instead of
    failing fast on the first one.
    """

    def __init__(self):
        self._errors: List[BaseError] = []

    def add(self, err: BaseError) -> None:
        self._errors.append(err)

    def add_message(self, message: str, token: Optional[Tuple[Any, ...]] = None,
                    pos: Optional[int] = None, filename: Optional[str] = None,
                    hint: Optional[str] = None) -> None:
        self.add(ParseError(message, token=token, pos=pos, filename=filename, hint=hint))

    def has_errors(self) -> bool:
        return len(self._errors) > 0

    def display_all(self, file=None) -> None:
        if file is None:
            file = sys.stderr
        for e in self._errors:
            print(format_error(e), file=file)

    def raise_if_any(self) -> None:
        if self.has_errors():
            # If multiple errors, combine into one message for raising
            messages = [format_error(e) for e in self._errors]
            raise ParseError("Multiple errors:\n" + "\n".join(messages))


# Small utility for in-place debugging ---------------------------------------

def fatal(msg: str) -> None:
    """Print a message and exit; a tiny helper for CLI tools and quick scripts."""
    print(msg, file=sys.stderr)
    sys.exit(1)
