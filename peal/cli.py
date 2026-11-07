import argparse
import sys

from .methods import LIBRARY, find_method
from .music import score
from .proof import prove


def _cmd_methods(args):
    for m in LIBRARY:
        print(f"{m.title:32} {m.place_notation}")


def _cmd_course(args):
    m = find_method(args.method)
    rows = m.plain_course()
    for i, row in enumerate(rows):
        marker = "  <" if i % m.lead_length == 0 and i else ""
        print(f"{row}{marker}")
    print(f"{m.title}: {prove(rows).summary()}")


def _cmd_music(args):
    m = find_method(args.method)
    tally = score(m.plain_course(), args.run)
    if not tally:
        print("no music")
    for name, n in sorted(tally.items(), key=lambda kv: (-kv[1], kv[0])):
        print(f"{n:5}  {name}")


def build_parser():
    p = argparse.ArgumentParser(prog="peal", description="change ringing toolkit")
    sub = p.add_subparsers(dest="command", required=True)

    sub.add_parser("methods").set_defaults(func=_cmd_methods)

    c = sub.add_parser("course")
    c.add_argument("method")
    c.set_defaults(func=_cmd_course)

    mu = sub.add_parser("music")
    mu.add_argument("method")
    mu.add_argument("--run", type=int, default=4)
    mu.set_defaults(func=_cmd_music)
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        args.func(args)
    except KeyError as e:
        print(e.args[0], file=sys.stderr)
        return 2
    return 0
