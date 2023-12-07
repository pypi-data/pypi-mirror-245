
from argparse import ArgumentParser

from .diff import Diff
from .patch import patchFilesWithJson


def main():
    parser = ArgumentParser()

    parser.add_argument('-diff', nargs=3)

    parser.add_argument('-patch', nargs=3)

    args = parser.parse_args()

    if args.diff:
        diff_obj = Diff(*args.diff)
        diff_obj.writeDiffToPath()

    elif args.patch:
        patchFilesWithJson(*args.patch)

    else:
        parser.print_help()


main()
