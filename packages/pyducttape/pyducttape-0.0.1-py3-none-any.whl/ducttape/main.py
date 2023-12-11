import argparse
import sys

import ducttape


def main():
    args = _parse_args()
    output_file = _open_output(args)
    output = ducttape.script(
        args.script,
        add_python_modules=args.add_python_module,
        add_python_paths=args.add_python_path,
        python_binary=args.python_binary,
        copy_shebang=args.copy_shebang,
        public_key=args.public_key,
        keygen=args.keygen,
    )
    if output is None:
        return
    output_file.write(output)


def _open_output(args):
    if args.output_file is None:
        return sys.stdout
    else:
        return open(args.output_file, "w")


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("script", nargs="?", help="path to script to ducttape")
    parser.add_argument("--keygen", action="store_true", help="generate a keypair")
    parser.add_argument(
        "--add-python-module", action="append", default=[], help="add a python module"
    )
    parser.add_argument(
        "--add-python-path", action="append", default=[], help="add a python path"
    )
    parser.add_argument("--python-binary", help="path to python binary")
    parser.add_argument("--output-file", help="path to output file")
    parser.add_argument("--public-key", help="path to public key")
    parser.add_argument(
        "--copy-shebang", action="store_true", help="copy shebang from source file"
    )
    return parser.parse_args()


if __name__ == "__main__":
    main()
