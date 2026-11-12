
import tkinter as tk
from tkinter import simpledialog
import json
import os
from guia_cultural import exibir_guia_cultural, buscar_traducao
from tema import (
    AZUL, AZUL_CLARO, VERMELHO, ROSA, ROSA_FORTE, CREME, BRANCO, BORDA,
    CINZA_AZULADO, TEXTO_SUAVE, fonte, desenhar_banner, quadrado_icone,
    galho_sakura
)

ARQUIVO = os.path.join(os.path.dirname(__file__), "documento.json")
LARGURA_MENU = 230
LARGURA_AREA = 920


def iniciar_aplicacao():
    janela = tk.Tk()
    janela.title("Ponte Nippon")
    janela.geometry("1200x700")
    janela.configure(bg=CREME)
    janela.resizable(False, False)

    rodape = tk.Frame(
        janela, bg=BRANCO, height=38,
        highlightbackground=BORDA, highlightthickness=1
    )
    rodape.pack(side="bottom", fill="x")
    rodape.pack_propagate(False)

    tk.Label(
        rodape, text="Ponte Nippon   —   Mais do que uma viagem, um encontro de culturas.",
        font=fonte(9), bg=BRANCO, fg=TEXTO_SUAVE
    ).pack(side="left", padx=25)

    tk.Label(
        rodape, text="⛩", font=fonte(13), bg=BRANCO, fg=VERMELHO
    ).pack(side="right", padx=25)

    menu = tk.Frame(janela, bg=AZUL, width=LARGURA_MENU)
    menu.pack(side="left", fill="y")
    menu.pack_propagate(False)

    area = tk.Frame(janela, bg=CREME)
    area.pack(fill="both", expand=True, padx=25, pady=18)

    botoes = {}

    def pagina(titulo, ativo=None):
        for w in area.winfo_children():
            w.destroy()

        for nome, botao in botoes.items():
            botao.config(bg=VERMELHO if nome == (ativo or titulo) else AZUL)

        if titulo:
            tk.Label(
                area, text=titulo, font=fonte(23, "bold"),
                bg=CREME, fg=AZUL
            ).pack(anchor="w", pady=(0, 18))

    def inicio():
        pagina("", ativo="Início")

        desenhar_banner(
            area, LARGURA_AREA, 215,
            "Bem-vindo ao", "Ponte Nippon",
            "Seu guia para se preparar, aprender\n"
            "e viver essa jornada entre Brasil e Japão."
        ).pack(anchor="w")

        cards = tk.Frame(area, bg=CREME)
        cards.pack(fill="x", pady=(18, 0))

        for nome, simbolo, cor_icone, descricao, comando in [
            ("Checklist", "☑", "#FDE7EA",
             "Organize seus documentos,\nrequisitos e tudo o que você\nprecisa para a sua viagem.",
             checklist),
            ("Dicionário", "▤", AZUL_CLARO,
             "Aprenda as principais\nfrases e expressões em\njaponês.",
             dicionario),
            ("Guia Cultural", "◉", "#EFEDFF",
             "Conheça os costumes,\ntradições e etiqueta\njaponesa.",
             guia),
        ]:
            card = tk.Frame(
                cards, bg=BRANCO, padx=16, pady=18,
                highlightbackground=BORDA, highlightthickness=1
            )
            card.pack(side="left", fill="both", expand=True, padx=(0, 12))

            quadrado_icone(card, simbolo, cor_icone, AZUL).pack(anchor="w", pady=(0, 14))

            tk.Label(
                card, text=nome, font=fonte(14, "bold"),
                bg=BRANCO, fg=AZUL
            ).pack(anchor="w", pady=(0, 8))

            tk.Label(
                card, text=descricao, font=fonte(10),
                justify="left", bg=BRANCO, fg=TEXTO_SUAVE
            ).pack(anchor="w", pady=(0, 16))

            tk.Button(
                card, text="Acessar  →", command=comando,
                font=fonte(10, "bold"), bg=AZUL, fg=BRANCO,
                relief="flat", borderwidth=0, highlightthickness=0,
                pady=6, cursor="hand2"
            ).pack(fill="x")

        citacao = tk.Frame(cards, bg=ROSA, padx=16, pady=18, width=205)
        citacao.pack(side="left", fill="both")
        citacao.pack_propagate(False)

        tk.Label(
            citacao, text="\"Novos horizontes\nexigem preparo.\"",
            font=fonte(12, "bold"), justify="left", bg=ROSA, fg=AZUL
        ).pack(anchor="w")

        tk.Label(
            citacao,
            text="O conhecimento é a ponte\nentre o seu presente\ne o seu futuro.",
            font=fonte(9), justify="left", bg=ROSA, fg=AZUL
        ).pack(anchor="w", pady=(12, 0))

        tk.Label(
            citacao, text="⛩", font=fonte(18), bg=ROSA, fg=VERMELHO
        ).pack(anchor="w", pady=(16, 0))

        faixa = tk.Frame(area, bg=AZUL_CLARO, padx=20, pady=16)
        faixa.pack(fill="x", pady=(18, 0))

        tk.Label(
            faixa, text="日本へ", font=fonte(14), bg=AZUL_CLARO, fg=AZUL
        ).pack(side="right")

        textos = tk.Frame(faixa, bg=AZUL_CLARO)
        textos.pack(side="left")

        tk.Label(
            textos, text="Cultura, linguagem, planejamento.",
            font=fonte(11, "bold"), bg=AZUL_CLARO, fg=AZUL
        ).pack(anchor="w")

        tk.Label(
            textos,
            text="Tudo o que você precisa para transformar o sonho do Japão em realidade.",
            font=fonte(10), bg=AZUL_CLARO, fg=TEXTO_SUAVE
        ).pack(anchor="w")

    def dicionario():
        pagina("Dicionário Japonês-Português", ativo="Dicionário")

        campo = tk.Entry(
            area, font=fonte(12), bg=BRANCO, fg=AZUL, relief="flat",
            highlightbackground=BORDA, highlightcolor=AZUL, highlightthickness=1
        )
        campo.pack(fill="x", ipady=8, pady=(0, 12))

        resultado = tk.Label(
            area, text="", bg=CREME, fg=AZUL,
            font=fonte(12), justify="left"
        )

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
            font=fonte(10, "bold"), bg=VERMELHO, fg=BRANCO,
            relief="flat", borderwidth=0, highlightthickness=0,
            padx=20, pady=7, cursor="hand2"
        ).pack(anchor="w")

        resultado.pack(anchor="w", pady=18)

        campo.bind("<Return>", lambda evento: pesquisar())
        campo.focus_set()

    def guia():
        pagina("Guia Cultural do Japão", ativo="Guia Cultural")

        try:
            dados = exibir_guia_cultural()
            texto = dados if isinstance(dados, str) else "\n\n".join(dados)
        except Exception as erro:
            texto = f"Não foi possível carregar o guia: {erro}"

        caixa = tk.Text(
            area, wrap="word", font=fonte(12),
            bg=BRANCO, fg=AZUL, relief="flat",
            padx=20, pady=18, spacing1=2, spacing3=4,
            highlightbackground=BORDA, highlightthickness=1
        )
        caixa.pack(fill="both", expand=True)
        caixa.insert("1.0", texto)
        caixa.config(state="disabled")

    def checklist():
        pagina("Checklist de documentação", ativo="Checklist")

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

        campo = tk.Entry(
            area, font=fonte(12), bg=BRANCO, fg=AZUL, relief="flat",
            highlightbackground=BORDA, highlightcolor=AZUL, highlightthickness=1
        )
        campo.pack(fill="x", ipady=8)

        lista_tarefas = tk.Listbox(
            area,
            font=fonte(12),
            bg=BRANCO,
            fg=AZUL,
            selectbackground=AZUL,
            selectforeground=BRANCO,
            relief="flat",
            highlightbackground=BORDA,
            highlightthickness=1,
            activestyle="none",
            height=13
        )
        lista_tarefas.pack(fill="both", expand=True, pady=12)

        mensagem = tk.Label(area, text="", bg=CREME, fg=TEXTO_SUAVE, font=fonte(10))
        mensagem.pack(anchor="w", pady=(0, 10))

        def atualizar_lista():
            lista_tarefas.delete(0, tk.END)

            tarefas = carregar()

            if not tarefas:
                lista_tarefas.insert(tk.END, "Nenhuma tarefa cadastrada")
                return

            for tarefa in tarefas:
                simbolo = "☑" if tarefa.get("Concluído", False) else "☐"
                nome = tarefa.get("tarefa", "Tarefa")
                lista_tarefas.insert(tk.END, f"  {simbolo}   {nome}")

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

        def editar():
            selecao = lista_tarefas.curselection()

            if not selecao:
                mensagem.config(text="Selecione uma tarefa para editar.")
                return

            indice = selecao[0]
            tarefas = carregar()

            if indice >= len(tarefas):
                return

            novo_nome = simpledialog.askstring(
                "Editar tarefa", "Novo texto da tarefa:",
                initialvalue=tarefas[indice].get("tarefa", ""),
                parent=janela
            )

            if novo_nome is None:
                return

            novo_nome = novo_nome.strip()

            if not novo_nome:
                mensagem.config(text="Digite o nome da tarefa.")
                return

            tarefas[indice]["tarefa"] = novo_nome

            try:
                salvar(tarefas)
                atualizar_lista()
                lista_tarefas.selection_set(indice)
                mensagem.config(text="Tarefa editada.")
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

        for texto, acao, cor in [
            ("Adicionar tarefa", adicionar, AZUL),
            ("Marcar / desmarcar", marcar, AZUL),
            ("Editar tarefa", editar, AZUL),
            ("Excluir tarefa", excluir_tarefa, VERMELHO),
        ]:
            tk.Button(
                botoes_checklist,
                text=texto,
                command=acao,
                font=fonte(10, "bold"),
                bg=cor,
                fg=BRANCO,
                relief="flat",
                borderwidth=0,
                highlightthickness=0,
                padx=16,
                pady=7,
                cursor="hand2"
            ).pack(side="left", padx=(0, 8))

        campo.bind("<Return>", lambda evento: adicionar())
        campo.focus_set()

        atualizar_lista()

    cabecalho = tk.Frame(menu, bg=AZUL)
    cabecalho.pack(fill="x", padx=18, pady=(26, 20))

    tk.Label(
        cabecalho, text="⛩", font=fonte(22), bg=AZUL, fg=VERMELHO
    ).pack(side="left", padx=(0, 10))

    titulos = tk.Frame(cabecalho, bg=AZUL)
    titulos.pack(side="left")

    tk.Label(
        titulos, text="Ponte Nippon",
        font=fonte(15, "bold"), bg=AZUL, fg=BRANCO
    ).pack(anchor="w")

    tk.Label(
        titulos, text="BRASIL   →   JAPÃO",
        font=fonte(8), bg=AZUL, fg=CINZA_AZULADO
    ).pack(anchor="w")

    for nome, simbolo, comando in [
        ("Início", "⌂", inicio),
        ("Dicionário", "▤", dicionario),
        ("Guia Cultural", "◉", guia),
        ("Checklist", "☑", checklist),
    ]:
        botao = tk.Button(
            menu, text=f"   {simbolo}    {nome}", command=comando,
            font=fonte(11), anchor="w", padx=12, pady=11,
            bg=AZUL, fg=BRANCO, activeforeground=BRANCO,
            activebackground=VERMELHO, relief="flat",
            borderwidth=0, highlightthickness=0, cursor="hand2"
        )
        botao.pack(fill="x", padx=14, pady=3)
        botoes[nome] = botao

    passos = tk.Frame(menu, bg=AZUL)
    passos.pack(side="bottom", fill="x", padx=20, pady=26)

    tk.Label(
        passos, text="\"Pequenos passos\ntambém te levam longe.\"",
        font=fonte(9), justify="left", bg=AZUL, fg=CINZA_AZULADO
    ).pack(anchor="w")

    tk.Label(
        passos, text="一歩ずつ、遠くへ",
        font=fonte(10), bg=AZUL, fg=ROSA_FORTE
    ).pack(anchor="w", pady=(6, 0))

    galho_sakura(menu, LARGURA_MENU, 150, AZUL).pack(side="bottom", fill="x")

    inicio()
    janela.mainloop()


if __name__ == "__main__":
    iniciar_aplicacao()
