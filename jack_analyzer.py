import os
import sys
from jack_tokenizer import JackTokenizer
from compilation_engine import CompilationEngine

def analyze_file(jack_file_path, output_xml_path):
    tokenizer = JackTokenizer(jack_file_path)
    engine = CompilationEngine(tokenizer, output_xml_path)
    engine.compile_class()
    engine.close()
    print(f"[OK] Gerado XML da Árvore Sintática: {output_xml_path}")
def main():
    if len(sys.argv) < 2:
        print("Uso: python jack_analyzer.py <arquivo.jack ou diretorio>")
        sys.exit(1)

    path = sys.argv[1]
    files = []

    if os.path.isfile(path) and path.endswith('.jack'):
        files.append(path)
    elif os.path.isdir(path):
        for f in os.listdir(path):
            if f.endswith('.jack'):
                files.append(os.path.join(path, f))

    for jack_file in files:
        # Gera o arquivo de saída com sufixo P_my.xml
        out_xml = jack_file.replace('.jack', 'P_my.xml')
        analyze_file(jack_file, out_xml)

if __name__ == "__main__":
    main()
