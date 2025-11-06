#!/usr/bin/env python3
import argparse


def main():
    parser = argparse.ArgumentParser(prog="nateos-cli", description="NateOS CLI (stub)")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("show", help="Show system state (stub)")
    sub.add_parser("conf", help="Enter configuration mode (stub)")

    args = parser.parse_args()
    if args.cmd == "show":
        print("(stub) show: interfaces, vlans, routes, neighbors")
    elif args.cmd == "conf":
        print("(stub) configuration mode: set system ... commit")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
