# run_tests.py
import os

test_files = [
    "nand2tetris/projects/10/Square/Square.jack",
    "nand2tetris/projects/10/Square/Main.jack",
    "nand2tetris/projects/10/Square/SquareGame.jack"
]

for test in test_files:
    os.system(f"python jack_tokenizer.py {test}")
    my_xml = test.replace(".jack", "T_my.xml")
    official_xml = test.replace(".jack", "T.xml")

    print(f"Testando {test}...")
    result = os.system(f"diff -w {my_xml} {official_xml}")

    if result == 0:
        print(f"OK: {test} passou sem diferenças!")
    else:
        print(f"ERRO: Diferenças encontradas em {test}")