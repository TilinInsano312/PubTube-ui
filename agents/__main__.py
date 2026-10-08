"""Top-level commands for the PubTube-ui agentic factory."""

from __future__ import annotations

import sys

from agents import doctor


def main(argv: list[str] | None = None) -> int:
    arguments = list(sys.argv[1:] if argv is None else argv)
    if arguments and arguments[0] == "doctor":
        return doctor.main(arguments[1:])
    print("Usage: python -m agents doctor [--static]", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
