import vmachine

if __name__ == '__main__':
    VM = vmachine.VirtualMachine("./export.obj")
    VM.execute_quads()
