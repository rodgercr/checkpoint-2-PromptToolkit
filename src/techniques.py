from src.prompt_builder import montar_prompt, adicionar_exemplos, adicionar_cot


def zero_shot(tarefa: dict, input_texto: str) -> str:
    return montar_prompt(
        instrucao=tarefa["instrucao"],
        contexto="",
        input_dados=input_texto,
        formato_output=tarefa["formato_output"],
    )


def few_shot(tarefa: dict, input_texto: str, exemplos: list = None) -> str:
    prompt_base = montar_prompt(
        instrucao=tarefa["instrucao"],
        contexto="",
        input_dados=input_texto,
        formato_output=tarefa["formato_output"],
    )
    exemplos_usados = exemplos if exemplos else tarefa.get("exemplos_fewshot", [])
    return adicionar_exemplos(prompt_base, exemplos_usados)


def chain_of_thought(tarefa: dict, input_texto: str, passos: list = None) -> str:
    prompt_base = montar_prompt(
        instrucao=tarefa["instrucao"],
        contexto="",
        input_dados=input_texto,
        formato_output=tarefa["formato_output"],
    )
    passos_usados = passos if passos else tarefa.get("passos_cot", [])
    return adicionar_cot(prompt_base, passos_usados)


def role_prompting(tarefa: dict, input_texto: str, persona: dict) -> tuple:
    system = persona.get("system_prompt", "Você é um assistente especializado.")
    user = montar_prompt(
        instrucao=tarefa["instrucao"],
        contexto="",
        input_dados=input_texto,
        formato_output=tarefa["formato_output"],
    )
    return system, user
