# src/jack_analyzer.py

import os
import sys
from jack_tokenizer import JackTokenizer
from compilation_engine import CompilationEngine

def analyze_file(jack_file_path, output_vm_path):
    tokenizer = JackTokenizer(jack_file_path)
    engine = CompilationEngine(tokenizer, output_vm_path)
    engine.compile_class()
    engine.close()
    print(f"[OK] Gerado arquivo VM: {output_vm_path}")

def main():
    if len(sys.argv) < 2:
        print("Uso: python src/jack_analyzer.py <arquivo.jack ou diretorio>")
        sys.exit(1)

    path = sys.argv[1]
    files = []

    if os.path.isfile(path) and path.endswith('.jack'):
        files.append(path)
    elif os.path.isdir(path):
        for f in os.listdir(path):
            if f.endswith('.jack'):
                files.append(os.path.join(path, f))

    if not files:
        print(f"Nenhum arquivo .jack encontrado em '{path}'.")
        sys.exit(1)

    for jack_file in files:
        out_vm = os.path.splitext(jack_file)[0] + '.vm'
        analyze_file(jack_file, out_vm)

if __name__ == "__main__":
    main()