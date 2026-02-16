"""CLI interface for inference policy gate."""

import argparse
import json
import sys

from src.config import Config, load_config, save_config
from src.rate_limiter import RateLimiter
from src.budget import BudgetManager


def cmd_init(args):
    """Initialize configuration file."""
    config = Config(
        requests_per_minute=args.requests,
        requests_per_hour=args.requests_hour,
        token_budget=args.tokens,
        config_file=args.config,
    )
    save_config(config, args.config)
    print(f"Created config file: {args.config}")
    print(json.dumps(config.to_dict(), indent=2))
    return 0


def cmd_show(args):
    """Show current configuration."""
    config = load_config(args.config)
    print(json.dumps(config.to_dict(), indent=2))
    return 0


def cmd_check(args):
    """Check if request would be allowed."""
    config = load_config(args.config)
    limiter = RateLimiter(
        requests_per_minute=config.requests_per_minute, requests_per_hour=config.requests_per_hour
    )
    budget = BudgetManager(token_budget=config.token_budget)

    allowed = limiter.check_limit(args.user)
    budget_ok = budget.check_budget(args.user, args.tokens)

    if allowed and budget_ok:
        print(f"Allowed - user: {args.user}, tokens: {args.tokens}")
        print(f"Remaining requests: {limiter.get_remaining(args.user)}")
        print(f"Remaining tokens: {budget.get_remaining(args.user)}")
        return 0
    else:
        print(f"Blocked - user: {args.user}, tokens: {args.tokens}")
        if not allowed:
            print("Reason: Rate limit exceeded")
        if not budget_ok:
            print("Reason: Budget exceeded")
        return 1


def cmd_status(args):
    """Show status for a user."""
    config = load_config(args.config)
    limiter = RateLimiter(
        requests_per_minute=config.requests_per_minute, requests_per_hour=config.requests_per_hour
    )
    budget = BudgetManager(token_budget=config.token_budget)

    remaining_requests = limiter.get_remaining(args.user)
    remaining_tokens = budget.get_remaining(args.user)
    spent_tokens = budget.get_spent(args.user)

    print(f"User: {args.user}")
    print(f"Remaining requests: {remaining_requests}/{config.requests_per_minute} (min)")
    print(
        f"Remaining requests: {limiter.get_remaining(args.user) + spent_tokens}/{config.requests_per_hour} (hour)"
    )
    print(f"Token budget: {remaining_tokens}/{config.token_budget} (spent: {spent_tokens})")
    return 0


def cmd_reset(args):
    """Reset limits for a user."""
    config = load_config(args.config)
    limiter = RateLimiter(
        requests_per_minute=config.requests_per_minute, requests_per_hour=config.requests_per_hour
    )
    budget = BudgetManager(token_budget=config.token_budget)

    limiter.reset(args.user)
    budget.reset(args.user)

    print(f"Reset limits for user: {args.user}")
    return 0


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Inference Policy Gate - Rate limiting for LLMs")
    parser.add_argument(
        "--config", "-c", default="rate_limit_config.json", help="Path to config file"
    )

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    init_parser = subparsers.add_parser("init", help="Initialize config")
    init_parser.add_argument("--requests", "-r", type=int, default=60, help="Requests per minute")
    init_parser.add_argument("--requests-hour", type=int, default=1000, help="Requests per hour")
    init_parser.add_argument("--tokens", "-t", type=int, default=100000, help="Token budget")

    subparsers.add_parser("show", help="Show config")

    check_parser = subparsers.add_parser("check", help="Check if request allowed")
    check_parser.add_argument("user", help="User ID")
    check_parser.add_argument("tokens", type=int, help="Token count")

    status_parser = subparsers.add_parser("status", help="Show user status")
    status_parser.add_argument("user", help="User ID")

    reset_parser = subparsers.add_parser("reset", help="Reset user limits")
    reset_parser.add_argument("user", help="User ID")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    commands = {
        "init": cmd_init,
        "show": cmd_show,
        "check": cmd_check,
        "status": cmd_status,
        "reset": cmd_reset,
    }

    return commands[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
