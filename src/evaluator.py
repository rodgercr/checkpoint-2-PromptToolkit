import json
import tiktoken


def contar_tokens(texto: str) -> int:
    try:
        enc = tiktoken.get_encoding("cl100k_base")
        return len(enc.encode(texto))
    except Exception:
        return len(texto.split())


def medir_acuracia(resposta: str, esperado) -> float:
    resposta_norm = str(resposta).strip().upper()

    if isinstance(esperado, dict):
        if not esperado:
            return 0.0
        acertos = sum(
            1 for v in esperado.values()
            if str(v).lower() in resposta.lower()
        )
        return round(acertos / len(esperado), 4)

    esperado_norm = str(esperado).strip().upper()

    if resposta_norm == esperado_norm:
        return 1.0
    if esperado_norm in resposta_norm:
        return 0.8

    palavras = [p for p in esperado_norm.split() if len(p) > 2]
    if not palavras:
        return 0.0
    matches = sum(1 for p in palavras if p in resposta_norm)
    return round(matches / len(palavras), 4)


def medir_consistencia(respostas: list) -> float:
    if not respostas:
        return 0.0
    normalizadas = [str(r).strip().upper() for r in respostas]
    mais_comum = max(set(normalizadas), key=normalizadas.count)
    return round(normalizadas.count(mais_comum) / len(normalizadas), 4)


def testar_temperatura(
    prompt: str,
    temps: list,
    system: str = "",
    client=None,
    repeticoes: int = 3,
) -> list:
    if client is None:
        from src.llm_client import LLMClient
        client = LLMClient()

    resultados = []
    for temp in temps:
        respostas = []
        for _ in range(repeticoes):
            res = client.chat(prompt=prompt, system=system, temp=temp, max_tokens=256)
            respostas.append(res["resposta"])

        consistencia = medir_consistencia(respostas)
        resultados.append({
            "temperatura": temp,
            "respostas": respostas,
            "consistencia": consistencia,
        })
    return resultados
