TAREFAS = [
    {
        "nome": "classificacao_sentimento",
        "tipo": "classificacao",
        "instrucao": (
            "Você receberá um review de cliente de e-commerce. "
            "Classifique o sentimento como POSITIVO, NEGATIVO, NEUTRO ou MISTO."
        ),
        "formato_output": (
            "Responda APENAS com uma das palavras: POSITIVO, NEGATIVO, NEUTRO ou MISTO. "
            "Não adicione mais nenhum texto."
        ),
        "exemplos_fewshot": [
            {
                "input": "Produto excelente, chegou dois dias antes do prazo e a qualidade superou minhas expectativas!",
                "output": "POSITIVO",
            },
            {
                "input": "Veio completamente amassado e o vendedor se recusou a fazer a troca. Péssima experiência.",
                "output": "NEGATIVO",
            },
            {
                "input": "Produto ok, mas a entrega atrasou três dias sem aviso prévio.",
                "output": "MISTO",
            },
        ],
        "passos_cot": [
            "Identifique todas as expressões e palavras de sentimento positivo no texto.",
            "Identifique todas as expressões e palavras de sentimento negativo no texto.",
            "Avalie o peso relativo de cada grupo (qual predomina?).",
            "Se há apenas sentimentos positivos → POSITIVO. Apenas negativos → NEGATIVO. "
            "Ambos com peso similar → MISTO. Sem carga emocional clara → NEUTRO.",
            "Conclua com a classificação final.",
        ],
        "persona": "analista_cx",
    },
    {
        "nome": "extracao_dados",
        "tipo": "extracao",
        "instrucao": (
            "Extraia as informações estruturadas do texto de reclamação do cliente. "
            "Retorne um JSON com os campos: produto, preco, defeito, urgencia."
        ),
        "formato_output": (
            'Responda APENAS com um JSON válido no formato: '
            '{"produto": "...", "preco": "...", "defeito": "...", "urgencia": "alta|media|baixa"}. '
            "Não adicione texto extra fora do JSON."
        ),
        "exemplos_fewshot": [
            {
                "input": "Meu notebook Dell i7 de R$4.500 está com a tela piscando desde ontem, preciso urgente!",
                "output": '{"produto": "Notebook Dell i7", "preco": "R$4.500", "defeito": "tela piscando", "urgencia": "alta"}',
            },
            {
                "input": "Comprei uma cadeira gamer por R$899 e o encosto veio quebrado dentro da embalagem lacrada.",
                "output": '{"produto": "Cadeira gamer", "preco": "R$899", "defeito": "encosto quebrado", "urgencia": "media"}',
            },
            {
                "input": "O mouse sem fio de R$150 está com o scroll dando problema às vezes, não é urgente.",
                "output": '{"produto": "Mouse sem fio", "preco": "R$150", "defeito": "scroll com falha intermitente", "urgencia": "baixa"}',
            },
        ],
        "passos_cot": [
            "Identifique o nome completo do produto mencionado.",
            "Encontre o valor ou preço citado no texto (procure por R$, reais, etc.).",
            "Descreva o defeito ou problema relatado de forma objetiva.",
            "Avalie a urgência: 'alta' se há palavras como urgente/queimando/não funciona/preciso hoje, "
            "'media' se o problema afeta o uso normal mas não é crítico, "
            "'baixa' se é um incômodo menor ou intermitente.",
            "Monte o JSON com os quatro campos extraídos.",
        ],
        "persona": "analista_dados",
    },
    {
        "nome": "sumarizacao_review",
        "tipo": "sumarizacao",
        "instrucao": (
            "Você receberá um review longo de cliente de e-commerce. "
            "Resuma os pontos mais relevantes em exatamente 3 bullet points objetivos."
        ),
        "formato_output": (
            "Responda com exatamente 3 bullet points, cada um começando com '•'. "
            "Cada bullet deve ter no máximo 15 palavras. Seja direto e objetivo."
        ),
        "exemplos_fewshot": [
            {
                "input": (
                    "O produto chegou no prazo prometido e a embalagem estava em perfeito estado. "
                    "No entanto, o produto em si tem qualidade bem inferior ao que as fotos mostram no site — "
                    "o tecido parece sintético barato e as costuras já estão soltando. "
                    "O atendimento do vendedor foi rápido quando entrei em contato para reclamar."
                ),
                "output": (
                    "• Entrega pontual com embalagem íntegra\n"
                    "• Qualidade do produto abaixo do anunciado — fotos enganosas\n"
                    "• Atendimento do vendedor ágil na resolução da reclamação"
                ),
            },
        ],
        "passos_cot": [
            "Leia todo o review e identifique os temas principais abordados.",
            "Separe os pontos positivos dos negativos mencionados.",
            "Selecione os 3 pontos mais relevantes para um futuro comprador.",
            "Escreva cada ponto de forma concisa em um bullet começando com '•'.",
            "Revise para garantir que cada bullet tem no máximo 15 palavras.",
        ],
        "persona": "analista_cx",
    },
]


def get_tarefa(nome: str) -> dict | None:
    for t in TAREFAS:
        if t["nome"] == nome:
            return t
    return None
