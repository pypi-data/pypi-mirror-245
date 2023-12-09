import os
import argparse
from pathlib import Path
from sonic_engine.core.engine import Engine
import yaml

VERSION = "1.4.7"


def start_cli(config_file, show_logs=False):
    print("CLI started! 🚀")
    if show_logs:
        print("Logs Enabled! 📜\n")

    abs_path = os.path.abspath(config_file)
    engine = Engine(abs_path)
    engine.start()


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-v", "--version", action="version", version=f"%(prog)s {VERSION}"
    )

    subparser = parser.add_subparsers(dest="command")

    start_parser = subparser.add_parser("start")

    start_parser.add_argument("config_file")
    start_parser.add_argument("-l", "--logs", action="store_true")

    args = parser.parse_args()

    target_config_file = Path(args.config_file)

    if args.command == "start":
        if not target_config_file.exists():
            print("Config file does not exist!")
            raise SystemExit(1)
        start_cli(target_config_file, args.logs)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
