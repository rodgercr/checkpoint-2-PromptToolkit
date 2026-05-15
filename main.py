import json
import os
import sys

from dotenv import load_dotenv

load_dotenv()

from src.llm_client import LLMClient
from src.techniques import zero_shot, few_shot, chain_of_thought, role_prompting
from src.tasks import TAREFAS
from src.evaluator import contar_tokens, medir_acuracia, testar_temperatura
from src import report


def carregar_json(caminho: str) -> dict:
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)


def executar():
    print("\n" + "=" * 65)
    print("  PROMPT TOOLKIT — E-Commerce CX  |  FIAP Checkpoint 02")
    print("=" * 65)

    print("\nConectando ao Ollama...")
    client = LLMClient()
    print(f"  Modelo: {client.model}  |  Host: {client.host}")

    inputs_data = carregar_json(os.path.join("data", "inputs.json"))
    system_prompts = carregar_json(os.path.join("prompts", "system_prompts.json"))

    resultados = []

    for tarefa in TAREFAS:
        nome = tarefa["nome"]
        inputs = inputs_data.get(nome, [])
        persona_key = tarefa.get("persona", "analista_cx")
        persona = system_prompts.get(persona_key, {})

        print(f"\n{'─' * 55}")
        print(f"  TAREFA: {nome}  ({len(inputs)} inputs)")
        print(f"{'─' * 55}")

        tecnicas = {
            "zero_shot": lambda t, i: (zero_shot(t, i), ""),
            "few_shot": lambda t, i: (few_shot(t, i), ""),
            "chain_of_thought": lambda t, i: (chain_of_thought(t, i), ""),
            "role_prompting": lambda t, i: role_prompting(t, i, persona),
        }

        for nome_tecnica, func_tecnica in tecnicas.items():
            print(f"\n  [{nome_tecnica}]")

            for item in inputs:
                texto_input = item["input"]
                esperado = item["esperado"]

                prompt, system = func_tecnica(tarefa, texto_input)

                resultado_llm = client.chat(
                    prompt=prompt,
                    system=system,
                    temp=0.3,
                    max_tokens=512,
                )

                resposta = resultado_llm["resposta"]
                acuracia = medir_acuracia(resposta, esperado)

                tokens_prompt = resultado_llm["tokens_prompt"] or contar_tokens(prompt + system)
                tokens_resposta = resultado_llm["tokens_resposta"] or contar_tokens(resposta)

                resultados.append({
                    "tarefa": nome,
                    "tecnica": nome_tecnica,
                    "input": texto_input[:60] + "...",
                    "resposta": resposta[:120],
                    "esperado": str(esperado)[:60],
                    "acuracia": acuracia,
                    "tokens_prompt": tokens_prompt,
                    "tokens_resposta": tokens_resposta,
                    "tokens_total": tokens_prompt + tokens_resposta,
                    "tempo_ms": resultado_llm["tempo_ms"],
                })

                print(f"    acurácia={acuracia:.2f}  tokens={tokens_prompt + tokens_resposta}  tempo={resultado_llm['tempo_ms']}ms")

    print(f"\n{'─' * 55}")
    print("  Gerando relatório e gráficos...")
    print(f"{'─' * 55}")

    df = report.gerar_tabela(resultados)
    report.grafico_acuracia(resultados)
    report.grafico_custo(resultados)

    print("\n  Executando teste de temperatura (0.1 / 0.5 / 1.0)...")
    tarefa_teste = TAREFAS[0]
    input_teste = inputs_data.get(tarefa_teste["nome"], [{}])[0].get("input", "Produto ótimo!")
    prompt_teste = zero_shot(tarefa_teste, input_teste)

    resultados_temp = testar_temperatura(
        prompt=prompt_teste,
        temps=[0.1, 0.5, 1.0],
        client=client,
        repeticoes=3,
    )
    report.grafico_temperatura(resultados_temp)

    recomendacoes = report.recomendar(resultados)
    report.imprimir_relatorio(df, recomendacoes)

    print("  Concluído. Saídas em output/\n")


if __name__ == "__main__":
    try:
        executar()
    except RuntimeError as e:
        print(f"\n[ERRO] {e}", file=sys.stderr)
        sys.exit(1)
