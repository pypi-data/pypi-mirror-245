import argparse
import sys

from ao_conventional_pre_commit import format

RESULT_SUCCESS = 0
RESULT_FAIL = 1


class Colors:
    LBLUE = "\033[00;34m"
    LRED = "\033[01;31m"
    RESTORE = "\033[0m"
    YELLOW = "\033[00;33m"


def main(argv=[]):
    parser = argparse.ArgumentParser(
        prog="conventional-pre-commit",
        description="Check a git commit message for AO-compliant Conventional Commits formatting.",
    )
    parser.add_argument("types", type=str, nargs="*", default=format.DEFAULT_TYPES, help="Optional list of types to support")
    parser.add_argument("input", type=str, help="A file containing a git commit message")
    parser.add_argument(
        "--force-scope", action="store_false", default=True, dest="optional_scope", help="Force commit to have scope defined."
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Force commit to strictly follow Conventional Commits formatting. Disallows fixup! style commits.",
    )
    parser.add_argument(
        "--optional-ticket",
        action="store_true",
        default=False,
        dest="optional_ticket",
        help="Allow for optional ticket number.  This enables default conventional commit style.",
    )
    parser.add_argument(
        "--force-colon-after-ticket",
        action="store_false",
        default=True,
        dest="optional_colon_after_ticket",
        help="Force commit to contain a colon after ticket number.",
    )

    if len(argv) < 1:
        argv = sys.argv[1:]

    try:
        args = parser.parse_args(argv)
    except SystemExit:
        return RESULT_FAIL

    try:
        with open(args.input, encoding="utf-8") as f:
            message = f.read()
    except UnicodeDecodeError:
        print(
            f"""
{Colors.LRED}[Bad Commit message encoding] {Colors.RESTORE}

{Colors.YELLOW}ao-conventional-pre-commit couldn't decode your commit message.{Colors.RESTORE}
{Colors.YELLOW}UTF-8{Colors.RESTORE} encoding is assumed, please configure git to write commit messages in UTF-8.
See {Colors.LBLUE}https://git-scm.com/docs/git-commit/#_discussion{Colors.RESTORE} for more.
        """
        )
        return RESULT_FAIL

    if not args.strict:
        if format.has_autosquash_prefix(message):
            return RESULT_SUCCESS

    if format.is_conventional(
        message, args.types, args.optional_scope, args.optional_ticket, args.optional_colon_after_ticket
    ):
        return RESULT_SUCCESS
    else:
        print(
            f"""
        {Colors.LRED}[Bad Commit message] >>{Colors.RESTORE} {message}
        {Colors.YELLOW}Your commit message does not follow Conventional Commits formatting
        {Colors.LBLUE}https://www.conventionalcommits.org/{Colors.YELLOW}

        AO Conventional Commits start with one of the below types, followed by a colon,
        followed by a ticket number and colon, followed by the commit subject and
        an optional body separated by a blank line:{Colors.RESTORE}

            {" ".join(format.conventional_types(args.types))}

        {Colors.YELLOW}Example commit message adding a feature:{Colors.RESTORE}

            feat: SVCOR-12: implement new API

        {Colors.YELLOW}Example commit message fixing an issue:{Colors.RESTORE}

            fix: DTCT-99: remove infinite loop

        {Colors.YELLOW}Example commit with scope in parentheses after the type for more context:{Colors.RESTORE}

            fix(account): PROSP-55: remove infinite loop

        {Colors.YELLOW}Example commit with a body:{Colors.RESTORE}

            fix: DATLA-42: remove infinite loop

            Additional information on the issue caused by the infinite loop
            """
        )
        return RESULT_FAIL


if __name__ == "__main__":
    raise SystemExit(main())
