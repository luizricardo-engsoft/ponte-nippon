
import tkinter as tk
import json
import os
from guia_cultural import exibir_guia_cultural, buscar_traducao

AZUL = "#0B1F3A"
VERMELHO = "#E63946"
CREME = "#FAF6F0"
BRANCO = "#FFFFFF"
ARQUIVO = os.path.join(os.path.dirname(__file__), "documento.json")


def iniciar_aplicacao():
    janela = tk.Tk()
    janela.title("Ponte Nippon")
    janela.geometry("1200x650")
    janela.configure(bg=CREME)

    menu = tk.Frame(janela, bg=AZUL, width=220)
    menu.pack(side="left", fill="y")
    menu.pack_propagate(False)

    area = tk.Frame(janela, bg=CREME)
    area.pack(fill="both", expand=True, padx=25, pady=20)

    botoes = {}

    def pagina(titulo):
        for w in area.winfo_children():
            w.destroy()

        for nome, botao in botoes.items():
            botao.config(bg=VERMELHO if nome == titulo else AZUL)

        tk.Label(
            area, text=titulo, font=("Arial", 23, "bold"),
            bg=CREME, fg=AZUL
        ).pack(anchor="w", pady=(0, 20))

    def inicio():
        pagina("Bem-vindo ao Ponte Nippon")

        tk.Label(
            area,
            text="Seu guia para se preparar, aprender\n"
                 "e viver essa jornada entre Brasil e Japão.",
            font=("Arial", 13), bg=CREME, fg=AZUL,
            justify="left"
        ).pack(anchor="w", pady=(0, 25))

        cards = tk.Frame(area, bg=CREME)
        cards.pack(fill="x")

        for nome, descricao, comando in [
            ("Checklist", "Organize seus documentos e tarefas.", checklist),
            ("Dicionário", "Aprenda frases e expressões em japonês.", dicionario),
            ("Guia Cultural", "Conheça costumes e tradições japonesas.", guia),
        ]:
            card = tk.Frame(
                cards, bg=BRANCO, padx=12, pady=18,
                highlightbackground="#DCDDE0", highlightthickness=1
            )
            card.pack(side="left", fill="both", expand=True, padx=(0, 10))

            tk.Label(
                card, text=nome, font=("Arial", 14, "bold"),
                bg=BRANCO, fg=AZUL
            ).pack(anchor="w", pady=(0, 12))

            tk.Label(
                card, text=descricao, wraplength=175,
                justify="left", bg=BRANCO, fg=AZUL
            ).pack(anchor="w", pady=(0, 20))

            tk.Button(
                card, text="Acessar →", command=comando,
                bg=AZUL, fg=BRANCO, relief="flat"
            ).pack(fill="x")

        tk.Label(
            area,
            text="Cultura, linguagem e planejamento.\n"
                 "Tudo para transformar o sonho do Japão em realidade.",
            font=("Arial", 12), bg="#EDF1F8", fg=AZUL,
            padx=15, pady=20
        ).pack(fill="x", pady=25)

    def dicionario():
        pagina("Dicionário Japonês-Português")

        campo = tk.Entry(area, font=("Arial", 13))
        campo.pack(fill="x", pady=5)

        resultado = tk.Label(
            area, text="", bg=CREME, fg=AZUL,
            font=("Arial", 12), justify="left"
        )
        resultado.pack(anchor="w", pady=15)

        def pesquisar():
            termo = campo.get().strip()

            if not termo:
                resultado.config(text="Digite uma palavra ou frase.")
                return

            try:
                dados = buscar_traducao(termo)
                resultado.config(
                    text="\n".join(dados) if dados
                    else "Frase não encontrada."
                )
            except Exception as erro:
                resultado.config(text=f"Erro: {erro}")

        tk.Button(
            area, text="Pesquisar", command=pesquisar,
            bg=VERMELHO, fg=BRANCO
        ).pack(anchor="w")

        campo.bind("<Return>", lambda evento: pesquisar())

    def guia():
        pagina("Guia Cultural do Japão")

        try:
            dados = exibir_guia_cultural()
            texto = dados if isinstance(dados, str) else "\n\n".join(dados)
        except Exception as erro:
            texto = f"Não foi possível carregar o guia: {erro}"

        caixa = tk.Text(
            area, wrap="word", font=("Arial", 12),
            bg=BRANCO, fg=AZUL
        )
        caixa.pack(fill="both", expand=True)
        caixa.insert("1.0", texto)
        caixa.config(state="disabled")

    def checklist():
        pagina("Checklist de documentação")

        def carregar():
            try:
                with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
                    return json.load(arquivo)
            except FileNotFoundError:
                return []
            except (OSError, json.JSONDecodeError):
                return []

        def salvar(tarefas):
            with open(ARQUIVO, "w", encoding="utf-8") as arquivo:
                json.dump(
                    tarefas, arquivo,
                    indent=4, ensure_ascii=False
                )

        campo = tk.Entry(area, font=("Arial", 12))
        campo.pack(fill="x", pady=5)

        lista_tarefas = tk.Listbox(
            area,
            font=("Arial", 12),
            bg=BRANCO,
            fg=AZUL,
            selectbackground=AZUL,
            selectforeground=BRANCO,
            height=14
        )
        lista_tarefas.pack(fill="both", expand=True, pady=10)

        mensagem = tk.Label(area, text="", bg=CREME, fg=AZUL)
        mensagem.pack(anchor="w", pady=5)

        def atualizar_lista():
            lista_tarefas.delete(0, tk.END)

            for tarefa in carregar():
                simbolo = "☑" if tarefa.get("Concluído", False) else "☐"
                nome = tarefa.get("tarefa", "Tarefa")
                lista_tarefas.insert(tk.END, f"{simbolo}  {nome}")

        def adicionar():
            nome = campo.get().strip()

            if not nome:
                mensagem.config(text="Digite o nome da tarefa.")
                return

            tarefas = carregar()
            tarefas.append({
                "tarefa": nome,
                "Concluído": False
            })

            try:
                salvar(tarefas)
                campo.delete(0, tk.END)
                atualizar_lista()
                mensagem.config(text="Tarefa adicionada.")
            except OSError as erro:
                mensagem.config(text=f"Erro ao salvar: {erro}")

        def marcar():
            selecao = lista_tarefas.curselection()

            if not selecao:
                mensagem.config(text="Selecione uma tarefa primeiro.")
                return

            indice = selecao[0]
            tarefas = carregar()

            if indice >= len(tarefas):
                return

            tarefas[indice]["Concluído"] = not tarefas[indice].get(
                "Concluído", False
            )

            try:
                salvar(tarefas)
                atualizar_lista()
                lista_tarefas.selection_set(indice)
                mensagem.config(text="Status da tarefa atualizado.")
            except OSError as erro:
                mensagem.config(text=f"Erro ao salvar: {erro}")

        def excluir_tarefa():
            selecao = lista_tarefas.curselection()

            if not selecao:
                mensagem.config(text="Selecione uma tarefa para excluir.")
                return

            indice = selecao[0]
            tarefas = carregar()

            if indice >= len(tarefas):
                return

            nome = tarefas[indice].get("tarefa", "Tarefa")
            tarefas.pop(indice)

            try:
                salvar(tarefas)
                atualizar_lista()
                mensagem.config(text=f"Tarefa '{nome}' excluída.")
            except OSError as erro:
                mensagem.config(text=f"Erro ao salvar: {erro}")

        botoes_checklist = tk.Frame(area, bg=CREME)
        botoes_checklist.pack(anchor="w")

        tk.Button(
            botoes_checklist,
            text="Adicionar tarefa",
            command=adicionar,
            bg=AZUL,
            fg=BRANCO
        ).pack(side="left", padx=(0, 8))

        tk.Button(
            botoes_checklist,
            text="Marcar / desmarcar",
            command=marcar,
            bg=AZUL,
            fg=BRANCO
        ).pack(side="left", padx=(0, 8))

        botao_excluir = tk.Button(
            botoes_checklist,
            text="Excluir tarefa",
            command=excluir_tarefa,
            bg=VERMELHO,
            fg=BRANCO
        )
        botao_excluir.pack(side="left")

        campo.bind("<Return>", lambda evento: adicionar())

        atualizar_lista()

    tk.Label(
        menu, text="⛩\nPonte Nippon\nBRASIL → JAPÃO",
        font=("Arial", 17, "bold"), bg=AZUL, fg=BRANCO,
        pady=25
    ).pack(fill="x")

    for nome, simbolo, comando in [
        ("Início", "⌂", inicio),
        ("Dicionário", "▤", dicionario),
        ("Guia Cultural", "◉", guia),
        ("Checklist", "☑", checklist),
    ]:
        botao = tk.Button(
            menu, text=f"  {simbolo}   {nome}", command=comando,
            font=("Arial", 11), anchor="w", padx=15, pady=12,
            bg=AZUL, fg=BRANCO, activeforeground=BRANCO,
            activebackground=VERMELHO, relief="flat"
        )
        botao.pack(fill="x", padx=12, pady=3)
        botoes[nome] = botao

    inicio()
    janela.mainloop()


if __name__ == "__main__":
    iniciar_aplicacao()
