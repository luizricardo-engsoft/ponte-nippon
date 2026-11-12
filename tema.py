import math
import random
import tkinter as tk
from tkinter import font as tkfont

AZUL = "#0B1F44"
AZUL_CLARO = "#EDF1F8"
VERMELHO = "#E63946"
ROSA = "#FADADD"
ROSA_FORTE = "#F2A3B3"
CREME = "#FAF9F6"
BRANCO = "#FFFFFF"
CINZA_AZULADO = "#DCE5ED"
BORDA = "#E6E3DE"
TEXTO_SUAVE = "#5A6A82"
COR_ERRO = "#B00020"
COR_SUCESSO = "#1B7F3B"

CEU_INICIO = "#FFFFFF"
CEU_FIM = "#FCE9EE"
MONTANHA_TOPO = "#D7E0EE"
MONTANHA_BASE = "#A9BBD6"
MONTANHA_FUNDO = "#E4EAF4"
NEVE = "#FFFFFF"
SOL = "#E8505F"
SOL_BRILHO = "#F6BFC6"
GALHO = "#8A6E60"

FRACAO_NEVE = 0.30
SAKURA_TONS = ("#FFE2EA", "#FBCBD9", "#F6B3C7")
SAKURA_MIOLO = "#F4A0B6"
IPE_TONS = ("#F3A8C6", "#E87FAE", "#DC5F99")

PREFERIDAS = ("Montserrat", "Segoe UI", "Helvetica", "Arial")

_familia = None


def familia():
    global _familia

    if _familia is None:
        disponiveis = tkfont.families()
        _familia = "Arial"

        for nome in PREFERIDAS:
            if nome in disponiveis:
                _familia = nome
                break

    return _familia


def fonte(tamanho, peso="normal"):
    return (familia(), tamanho, peso)


def misturar(cor_a, cor_b, proporcao):
    canal_a = (int(cor_a[1:3], 16), int(cor_a[3:5], 16), int(cor_a[5:7], 16))
    canal_b = (int(cor_b[1:3], 16), int(cor_b[3:5], 16), int(cor_b[5:7], 16))

    return "#%02x%02x%02x" % tuple(
        int(a + (b - a) * proporcao) for a, b in zip(canal_a, canal_b)
    )


def retangulo_arredondado(canvas, x1, y1, x2, y2, raio, **opcoes):
    pontos = [
        x1 + raio, y1, x2 - raio, y1, x2, y1,
        x2, y1 + raio, x2, y2 - raio, x2, y2,
        x2 - raio, y2, x1 + raio, y2, x1, y2,
        x1, y2 - raio, x1, y1 + raio, x1, y1,
    ]
    return canvas.create_polygon(pontos, smooth=True, **opcoes)


def gradiente(canvas, largura, altura, inicio, fim, passo=3):
    for x in range(0, largura, passo):
        cor = misturar(inicio, fim, min(1.0, x / max(1, largura - passo)))
        canvas.create_rectangle(x, 0, x + passo, altura, fill=cor, outline=cor)


def _petala(canvas, x, y, raio, angulo, cor):
    contorno = (
        (0.0, 0.0), (0.52, -0.52), (0.40, -1.30),
        (0.0, -1.58), (-0.40, -1.30), (-0.52, -0.52),
    )
    cosseno = math.cos(angulo)
    seno = math.sin(angulo)
    pontos = []

    for px, py in contorno:
        pontos += [
            x + (px * cosseno - py * seno) * raio,
            y + (px * seno + py * cosseno) * raio,
        ]

    canvas.create_polygon(pontos, fill=cor, outline=cor, smooth=True)


def _flor_sakura(canvas, x, y, raio, cor):
    for i in range(5):
        _petala(canvas, x, y, raio, i * 2 * math.pi / 5, cor)

    miolo = raio * 0.20
    canvas.create_oval(
        x - miolo, y - miolo, x + miolo, y + miolo,
        fill=SAKURA_MIOLO, outline=SAKURA_MIOLO
    )


def _cacho_ipe(canvas, x, y, raio, sorteio):
    for _ in range(10):
        dx = sorteio.uniform(-raio, raio)
        dy = sorteio.uniform(-raio * 0.75, raio * 0.75)
        tamanho = raio * sorteio.uniform(0.30, 0.55)
        cor = sorteio.choice(IPE_TONS)
        canvas.create_oval(
            x + dx - tamanho, y + dy - tamanho,
            x + dx + tamanho, y + dy + tamanho,
            fill=cor, outline=cor
        )


def _ramo(canvas, pontos, largura):
    for i in range(len(pontos) - 1):
        (x1, y1), (x2, y2) = pontos[i], pontos[i + 1]
        espessura = max(1, int(largura - i * 0.9))
        canvas.create_line(
            x1, y1, x2, y2, fill=GALHO,
            width=espessura, capstyle="round"
        )


def _ramo_sakura(canvas, pontos, sorteio, quantidade=26, raio=7):
    _ramo(canvas, pontos, 4)

    for _ in range(quantidade):
        base = sorteio.choice(pontos)
        x = base[0] + sorteio.uniform(-28, 28)
        y = base[1] + sorteio.uniform(-20, 20)
        _flor_sakura(
            canvas, x, y,
            raio * sorteio.uniform(0.6, 1.25),
            sorteio.choice(SAKURA_TONS)
        )


def _ramo_ipe(canvas, pontos, sorteio, quantidade=22, raio=13):
    _ramo(canvas, pontos, 4)

    for _ in range(quantidade):
        base = sorteio.choice(pontos)
        x = base[0] + sorteio.uniform(-26, 26)
        y = base[1] + sorteio.uniform(-18, 18)
        _cacho_ipe(canvas, x, y, raio * sorteio.uniform(0.55, 1.1), sorteio)


def _monte(canvas, centro_x, base_y, largura, altura, cor_topo, cor_base, faixas=44):
    meia = largura / 2

    for i in range(faixas):
        alto = i / faixas
        baixo = (i + 1) / faixas
        cor = misturar(cor_topo, cor_base, alto)
        largura_alto = meia * (alto ** 1.45)
        largura_baixo = meia * (baixo ** 1.45)

        canvas.create_polygon(
            centro_x - largura_alto, base_y - altura * (1 - alto),
            centro_x + largura_alto, base_y - altura * (1 - alto),
            centro_x + largura_baixo, base_y - altura * (1 - baixo),
            centro_x - largura_baixo, base_y - altura * (1 - baixo),
            fill=cor, outline=cor
        )


def _neve(canvas, centro_x, topo_y, altura, meia):
    bordas = ((0.34, 0.50), (0.58, 0.92), (0.76, 0.66), (1.0, 1.0))
    pontos = [centro_x, topo_y]

    for fator_x, fator_y in bordas:
        pontos += [centro_x + meia * fator_x, topo_y + altura * fator_y]

    for fator_x, fator_y in reversed(bordas):
        pontos += [centro_x - meia * fator_x, topo_y + altura * fator_y]

    canvas.create_polygon(pontos, fill=NEVE, outline=NEVE, smooth=True)


def _sol(canvas, x, y, raio, cor_ceu, aneis=18):
    for i in range(aneis, 0, -1):
        distancia = i / aneis
        atual = raio * (1 + 1.15 * distancia)
        cor = misturar(SOL_BRILHO, cor_ceu, distancia ** 0.75)
        canvas.create_oval(
            x - atual, y - atual, x + atual, y + atual,
            fill=cor, outline=cor
        )

    canvas.create_oval(x - raio, y - raio, x + raio, y + raio, fill=SOL, outline=SOL)


def _torii(canvas, centro_x, base_y, largura, altura, cor):
    meia = largura / 2
    topo = base_y - altura
    espessura = largura * 0.085
    recuo = largura * 0.030
    base_pilar = meia * 0.64
    sob_viga = topo + altura * 0.175
    nuki = topo + altura * 0.42

    for lado in (-1, 1):
        x_base = centro_x + lado * base_pilar
        x_topo = centro_x + lado * (base_pilar - recuo)
        canvas.create_polygon(
            x_base - espessura / 2, base_y,
            x_base + espessura / 2, base_y,
            x_topo + espessura / 2, sob_viga,
            x_topo - espessura / 2, sob_viga,
            fill=cor, outline=cor
        )

    canvas.create_rectangle(
        centro_x - largura * 0.025, sob_viga,
        centro_x + largura * 0.025, nuki,
        fill=cor, outline=cor
    )
    canvas.create_rectangle(
        centro_x - meia * 0.80, nuki,
        centro_x + meia * 0.80, nuki + altura * 0.060,
        fill=cor, outline=cor
    )
    canvas.create_rectangle(
        centro_x - meia * 0.90, topo + altura * 0.115,
        centro_x + meia * 0.90, sob_viga,
        fill=cor, outline=cor
    )

    canvas.create_polygon(
        centro_x - meia, topo,
        centro_x - meia * 0.45, topo + altura * 0.045,
        centro_x, topo + altura * 0.055,
        centro_x + meia * 0.45, topo + altura * 0.045,
        centro_x + meia, topo,
        centro_x + meia, topo + altura * 0.058,
        centro_x + meia * 0.45, topo + altura * 0.100,
        centro_x, topo + altura * 0.112,
        centro_x - meia * 0.45, topo + altura * 0.100,
        centro_x - meia, topo + altura * 0.058,
        fill=cor, outline=cor, smooth=True
    )


def _petalas_ao_vento(canvas, largura, altura, sorteio, evitar, quantidade=16):
    centro_x, centro_y, raio_livre = evitar

    for _ in range(quantidade):
        x = sorteio.uniform(largura * 0.42, largura)
        y = sorteio.uniform(altura * 0.18, altura * 0.88)

        if math.hypot(x - centro_x, y - centro_y) < raio_livre:
            continue

        _petala(
            canvas, x, y,
            sorteio.uniform(3.0, 5.5),
            sorteio.uniform(0, 2 * math.pi),
            sorteio.choice(SAKURA_TONS)
        )


def desenhar_banner(parent, largura, altura, titulo, destaque, subtitulo):
    canvas = tk.Canvas(parent, width=largura, height=altura, highlightthickness=0)
    sorteio = random.Random(11)

    gradiente(canvas, largura, altura, CEU_INICIO, CEU_FIM)

    _monte(canvas, largura * 0.52, altura, largura * 0.30, altura * 0.42,
           MONTANHA_FUNDO, misturar(MONTANHA_FUNDO, MONTANHA_BASE, 0.35))
    sol_x = largura * 0.715
    sol_y = altura * 0.30
    _sol(canvas, sol_x, sol_y, 34, misturar(CEU_INICIO, CEU_FIM, 0.715))

    centro_fuji = largura * 0.66
    altura_fuji = altura * 0.64
    meia_fuji = largura * 0.40 / 2
    _monte(canvas, centro_fuji, altura, largura * 0.40, altura_fuji,
           MONTANHA_TOPO, MONTANHA_BASE)
    _neve(canvas, centro_fuji, altura - altura_fuji,
          altura_fuji * FRACAO_NEVE, meia_fuji * (FRACAO_NEVE ** 1.45))

    _torii(canvas, largura * 0.895, altura - 6, 80, altura * 0.50, AZUL)

    _ramo_ipe(canvas, [
        (largura * 0.40, -16), (largura * 0.44, altura * 0.05),
        (largura * 0.49, altura * 0.11), (largura * 0.54, altura * 0.13),
    ], sorteio, quantidade=18, raio=11)

    _ramo_sakura(canvas, [
        (largura * 1.03, altura * 0.03), (largura * 0.96, altura * 0.09),
        (largura * 0.89, altura * 0.07), (largura * 0.82, altura * 0.12),
    ], sorteio, quantidade=24)

    _petalas_ao_vento(canvas, largura, altura, sorteio, (sol_x, sol_y, 80))

    canvas.create_text(44, altura * 0.30, text=titulo, anchor="w",
                       fill=AZUL, font=fonte(19))
    canvas.create_text(44, altura * 0.50, text=destaque, anchor="w",
                       fill=AZUL, font=fonte(30, "bold"))
    canvas.create_text(44, altura * 0.76, text=subtitulo, anchor="w",
                       fill=TEXTO_SUAVE, font=fonte(12), justify="left")

    return canvas


def quadrado_icone(parent, simbolo, cor_fundo, cor_simbolo, cor_cartao=BRANCO, lado=54):
    canvas = tk.Canvas(
        parent, width=lado, height=lado,
        bg=cor_cartao, highlightthickness=0
    )
    retangulo_arredondado(canvas, 2, 2, lado - 2, lado - 2, 14,
                          fill=cor_fundo, outline=cor_fundo)
    canvas.create_text(lado / 2, lado / 2, text=simbolo,
                       fill=cor_simbolo, font=fonte(21, "bold"))
    return canvas


def galho_sakura(parent, largura, altura, cor_fundo):
    canvas = tk.Canvas(
        parent, width=largura, height=altura,
        bg=cor_fundo, highlightthickness=0
    )
    sorteio = random.Random(5)

    _ramo_ipe(canvas, [
        (-10, altura * 0.98), (largura * 0.22, altura * 0.80),
        (largura * 0.40, altura * 0.70),
    ], sorteio, quantidade=10, raio=11)

    _ramo_sakura(canvas, [
        (largura * 0.40, altura * 0.70), (largura * 0.62, altura * 0.48),
        (largura * 0.84, altura * 0.26),
    ], sorteio, quantidade=14, raio=7)

    return canvas


def cabecalho_login(parent, largura, altura):
    canvas = tk.Canvas(parent, width=largura, height=altura, highlightthickness=0)
    sorteio = random.Random(3)

    gradiente(canvas, largura, altura, CEU_INICIO, CEU_FIM)

    centro = largura * 0.30
    alto = altura * 0.56
    _monte(canvas, centro, altura, largura * 0.52, alto, MONTANHA_TOPO, MONTANHA_BASE)
    _neve(canvas, centro, altura - alto, alto * FRACAO_NEVE,
          largura * 0.52 / 2 * (FRACAO_NEVE ** 1.45))

    _torii(canvas, largura * 0.72, altura - 4, 58, altura * 0.46, AZUL)

    _ramo_ipe(canvas, [
        (largura * 0.06, -12), (largura * 0.12, altura * 0.14),
    ], sorteio, quantidade=7, raio=10)

    _ramo_sakura(canvas, [
        (largura * 1.02, altura * 0.08), (largura * 0.90, altura * 0.16),
    ], sorteio, quantidade=10, raio=6)

    return canvas
