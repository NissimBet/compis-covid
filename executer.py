import vmachine
from compiler import parse, export
import sys

if __name__ == '__main__':
    # if len(sys.argv) < 2:
    #     print("Missing input file param")
    # elif len(sys.argv) < 3:
    #     print("Missing output file param")
    # else:
    parse("tests/test.txt", False)
    export("./export.obj")
    VM = vmachine.VirtualMachine("./export.obj")
    VM.execute_quads()
