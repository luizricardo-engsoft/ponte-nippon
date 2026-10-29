import json
dicionario_cultural_para_japones = {
            "bom dia": "ohayou gozaimasu",
            "obrigado": "arigatou gozaimasu",
            "onde fica o banheiro?": "Toire wa doko desu ka?",
            "Com licença / Desculpe": "Sumimasen",
            "Muito obrigado(a)": "Arigatou gozaimasu",
            "Por favor": "O-negai shimasu",
            "Este, por favor": "Kore o kudasai",
            "Quanto custa?": "Ikura desu ka?",
            "Onde fica [Lugar]?": "[Lugar] wa doko desu ka?",
            "A conta, por favor": "O-kaikei o negai shimasu",
            "Aceita cartão de crédito?": "Kurejitto kaado wa tsukaemasu ka?",
            "Você fala inglês?": "Eigo ga hanasemasu ka?",
            "Não entendo": "Wakarimasen",
            "Tudo bem / Não precisa": "Daijoubu desu",
            "Tem Wi-Fi?": "Wi-Fi wa arimasu ka?",
            "O menu, por favor": "Menyuu o kudasai",
            "Água, por favor": "Mizu o kudasai",
            "Socorro / Ajude-me": "Tasukete kudasai",
}

def pesquisar_dicionario():
    while True:
        
        entrada_de_palavra_usuario = (
            input("Digite a frase em português ou '0' para sair: ")
            .lower()
            .strip()
        )

        if entrada_de_palavra_usuario == "0":
            break

        elif entrada_de_palavra_usuario == "":
            print("\n[Erro.] Por favor, digite uma palavra válida.")

        else:
            achou_resultado = False

            for palavra, traducao in dicionario_cultural_para_japones.items():
                if entrada_de_palavra_usuario in palavra:
                    print(
                        f"\nA tradução de '{entrada_de_palavra_usuario}' para o japonês é: '{traducao}'"
                    )
                    achou_resultado = True

            if not achou_resultado:
                print(
                    f"\nNão foi possível encontrar a tradução para '{entrada_de_palavra_usuario}' no dicionário."
                )


def exibir_guia_cultural():
    costumes = [
        "->> Trocar os sapatos em determinados ambientes",
        "->> Respeitar filas",
        "->> Manter o silêncio em transporte público",
        "->> Descartar o lixo corretamente",
    ]

    return costumes


def checklist_para_viagem():
    with open("documento.json", "r", encoding="utf-8") as arquivo:
        meu_checklist = json.load(arquivo)

    nova_tarefa = input("Digite uma tarefa (ou 'sair'): ").strip()

    while nova_tarefa.lower() != "sair":
        if nova_tarefa == "":
            print("\n[Erro.] Por favor, digite uma tarefa válida.")
            nova_tarefa = input("Digite uma tarefa (ou 'sair'): ").strip()
            continue

        meu_checklist.append({"tarefa": nova_tarefa, "Concluído": False})

        with open("documento.json", "w", encoding="utf-8") as arquivo:
            json.dump(meu_checklist, arquivo, indent=4, ensure_ascii=False)

        print(f"\nTarefa '{nova_tarefa}' adicionada ao checklist.")
        nova_tarefa = input("Digite uma tarefa (ou 'sair'): ").strip()

        escolha = int(input("Qual tarefa deseja concluir? "))
        contador = 1
        tarefa_encontrada = False

        for tarefa in meu_checklist:
            if contador == escolha:
                print(f"Tarefa encontrada: {tarefa['tarefa']}")

                tarefa["Concluído"] = True
                tarefa_encontrada = True

            contador += 1

        if tarefa_encontrada:
            with open("documento.json", "w", encoding="utf-8") as arquivo:
                json.dump(meu_checklist, arquivo, indent=4, ensure_ascii=False)

            print("Tarefa marcada como concluída!")
        else:
            print("Número de tarefa inválido.")


def buscar_traducao(entrada):
    entrada = entrada.lower().strip()

    resultados = []

    for palavra, traducao in dicionario_cultural_para_japones.items():
        if entrada in palavra.lower():
            resultados.append(f"{palavra}: {traducao}")

    return resultados

