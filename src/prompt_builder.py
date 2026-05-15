def montar_prompt(instrucao: str, contexto: str, input_dados: str, formato_output: str) -> str:
    if not instrucao or not instrucao.strip():
        raise ValueError("Instrução não pode ser vazia.")
    if not input_dados or not input_dados.strip():
        raise ValueError("Input de dados não pode ser vazio.")

    partes = [instrucao.strip()]
    if contexto and contexto.strip():
        partes.append(f"\nContexto:\n{contexto.strip()}")
    partes.append(f"\nInput:\n{input_dados.strip()}")
    if formato_output and formato_output.strip():
        partes.append(f"\n{formato_output.strip()}")

    return "\n".join(partes)


def adicionar_exemplos(prompt: str, exemplos: list) -> str:
    if not exemplos:
        return prompt

    linhas = ["\nExemplos:"]
    for ex in exemplos:
        linhas.append(f'Input: "{ex["input"]}" → Output: "{ex["output"]}"')

    bloco_exemplos = "\n".join(linhas)
    return bloco_exemplos + "\n\n" + prompt


def adicionar_cot(prompt: str, passos: list) -> str:
    if not passos:
        return prompt

    instrucao_cot = "\n\nAnalise passo a passo:\n"
    instrucao_cot += "\n".join(f"{i + 1}. {p}" for i, p in enumerate(passos))
    instrucao_cot += "\n\nApós concluir a análise, forneça sua resposta final."

    return prompt + instrucao_cot
