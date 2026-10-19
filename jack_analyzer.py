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