
# Jack Compiler — Analisador Léxico (Projeto 10 Nand2Tetris)

Implementação do **analisador léxico (tokenizer)** da linguagem Jack, desenvolvido para a disciplina de **Compiladores**.

O programa lê um arquivo `.jack`, remove comentários, extrai os tokens e gera um arquivo XML estruturado no formato exigido pelo projeto 10 do Nand2Tetris.

---

## 👥 Integrantes

- Yuram Almeida Santos
- Euderlan sousa freire





## 📂 Estrutura do projeto
 

 jackcompiler/
├── jack_tokenizer.py # Tokenizer + geração do XML
├── run_tests.py # Script de testes automáticos
└── README.md




##  Como executar

### Pré-requisitos
- Python 3.8 ou superior

### 1. Analisar um arquivo `.jack` individual

```bash
python jack_tokenizer.py caminho/para/Arquivo.jack

Gera o arquivo ArquivoT_my.xml na mesma pasta do .jack.

2. Analisar um diretório inteiro
bash
python jack_tokenizer.py caminho/para/pasta/
Percorre todos os arquivos .jack da pasta e gera um XML para cada um.

3. Rodar os testes automáticos
bash
python run_tests.py
O script compara a saída gerada (*T_my.xml) com o gabarito oficial do Nand2Tetris (*T.xml) usando diff -w.

🧠 Como funciona
O tokenizer segue as seguintes etapas:

Remoção de comentários — elimina comentários de linha (//) e de bloco (/* ... */).

Tokenização — usa uma expressão regular para identificar:

stringConstant — strings entre aspas duplas

symbol — símbolos da linguagem ({ } ( ) [ ] . , ; + - * / & | < > = ~)

integerConstant — números inteiros

keyword / identifier — palavras reservadas e identificadores

Classificação — cada token é classificado em um dos cinco tipos.

Geração do XML — o resultado é escrito no formato exigido pelo Nand2Tetris, com escape de caracteres especiais (<, >, ", &).


📚 Referências
Nand2Tetris — Projeto 10

Livro: The Elements of Computing Systems — Capítulo 10