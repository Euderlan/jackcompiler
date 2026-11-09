# src/vm_writer.py

class VMWriter:
    """
    Emite instruções da VM Jack para o arquivo de saída .vm.
    """

    SEGMENT_MAP = {
        "CONST": "constant",
        "CONSTANT": "constant",
        "ARG": "argument",
        "ARGUMENT": "argument",
        "LOCAL": "local",
        "VAR": "local",
        "STATIC": "static",
        "THIS": "this",
        "FIELD": "this",
        "THAT": "that",
        "POINTER": "pointer",
        "TEMP": "temp"
    }

    ARITHMETIC_COMMANDS = {
        "+": "add",
        "-": "sub",
        "=": "eq",
        ">": "gt",
        "<": "lt",
        "&": "and",
        "|": "or",
        "NEG": "neg",
        "NOT": "not",
        "~": "not"
    }

    def __init__(self, output_file_path: str):
        self.out = open(output_file_path, 'w', encoding='utf-8')

    def write_push(self, segment: str, index: int):
        seg = self.SEGMENT_MAP.get(segment.upper(), segment.lower())
        self.out.write(f"push {seg} {index}\n")

    def write_pop(self, segment: str, index: int):
        seg = self.SEGMENT_MAP.get(segment.upper(), segment.lower())
        self.out.write(f"pop {seg} {index}\n")

    def write_arithmetic(self, command: str):
        cmd = self.ARITHMETIC_COMMANDS.get(command, command.lower())
        self.out.write(f"{cmd}\n")

    def write_label(self, label: str):
        self.out.write(f"label {label}\n")

    def write_goto(self, label: str):
        self.out.write(f"goto {label}\n")

    def write_if(self, label: str):
        self.out.write(f"if-goto {label}\n")

    def write_call(self, name: str, n_args: int):
        self.out.write(f"call {name} {n_args}\n")

    def write_function(self, name: str, n_vars: int):
        self.out.write(f"function {name} {n_vars}\n")

    def write_return(self):
        self.out.write("return\n")

    def close(self):
        self.out.close()