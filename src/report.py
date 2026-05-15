import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

OUTPUT_DIR = "output"
GRAFICOS_DIR = os.path.join(OUTPUT_DIR, "graficos")

CORES_TECNICAS = {
    "zero_shot": "#4C72B0",
    "few_shot": "#DD8452",
    "chain_of_thought": "#55A868",
    "role_prompting": "#C44E52",
}


def _garantir_dirs():
    os.makedirs(GRAFICOS_DIR, exist_ok=True)


def gerar_tabela(resultados: list) -> pd.DataFrame:
    _garantir_dirs()
    df = pd.DataFrame(resultados)
    csv_path = os.path.join(OUTPUT_DIR, "resultados.csv")
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    print(f"  → Tabela salva em {csv_path}")
    return df


def grafico_acuracia(resultados: list):
    _garantir_dirs()
    df = pd.DataFrame(resultados)
    if "tecnica" not in df.columns or "acuracia" not in df.columns:
        return

    resumo = (
        df.groupby(["tarefa", "tecnica"])["acuracia"]
        .mean()
        .unstack(fill_value=0)
    )

    fig, ax = plt.subplots(figsize=(13, 6))
    resumo.plot(kind="bar", ax=ax, color=[CORES_TECNICAS.get(c, "#888") for c in resumo.columns])
    ax.set_title("Acurácia Média por Técnica e Tarefa", fontsize=14, fontweight="bold")
    ax.set_xlabel("Tarefa", fontsize=11)
    ax.set_ylabel("Acurácia Média (0–1)", fontsize=11)
    ax.set_ylim(0, 1.15)
    ax.set_xticklabels(resumo.index, rotation=20, ha="right")
    ax.legend(title="Técnica", bbox_to_anchor=(1.02, 1), loc="upper left")
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()

    caminho = os.path.join(GRAFICOS_DIR, "acuracia_por_tecnica.png")
    plt.savefig(caminho, dpi=120)
    plt.close()
    print(f"  → Gráfico salvo em {caminho}")


def grafico_custo(resultados: list):
    _garantir_dirs()
    df = pd.DataFrame(resultados)
    if "tecnica" not in df.columns or "tokens_total" not in df.columns:
        return

    resumo = df.groupby("tecnica")["tokens_total"].mean().sort_values()

    fig, ax = plt.subplots(figsize=(9, 5))
    cores = [CORES_TECNICAS.get(t, "#888") for t in resumo.index]
    bars = ax.bar(resumo.index, resumo.values, color=cores, width=0.5)
    ax.set_title("Custo Médio de Tokens por Técnica", fontsize=14, fontweight="bold")
    ax.set_xlabel("Técnica", fontsize=11)
    ax.set_ylabel("Tokens Médios (prompt + resposta)", fontsize=11)
    ax.grid(axis="y", alpha=0.3)
    for bar in bars:
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 1,
            f"{bar.get_height():.0f}",
            ha="center",
            va="bottom",
            fontsize=10,
        )
    plt.tight_layout()

    caminho = os.path.join(GRAFICOS_DIR, "custo_tokens_por_tecnica.png")
    plt.savefig(caminho, dpi=120)
    plt.close()
    print(f"  → Gráfico salvo em {caminho}")


def grafico_temperatura(resultados_temp: list):
    _garantir_dirs()
    if not resultados_temp:
        return

    temps = [r["temperatura"] for r in resultados_temp]
    consistencias = [r["consistencia"] for r in resultados_temp]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(temps, consistencias, marker="o", linewidth=2.5, markersize=9, color="#4C72B0")
    ax.fill_between(temps, consistencias, alpha=0.15, color="#4C72B0")
    ax.set_title("Consistência de Respostas por Temperatura", fontsize=14, fontweight="bold")
    ax.set_xlabel("Temperatura", fontsize=11)
    ax.set_ylabel("Consistência (% respostas idênticas)", fontsize=11)
    ax.set_ylim(0, 1.15)
    ax.set_xticks(temps)
    ax.grid(alpha=0.3)
    for x, y in zip(temps, consistencias):
        ax.annotate(
            f"{y:.0%}",
            (x, y),
            textcoords="offset points",
            xytext=(0, 12),
            ha="center",
            fontsize=11,
        )
    plt.tight_layout()

    caminho = os.path.join(GRAFICOS_DIR, "consistencia_por_temperatura.png")
    plt.savefig(caminho, dpi=120)
    plt.close()
    print(f"  → Gráfico salvo em {caminho}")


def recomendar(resultados: list) -> dict:
    df = pd.DataFrame(resultados)
    recomendacoes = {}

    for tarefa in df["tarefa"].unique():
        df_t = df[df["tarefa"] == tarefa]
        resumo = (
            df_t.groupby("tecnica")
            .agg(acuracia_media=("acuracia", "mean"), tokens_medios=("tokens_total", "mean"), tempo_medio=("tempo_ms", "mean"))
            .reset_index()
        )
        melhor = resumo.loc[resumo["acuracia_media"].idxmax()]
        recomendacoes[tarefa] = {
            "melhor_tecnica": melhor["tecnica"],
            "acuracia": round(float(melhor["acuracia_media"]), 4),
            "tokens_medios": round(float(melhor["tokens_medios"]), 1),
            "justificativa": (
                f"Maior acurácia média ({melhor['acuracia_media']:.1%}) "
                f"com {melhor['tokens_medios']:.0f} tokens médios."
            ),
        }
    return recomendacoes


def imprimir_relatorio(df: pd.DataFrame, recomendacoes: dict):
    sep = "=" * 65
    print(f"\n{sep}")
    print("  RELATÓRIO COMPARATIVO — PROMPT TOOLKIT (E-Commerce CX)")
    print(sep)

    resumo = (
        df.groupby(["tarefa", "tecnica"])
        .agg(
            acuracia=("acuracia", "mean"),
            tokens=("tokens_total", "mean"),
            tempo_ms=("tempo_ms", "mean"),
        )
        .round(3)
    )
    print("\n" + resumo.to_string())

    print(f"\n{sep}")
    print("  RECOMENDAÇÕES POR TAREFA")
    print(sep)
    for tarefa, rec in recomendacoes.items():
        print(f"\n  {tarefa}:")
        print(f"    Melhor técnica : {rec['melhor_tecnica']}")
        print(f"    Justificativa  : {rec['justificativa']}")

    print(f"\n{sep}\n")
