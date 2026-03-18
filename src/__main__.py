"""CLI for saral."""
import sys, json, argparse
from .core import Saral

def main():
    parser = argparse.ArgumentParser(description="Saral — AI Jargon Simplifier. Translate technical jargon into plain language for any audience.")
    parser.add_argument("command", nargs="?", default="status", choices=["status", "run", "info"])
    parser.add_argument("--input", "-i", default="")
    args = parser.parse_args()
    instance = Saral()
    if args.command == "status":
        print(json.dumps(instance.get_stats(), indent=2))
    elif args.command == "run":
        print(json.dumps(instance.process(input=args.input or "test"), indent=2, default=str))
    elif args.command == "info":
        print(f"saral v0.1.0 — Saral — AI Jargon Simplifier. Translate technical jargon into plain language for any audience.")

if __name__ == "__main__":
    main()
