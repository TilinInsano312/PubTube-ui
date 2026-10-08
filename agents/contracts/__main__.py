"""CLI for validating versioned task contracts."""

from __future__ import annotations

import argparse
import sys

from .validator import ContractError, load_contracts


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate PubTube task contracts without executing them.")
    parser.add_argument("path", help="JSONL file or directory containing JSONL contracts")
    args = parser.parse_args(argv)
    try:
        contracts = load_contracts(args.path)
    except (ContractError, OSError) as error:
        print(f"CONTRACTS INVALID: {error}", file=sys.stderr)
        return 1
    sources = {contract.source for contract in contracts}
    print(f"CONTRACTS VALID: {len(contracts)} task(s) from {len(sources)} file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
