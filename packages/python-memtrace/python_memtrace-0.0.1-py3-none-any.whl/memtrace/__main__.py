"""
Copyright (c) 2008-2023 synodriver <diguohuangjiajinweijun@gmail.com>
"""
import argparse

from memtrace import State, parse_log


def get_parser():
    parser = argparse.ArgumentParser(description="Detect memory leak at log files")
    parser.add_argument(
        "-f", "--file", help="set the log file to parse", required=True, type=str
    )
    parser.add_argument(
        "-r",
        "--rule",
        help="set the parse rule, should be a regex with a addr named group",
        nargs="+",
    )
    parser.add_argument(
        "-e", "--encoding", help="set the encoding of file", default="utf-8", type=str
    )
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()
    rules: list = args.rule
    if len(rules) % 2 == 1:
        raise ValueError("must provide even number of rules")
    rules_ = []
    for i in range(0, len(rules), 2):
        rules_.append((rules[i], rules[i + 1]))

    state = State(rules_)
    parse_log(args.file, state, args.encoding)


if __name__ == "__main__":
    main()
