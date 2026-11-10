class VMWriter:
    """
    Emissor de comandos da Máquina Virtual Jack (.vm).
    """
    SEGMENT_MAP = {
        'field': 'this',
        'var': 'local',
        'arg': 'argument',
        'static': 'static',
        'this': 'this',
        'that': 'that',
        'pointer': 'pointer',
        'temp': 'temp',
        'constant': 'constant'
    }

    def __init__(self, output_file_path: str):
        self.out = open(output_file_path, 'w', encoding='utf-8')

    def write_push(self, segment: str, index: int):
        seg = self.SEGMENT_MAP.get(segment.lower(), segment)
        self.out.write(f"push {seg} {index}\n")

    def write_pop(self, segment: str, index: int):
        seg = self.SEGMENT_MAP.get(segment.lower(), segment)
        self.out.write(f"pop {seg} {index}\n")

    def write_arithmetic(self, command: str):
        self.out.write(f"{command.lower()}\n")

    def write_label(self, label: str):
        self.out.write(f"label {label}\n")

    def write_goto(self, label: str):
        self.out.write(f"goto {label}\n")

    def write_if(self, label: str):
        self.out.write(f"if-goto {label}\n")

    def write_call(self, name: str, n_args: int):
        self.out.write(f"call {name} {n_args}\n")

    def write_function(self, name: str, n_locals: int):
        self.out.write(f"function {name} {n_locals}\n")

    def write_return(self):
        self.out.write("return\n")

    def close(self):
        if hasattr(self, 'out') and not self.out.closed:
            self.out.close()