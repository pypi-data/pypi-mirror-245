import sys
from .data import main as data
from mlvault.config import config, set_auth_config

NAMESPACES = ["data", "config"]

def exit_with_help(msg=""):
    if msg:
        print()
        print("  Error:")
        print(f"    {msg}")
        print()
    print("Usage: mlvcli <namespace> <args>")
    print("Namespaces: data, config")
    print("For help on a namespace, run: mlvault <namespace> --help")
    exit(1)

def main():
    input_args = sys.argv[1:]
    if len(sys.argv) < 2:
        exit_with_help("Invalid args")
    namespace_name, *args = input_args
    if namespace_name not in NAMESPACES:
        print(f"Namespace {namespace_name} not found")
        exit(1)
    if namespace_name == "data":
        data(args)
    elif namespace_name == "config":
        if len(args) == 0:
            config()
        else:
            r_index = args.index("-r")
            r_value = args[r_index+1]
            w_index = args.index("-w")
            w_value = args[w_index+1]
            if r_value:
                set_auth_config(r_token=r_value)
            if w_value:
                set_auth_config(w_token=w_value)
        pass
