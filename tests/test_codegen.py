import os
import sys
import pytest

# Adiciona a pasta src no PATH para importar os módulos do compilador
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from jack_tokenizer import JackTokenizer
from compilation_engine import CompilationEngine

FIXTURES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fixtures'))
TEST_FILES = ["Square", "Main", "SquareGame"]

def normalize_vm(content):
    """Remove comentários, espaços extras e linhas em branco para comparação limpa."""
    lines = []
    for line in content.splitlines():
        # Remove comentários de linha em arquivos VM (ex: // comment)
        code = line.split('//')[0].strip()
        if code:
            lines.append(code)
    return '\n'.join(lines)

@pytest.mark.parametrize("file_prefix", TEST_FILES)
def test_vm_code_generation(file_prefix, tmp_path):
    jack_path = os.path.join(FIXTURES_DIR, f"{file_prefix}.jack")
    official_vm_path = os.path.join(FIXTURES_DIR, f"{file_prefix}.vm")
    generated_vm_path = os.path.join(tmp_path, f"{file_prefix}.vm")

    # Compila o arquivo .jack gerando o arquivo .vm
    tokenizer = JackTokenizer(jack_path)
    engine = CompilationEngine(tokenizer, generated_vm_path)
    engine.compile_class()
    engine.close()

    # Se existir o gabarito oficial em .vm, compara as instruções
    if os.path.exists(official_vm_path):
        with open(official_vm_path, 'r', encoding='utf-8') as f_exp:
            expected = normalize_vm(f_exp.read())

        with open(generated_vm_path, 'r', encoding='utf-8') as f_gen:
            generated = normalize_vm(f_gen.read())

        assert generated == expected, f"Divergência de código VM encontrada em {file_prefix}.jack"
    else:
        # Se não houver gabarito .vm, valida apenas se o arquivo .vm foi gerado e não está vazio
        assert os.path.exists(generated_vm_path)
        assert os.path.getsize(generated_vm_path) > 0