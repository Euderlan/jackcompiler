import os
import sys
import pytest

# Adiciona a pasta src no PATH para os imports funcionarem no pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from jack_tokenizer import JackTokenizer
from compilation_engine import CompilationEngine

FIXTURES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fixtures'))

TEST_FILES = ["Square", "Main", "SquareGame"]

def normalize_xml(content):
    """Remove espaços em branco e linhas vazias para comparação de sintaxe."""
    return '\n'.join(line.strip() for line in content.splitlines() if line.strip())

@pytest.mark.parametrize("file_prefix", TEST_FILES)
def test_parser_against_official_xml(file_prefix, tmp_path):
    jack_path = os.path.join(FIXTURES_DIR, f"{file_prefix}.jack")
    official_xml_path = os.path.join(FIXTURES_DIR, f"{file_prefix}.xml")
    
    generated_xml_path = os.path.join(tmp_path, f"{file_prefix}P_my.xml")

    tokenizer = JackTokenizer(jack_path)
    engine = CompilationEngine(tokenizer, generated_xml_path)
    engine.compile_class()
    engine.close()

    with open(official_xml_path, 'r', encoding='utf-8') as f_exp:
        expected = normalize_xml(f_exp.read())
        
    with open(generated_xml_path, 'r', encoding='utf-8') as f_gen:
        generated = normalize_xml(f_gen.read())

    assert generated == expected, f"Divergência sintática encontrada no arquivo {file_prefix}.jack"