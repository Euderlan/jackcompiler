# Jack Compiler - Analisador Léxico e Sintático (Unidade 1)

Este repositório contém a implementação integrada do **Analisador Léxico (Scanner)** e do **Analisador Sintático (Parser)** para a linguagem **Jack**, desenvolvidos para a disciplina de Compiladores com base no projeto *Nand2Tetris* (Projetos 10 e 11).

---

## 👥 Identificação da Dupla
* **Integrante 1:** Euderlan Freire da Silva Abreu — **Matrícula:** 20250071198
* **Integrante 2:** Yuram Almeida Santos — **Matrícula:** 20260060213

---

## 🛠️ Tecnologias e Especificações
* **Linguagem:** Python 3.8+
* **Framework de Teste:** `pytest`
* **Paradigma:** Orientação a Objetos com Análise Sintática por Descida Recursiva (*Recursive Descent Parsing*).

---

## 📥 Instalação e Configuração

Para clonar e configurar o repositório em sua máquina local, siga os passos abaixo:

```bash
# 1. Clonar o repositório
git clone https://github.com/seu-usuario/jackcompiler.git

# 2. Entrar na pasta do projeto
cd jackcompiler

# 3. (Opcional) Instalar o pytest para execução dos testes
pip install pytest
```

---

## Estrutura do Repositório

```text
jackcompiler/
├── README.md
├── .gitignore
├── assets/                  # Imagens e diagramas da documentação
│   ├── arvore_sintatica_xml.png
│   ├── codigo_jack.png
│   └── tokens_xml.png
├── src/                     # Código-fonte principal do compilador
│   ├── compilation_engine.py # Motor sintático (regras de classe e subrotina)
│   ├── engine_base.py        # Escrita XML, indentação, consumo e validação de tipos
│   ├── expressions_mixin.py # Análise sintática de expressões, termos e operadores
│   ├── jack_analyzer.py     # Ponto de entrada (CLI) da aplicação
│   ├── jack_tokenizer.py    # Análise léxica e remoção de comentários
│   └── statements_mixin.py  # Análise sintática de comandos (if, while, let, etc.)
└── tests/                   # Suíte de testes automatizados reproduzíveis
    ├── fixtures/            # Gabaritos e arquivos Jack oficiais do Nand2Tetris
    └── test_parser.py       # Testes de integração via pytest
```

---

## Como Executar

O analisador sintático aceita como argumento o caminho de um arquivo `.jack` específico ou de um diretório contendo múltiplos arquivos `.jack`:

```bash
# Executar para um arquivo individual
python -m src.jack_analyzer tests/fixtures/Square.jack

# Executar para um diretório completo
python src/jack_analyzer.py tests/fixtures/
```

Ao executar o comando, o compilador processa a sintaxe e gera o arquivo da Árvore Sintática em formato XML (com o sufixo `P_my.xml`) no mesmo diretório de entrada.

---

## Validação e Testes Automatizados

A suíte de testes utiliza arquivos oficiais do *Nand2Tetris* armazenados em `tests/fixtures/` e compara os arquivos XML gerados com os gabaritos esperados, ignorando divergências superficiais de indentação.

Para rodar os testes unitários e de integração, execute:

```bash
pytest tests/
```

### Saída Esperada dos Testes:

```text
========================================================== test session starts ===========================================================
platform win32 -- Python 3.13.11, pytest-9.1.1, pluggy-1.5.0
rootdir: C:\Users\EudFr\OneDrive\Documentos\VSCODEPROJETOS\jackcompiler\jackcompiler
collected 3 items                                                                                                                         

tests\test_parser.py ...                                                                                                           [100%]

=========================================================== 3 passed in 0.07s ============================================================
```

---

##  Exemplo Prático de Funcionamento

Abaixo está a comparação entre o código-fonte original da linguagem Jack e o resultado gerado pelo nosso analisador léxico:

### 1. Código-Fonte Original (`Square.jack`)
Código bruto com comentários, espaços e quebras de linha:

![Código Fonte Jack](assets/codigo_jack.png)

---

### 2. Saída do Analisador Léxico (`SquareT_my.xml`)
Resultado gerado pelo `JackTokenizer` após remover comentários/espaços e classificar cada palavra em tokens:

![Saída do Analisador Léxico](assets/tokens_xml.png)

> **O que aconteceu na transformação:** 
> O analisador léxico limpou todo o texto do código-fonte (removendo comentários `//` e `/* */`) e converteu cada palavra/símbolo em sua respectiva tag de token (`keyword`, `identifier`, `symbol`, etc.), gerando a lista exata esperada pelo compilador.

### 2. Saída do Analisador Sintático (`MainP_my.xml`)
A estrutura hierárquica em XML gerada pelo *Parser* por descida recursiva:

![Árvore Sintática em XML](assets/arvore_sintatica_xml.png)

* **Descrição:** O XML final gerado representa a **Árvore Sintática (Parse Tree)** do programa. Enquanto o analisador léxico produz apenas uma lista plana de tokens soltos, o analisador sintático organiza esses tokens dentro das regras gramaticais da linguagem Jack — agrupando elementos em tags estruturais como `<class>`, `<classVarDec>`, `<subroutineDec>`, `<subroutineBody>`, `<varDec>` e `<statements>`.

## Referências

Nand2Tetris — Projeto 10
Livro: The Elements of Computing Systems — Capítulo 10
