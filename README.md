# Jack Compiler - Compilador Completo Jack para Hack VM (Projetos 10 e 11)

Este repositório contém a implementação integrada do **Compilador Jack** (`JackCompiler`), abrangendo a **Análise Léxica** (*Tokenizer*), **Análise Sintática** (*Parser*), gerenciamento de escopo via **Tabela de Símbolos** (*Symbol Table*) e a emissão de código de máquina intermediária via **Gerador de Bytecode VM** (*VM Writer*). Desenvolvido para a disciplina de Compiladores com base nos Projetos 10 e 11 do ecossistema *Nand2Tetris*.

---

## 👥 Identificação da Dupla
- **Integrante 1:** Euderlan Freire da Silva Abreu — **Matrícula:** 20250071198
- **Integrante 2:** Yuram Almeida Santos — **Matrícula:** 20260060213

---

## 🛠️ Tecnologias e Especificações
- **Linguagem:** Python 3.8+
- **Framework de Teste:** `pytest`
- **Paradigma:** Orientação a Objetos com Descida Recursiva (*Recursive Descent Parsing*) e arquitetura modular baseada em *Mixins*.
- **Alvo de Compilação:** Bytecode da *Hack Virtual Machine* (`.vm`).

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

## 📁 Estrutura do Repositório

```text
jackcompiler/
├── README.md                # Documentação unificada e atualizada do compilador
├── .gitignore               # Regras para ignorar temporários, cache e artefatos .vm/.xml
├── assets/                  # Imagens e diagramas da documentação
│   ├── arvore_sintatica_xml.png
│   ├── codigo_jack.png
│   └── tokens_xml.png
├── src/                     # Código-fonte principal do compilador
│   ├── compilation_engine.py # Motor de compilação global (classes, subrotinas e prólogos)
│   ├── engine_base.py        # Validação sintática e consumo de tokens sem ruído XML
│   ├── expressions_mixin.py # Tradução sintática/semântica de expressões, termos e chamadas
│   ├── statements_mixin.py  # Tradução sintática/semântica de comandos (let, if, while, do, return)
│   ├── symbol_table.py      # Gerenciamento de tabela de símbolos (escopos de classe e método)
│   ├── vm_writer.py          # Emissor baixo nível de instruções VM (push, pop, call, function, etc.)
│   ├── jack_tokenizer.py    # Análise léxica e remoção de comentários
│   └── jack_analyzer.py     # CLI e ponto de entrada da compilação
└── tests/                   # Suíte de testes automatizados reproduzíveis
    ├── fixtures/            # Programas Jack (.jack) e gabaritos VM oficiais (.vm)
    ├── test_codegen.py      # Testes de geração e equivalência de Bytecode VM
    ├── test_parser.py       # Testes legados de análise sintática XML (Projeto 10)
    └── run_tests.py         # Script utilitário para execução rápida
```

---

## 🚀 Como Executar

O compilador aceita como argumento o caminho de um arquivo `.jack` individual ou de um diretório contendo múltiplos arquivos `.jack`:

```bash
# Executar para um arquivo individual
python src/jack_analyzer.py tests/fixtures/Square.jack

# Executar para um diretório completo
python src/jack_analyzer.py "C:\Users\EudFr\Downloads\nand2tetris\nand2tetris\projects\11\Square"
```

Ao executar o comando, o compilador processa o código Jack, resolve símbolos e gera o arquivo correspondente em **bytecode VM (`.vm`)** no mesmo diretório de entrada.

---

## 🧪 Validação e Testes Automatizados

A suíte de testes utiliza os programas oficiais do *Nand2Tetris* armazenados em `tests/fixtures/` (`Square`, `Main`, `SquareGame`) e compara o bytecode VM gerado instrução por instrução contra os gabaritos esperados.

Para rodar a validação do gerador de código VM, execute:

```bash
pytest tests/test_codegen.py
```

### Saída Esperada dos Testes:

```text
========================================================== test session starts ===========================================================
platform win32 -- Python 3.13.11, pytest-9.1.1, pluggy-1.5.0
rootdir: C:\Users\EudFr\OneDrive\Documentos\VSCODEPROJETOS\jackcompiler\jackcompiler
collected 3 items                                                                                                                         

tests\test_codegen.py ...                                                                                                          [100%]

=========================================================== 3 passed in 0.08s ============================================================
```

---

## 🏛️ Arquitetura do Compilador e Gerador de Código VM

O processo de compilação da Unidade 2 (Projeto 11) opera através da integração de quatro componentes principais:

1. **`SymbolTable` (Tabela de Símbolos):**
   - Mapeia identificadores para seus respectivos tipos (`int`, `boolean`, `char`, `className`), categorias (`STATIC`, `FIELD`, `ARG`, `VAR`) e índices numéricos nos segmentos da VM.
   - Gerencia escopos aninhados de **Classe** e de **Subrotina**.

2. **`VMWriter` (Emissor VM):**
   - Abstrai a sintaxe da VM da arquitetura Hack, fornecendo rotinas como `write_push`, `write_pop`, `write_arithmetic`, `write_label`, `write_goto`, `write_if`, `write_call`, `write_function` e `write_return`.

3. **`CompilationEngine` & Mixins (`StatementsMixin`, `ExpressionsMixin`):**
   - **Prólogos de Subrotinas:** Alocação de memória no Heap (`Memory.alloc`) para construtores (`constructor`) e ancoragem do ponteiro de instância (`pointer 0`) para métodos (`method`).
   - **Controle de Fluxo:** Geração de rótulos únicos (`IF_TRUE`, `IF_FALSE`, `IF_END`, `WHILE_EXP`, `WHILE_END`) para tradução de blocos `if/else` e laços `while`.
   - **Manipulação de Arrays:** Armazenamento temporário do ponteiro via `temp 0` e ajuste dos segmentos `pointer 1` / `that 0` para leituras e atribuições seguras do tipo `a[i] = expr`.

---

## 🎮 Execução no VM Emulator (Nand2Tetris)

Para testar a execução interativa dos programas compilados no **VM Emulator** oficial:

1. Compile o diretório do projeto desejado:
   ```powershell
   python src/jack_analyzer.py "C:\Users\EudFr\Downloads\nand2tetris\nand2tetris\projects\11\Square"
   ```
2. Abra o **VM Emulator** (`VMEmulator.bat`).
3. Clique em **Load Program** (ícone da pasta amarela) e selecione a pasta do projeto (ex: `Square`).
4. Selecione **Sim** na janela referente ao carregamento do Jack OS embutido (*built-in OS*).
5. Defina a velocidade para *No Animation* e clique em **Play (`▶`)**.

---

## 🔄 Exemplo de Tradução (Jack -> VM)

### Código Fonte em Jack:
```jack
method void moveSquare() {
    if (direction = 1) {
        do square.up();
    }
    return;
}
```

### Bytecode VM Gerado:
```text
function SquareGame.moveSquare 0
push argument 0
pop pointer 0
push this 1
push constant 1
eq
if-goto IF_TRUE0
goto IF_FALSE0
label IF_TRUE0
push this 0
call Square.up 1
pop temp 0
label IF_FALSE0
push constant 0
return
```

---

## 📚 Referências

- **Nand2Tetris — Projeto 10:** *Compiler I: Syntax Analysis*
- **Nand2Tetris — Projeto 11:** *Compiler II: Code Generation*
- **Livro:** *The Elements of Computing Systems* (Nisan & Schocken) — Capítulos 10 e 11.