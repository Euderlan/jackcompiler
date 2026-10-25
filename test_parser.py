import os
import pytest
from jack_tokenizer import JackTokenizer
from compilation_engine import CompilationEngine

def normalize_xml(content):
    """Remove espaços em branco no início de cada linha para ignorar diferenças de indentação."""
    return '\n'.join(line.strip() for line in content.splitlines() if line.strip())

TEST_CASES = [
    (r"C:\Users\EudFr\Downloads\nand2tetris\nand2tetris\projects\10\Square", "Square"),
    (r"C:\Users\EudFr\Downloads\nand2tetris\nand2tetris\projects\10\Square", "Main"),
    (r"C:\Users\EudFr\Downloads\nand2tetris\nand2tetris\projects\10\Square", "SquareGame"),
    (r"C:\Users\EudFr\Downloads\nand2tetris\nand2tetris\projects\10\ArrayTest", "Main"),
]

@pytest.mark.parametrize("folder, file_prefix", TEST_CASES)
def test_parser_against_official_xml(folder, file_prefix):
    jack_path = os.path.join(folder, f"{file_prefix}.jack")
    official_xml_path = os.path.join(folder, f"{file_prefix}.xml")
    
    if not os.path.exists(official_xml_path):
        official_xml_path = os.path.join(folder, f"{file_prefix}P.xml")
        
    generated_xml_path = os.path.join(folder, f"{file_prefix}P_my.xml")

    tokenizer = JackTokenizer(jack_path)
    engine = CompilationEngine(tokenizer, generated_xml_path)
    engine.compile_class()
    engine.close()

    with open(official_xml_path, 'r', encoding='utf-8') as f_exp:
        expected = normalize_xml(f_exp.read())
        
    with open(generated_xml_path, 'r', encoding='utf-8') as f_gen:
        generated = normalize_xml(f_gen.read())

    assert generated == expected, f"Divergência sintática encontrada no teste {file_prefix}.jack"