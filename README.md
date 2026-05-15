# Prompt Toolkit — E-Commerce CX

FIAP · Checkpoint 02 · Prompt Engineering & Artificial Intelligence · Módulo 2

Toolkit Python modular que aplica automaticamente as 4 técnicas de prompting (**Zero-Shot, Few-Shot, Chain-of-Thought e Role Prompting**) sobre tarefas reais de atendimento ao cliente de e-commerce, compara os resultados e recomenda a melhor abordagem por tarefa.

---

## Domínio

**Atendimento ao Cliente — E-Commerce Brasileiro**

Tarefas implementadas:
| Tarefa | Tipo | Descrição |
|---|---|---|
| `classificacao_sentimento` | Classificação | Classifica reviews como POSITIVO / NEGATIVO / NEUTRO / MISTO |
| `extracao_dados` | Extração | Extrai produto, preço, defeito e urgência de reclamações |
| `sumarizacao_review` | Sumarização | Resume reviews longos em 3 bullet points objetivos |

---

## Pré-requisitos

- Python 3.10+
- [Ollama](https://ollama.com) instalado e rodando localmente
- Modelo `gpt-oss:120b` disponível no Ollama

---

## Instalação

```bash
# 1. Clone o repositório
git clone <url-do-repositorio>
cd checkpoint-2-PromptToolkit

# 2. Crie e ative o ambiente virtual
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure as variáveis de ambiente
cp .env.example .env
# Edite .env se necessário (host/modelo do Ollama)
```

---

## Configuração

Edite o arquivo `.env` conforme seu ambiente:

```env
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=gpt-oss:120b
```

Certifique-se de que o Ollama está rodando:

```bash
ollama serve
ollama pull gpt-oss:120b
```

---

## Execução

```bash
python main.py
```

O toolkit vai:
1. Carregar os inputs de `data/inputs.json`
2. Aplicar as 4 técnicas em cada tarefa × cada input
3. Medir acurácia, tokens e tempo de resposta
4. Executar teste de temperatura (0.1 / 0.5 / 1.0)
5. Salvar resultados em `output/resultados.csv`
6. Gerar gráficos em `output/graficos/`
7. Imprimir o relatório comparativo no terminal

---

## Estrutura do Projeto

```
checkpoint-2-PromptToolkit/
├── README.md
├── requirements.txt
├── .env.example
├── main.py                        # Ponto de entrada
├── src/
│   ├── __init__.py
│   ├── llm_client.py              # Conexão com Ollama API
│   ├── prompt_builder.py          # Montagem de prompts por anatomia
│   ├── techniques.py              # 4 técnicas: ZS, FS, CoT, Role
│   ├── tasks.py                   # Definição das tarefas do domínio
│   ├── evaluator.py               # Métricas: acurácia, tokens, consistência
│   └── report.py                  # Geração de tabelas e gráficos
├── data/
│   ├── inputs.json                # 5+ inputs reais por tarefa
│   └── examples.json              # Exemplos globais para few-shot
├── prompts/
│   ├── system_prompts.json        # Personas detalhadas para role prompting
│   └── templates.json             # Templates de prompt por tarefa
├── output/
│   ├── resultados.csv             # Resultados da execução
│   └── graficos/                  # PNGs dos gráficos gerados
└── docs/
    └── CP02_NomeDoGrupo.pdf       # Documentação do projeto
```

---

## Fluxo de Execução

```
inputs.json
    ↓
prompt_builder  ←  techniques (ZS / FS / CoT / Role)
    ↓
llm_client  →  Ollama API (gpt-oss:120b)
    ↓
evaluator  (acurácia · tokens · consistência · temperatura)
    ↓
report  →  output/resultados.csv + output/graficos/
```

---

## Saídas Geradas

| Arquivo | Descrição |
|---|---|
| `output/resultados.csv` | Tabela com todas as execuções: técnica, tarefa, acurácia, tokens, tempo |
| `output/graficos/acuracia_por_tecnica.png` | Barras agrupadas: acurácia por técnica × tarefa |
| `output/graficos/custo_tokens_por_tecnica.png` | Tokens médios por técnica |
| `output/graficos/consistencia_por_temperatura.png` | Consistência das respostas por temperatura |

---

## Dependências

| Biblioteca | Versão | Uso |
|---|---|---|
| `requests` | ≥ 2.31 | Chamadas à API REST do Ollama |
| `tiktoken` | ≥ 0.7 | Contagem de tokens (encoding cl100k_base) |
| `pandas` | ≥ 2.1 | Geração da tabela comparativa e CSV |
| `matplotlib` | ≥ 3.8 | Geração dos gráficos PNG |
| `python-dotenv` | ≥ 1.0 | Leitura das variáveis de ambiente |

---

## Stack Técnica

- **Linguagem:** Python 3.10+
- **LLM:** Ollama API local (gratuito) — modelo `gpt-oss:120b`
- **Tokens:** tiktoken com encoding `cl100k_base`
- **Visualização:** matplotlib + pandas
- **Sem API paga** — tudo gratuito e local
