import argparse

import log_parser
import report
from log_parser import Message
from dataclasses import dataclass


@dataclass
class CMDArguments:
    log_filename: str
    image_filename: str


def parse_args() -> CMDArguments:
    parser = argparse.ArgumentParser(
        description='Log visualizer for whirl-framework')
    parser.add_argument('--log', '-l', required=True)
    parser.add_argument('--output', '-o', required=True)
    args = parser.parse_args()
    return CMDArguments(args.log, args.output)


def main():
    args = parse_args()

    log = log_parser.read_log(args.log_filename)

    messages = [Message.parse_str(line) for line in log if
                Message.is_str_valid(line)]

    report.Report(messages).save(args.image_filename)


if __name__ == '__main__':
    main()
