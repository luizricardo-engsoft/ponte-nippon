import hashlib
import hmac
import json
import os
import tkinter as tk

ARQUIVO_USUARIOS = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "usuarios.json"
)

ITERACOES = 200_000
MAX_TENTATIVAS = 5
BLOQUEIO_SEGUNDOS = 30

AZUL = "#0B1F3A"
CREME = "#FAF6F0"
CINZA_AZULADO = "#DCE5ED"
COR_ERRO = "#B00020"
COR_SUCESSO = "#1B7F3B"


def gerar_hash(senha, salt=None):
    salt = salt or os.urandom(16)
    derivado = hashlib.pbkdf2_hmac("sha256", senha.encode("utf-8"), salt, ITERACOES)
    return f"{salt.hex()}:{derivado.hex()}"


def verificar_senha(senha, armazenado):
    try:
        salt_hex, hash_hex = armazenado.split(":")
        salt = bytes.fromhex(salt_hex)
    except (ValueError, AttributeError):
        return False

    derivado = hashlib.pbkdf2_hmac("sha256", senha.encode("utf-8"), salt, ITERACOES)
    return hmac.compare_digest(derivado.hex(), hash_hex)


def _hash_legado(senha):
    return hashlib.sha256(senha.encode("utf-8")).hexdigest()


def carregar_usuarios():
    if not os.path.exists(ARQUIVO_USUARIOS):
        return {}

    try:
        with open(ARQUIVO_USUARIOS, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
            return dados if isinstance(dados, dict) else {}
    except (json.JSONDecodeError, OSError):
        return {}


def salvar_usuarios(usuarios):
    temporario = ARQUIVO_USUARIOS + ".tmp"
    with open(temporario, "w", encoding="utf-8") as arquivo:
        json.dump(usuarios, arquivo, indent=4, ensure_ascii=False)
    os.replace(temporario, ARQUIVO_USUARIOS)


def autenticar(email, senha):
    usuarios = carregar_usuarios()
    armazenado = usuarios.get(email)

    if not isinstance(armazenado, str):
        return False

    if ":" in armazenado:
        return verificar_senha(senha, armazenado)

    if hmac.compare_digest(armazenado, _hash_legado(senha)):
        usuarios[email] = gerar_hash(senha)
        try:
            salvar_usuarios(usuarios)
        except OSError:
            pass
        return True

    return False


def email_valido(email):
    if "@" not in email:
        return False
    usuario, _, dominio = email.rpartition("@")
    return bool(usuario) and "." in dominio and not dominio.startswith(".") and not dominio.endswith(".")


def iniciar_login():
    janela = tk.Tk()
    janela.title("Ponte Nippon — Acesso")
    janela.geometry("400x370")
    janela.configure(bg=CREME)
    janela.resizable(False, False)

    estado = {"tentativas": 0, "bloqueado": False, "autenticado": False, "app": None}

    tk.Label(
        janela, text="Ponte Nippon",
        font=("Arial", 20, "bold"), bg=CREME, fg=AZUL
    ).pack(pady=(25, 5))

    tk.Label(
        janela, text="Entre ou crie sua conta", bg=CREME, fg=AZUL
    ).pack(pady=(0, 15))

    tk.Label(janela, text="E-mail", bg=CREME, fg=AZUL).pack()
    email_entry = tk.Entry(janela, width=32)
    email_entry.pack(pady=5)

    tk.Label(janela, text="Senha", bg=CREME, fg=AZUL).pack()
    senha_entry = tk.Entry(janela, width=32, show="*")
    senha_entry.pack(pady=5)

    mensagem = tk.Label(janela, text="", bg=CREME, wraplength=340)
    mensagem.pack(pady=8)

    def mostrar(texto, erro=True):
        mensagem.config(text=texto, fg=COR_ERRO if erro else COR_SUCESSO)

    def contagem_bloqueio(restante):
        if restante > 0:
            mostrar(f"Muitas tentativas. Aguarde {restante}s.")
            janela.after(1000, lambda: contagem_bloqueio(restante - 1))
        else:
            estado["bloqueado"] = False
            estado["tentativas"] = 0
            botao_entrar.config(state="normal")
            mostrar("Você já pode tentar novamente.", erro=False)

    def bloquear():
        estado["bloqueado"] = True
        botao_entrar.config(state="disabled")
        contagem_bloqueio(BLOQUEIO_SEGUNDOS)

    def cadastrar():
        email = email_entry.get().strip().lower()
        senha = senha_entry.get()

        if not email or not senha:
            mostrar("Preencha o e-mail e a senha.")
            return

        if not email_valido(email):
            mostrar("Digite um e-mail válido.")
            return

        if len(senha) < 6:
            mostrar("A senha deve ter pelo menos 6 caracteres.")
            return

        usuarios = carregar_usuarios()

        if email in usuarios:
            mostrar("Este e-mail já está cadastrado.")
            return

        usuarios[email] = gerar_hash(senha)

        try:
            salvar_usuarios(usuarios)
        except OSError:
            mostrar("Não foi possível salvar o cadastro.")
            return

        senha_entry.delete(0, tk.END)
        mostrar("Cadastro realizado! Agora entre na sua conta.", erro=False)

    def login(event=None):
        if estado["bloqueado"]:
            return

        email = email_entry.get().strip().lower()
        senha = senha_entry.get()

        if not email or not senha:
            mostrar("Preencha o e-mail e a senha.")
            return

        if not autenticar(email, senha):
            estado["tentativas"] += 1
            restantes = MAX_TENTATIVAS - estado["tentativas"]

            if restantes <= 0:
                bloquear()
            else:
                mostrar(f"E-mail ou senha incorretos. Tentativas restantes: {restantes}.")
            return

        try:
            from interface import iniciar_aplicacao
        except ImportError as erro:
            mostrar(f"Não foi possível abrir o sistema: {erro}")
            return

        estado["autenticado"] = True
        estado["app"] = iniciar_aplicacao
        janela.destroy()

    botao_entrar = tk.Button(
        janela, text="Entrar", command=login,
        bg=AZUL, fg="white", width=25
    )
    botao_entrar.pack(pady=4)

    tk.Button(
        janela, text="Criar conta", command=cadastrar,
        bg=CINZA_AZULADO, fg=AZUL, width=25
    ).pack(pady=4)

    janela.bind("<Return>", login)
    email_entry.focus_set()

    janela.mainloop()

    if estado["autenticado"] and estado["app"]:
        estado["app"]()


if __name__ == "__main__":
    iniciar_login()
