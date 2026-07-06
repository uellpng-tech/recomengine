import matplotlib.pyplot as plt
import tkinter as tk
import random as rd
import time as tm
import os
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

janela = tk.Tk()
janela.title("RecomEngine")
janela.geometry("900x600")
janela.iconbitmap("imagens/icones/logo.ico")
janela.configure(bg="#1e1e1e")

janela.grid_rowconfigure(0, weight=1)
janela.grid_columnconfigure(0, weight=1)  
janela.grid_columnconfigure(1, minsize=4) 
janela.grid_columnconfigure(2, weight=0, minsize=0)  

frame_esq = tk.Frame(janela, bg="#1e1e1e", bd=0, highlightthickness=0)
frame_esq.grid(row=0, column=0, sticky="nsew")

dividir = tk.Frame(janela, bg="#303030", width=4)
dividir.grid(row=0, column=1, sticky="ns")

frame_dir = tk.Frame(janela, bg="#2a2a2a", bd=0, highlightthickness=0)

frame_dir.grid(row=0, column=2, sticky="nsew")

frame_dir.grid_remove()

janela.grid_columnconfigure(2, weight=0, minsize=0)

mostrar_direita = False 

def esconder_direita():
    global mostrar_direita

    if mostrar_direita:
        frame_dir.grid_remove()
        dividir.grid_remove()

        janela.grid_columnconfigure(2, weight=0, minsize=0)

        btn_esconder.config(image=img_mostrar)
        btn_esconder.image = img_mostrar

        mostrar_direita = False
    else:
        frame_dir.grid(row=0, column=2, sticky="nsew")
        dividir.grid(row=0, column=1, sticky="ns")

        janela.grid_columnconfigure(2, weight=2)

        btn_esconder.config(image=img_esconder)
        btn_esconder.image = img_esconder

        mostrar_direita = True

img_mostrar = ImageTk.PhotoImage(Image.open("imagens/icones/esconderoff.png"))
img_esconder = ImageTk.PhotoImage(Image.open("imagens/icones/esconderon.png"))

frame_dir.grid(row=0, column=2, sticky="nsew")
frame_dir.grid_remove()
dividir.grid_remove()

frame_esq.grid_rowconfigure(0, weight=1)
frame_esq.grid_columnconfigure(0, weight=0)
frame_esq.grid_columnconfigure(1, weight=3)  
frame_esq.grid_columnconfigure(2, weight=0)

menu = tk.Frame(frame_esq, bg="#111111")
menu.grid(row=0, column=0, sticky="nsew")

btn_esconder = tk.Button(menu, image=img_esconder, command=esconder_direita, bd=0, highlightthickness=0, relief="flat", bg="#111111",  activebackground="#111111")
btn_esconder.image = img_esconder
btn_esconder.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

feed = tk.Frame(frame_esq, bg="#1e1e1e")
feed.grid(row=0, column=1, sticky="nsew", padx=20)
feed.grid_rowconfigure(0, weight=3) 

card = tk.Frame(feed, bg="#252525")
card.place(relx=0.5, rely=0.5, anchor="center", width=500, height=1010)

bloco = tk.Frame(card, bg="#252525")
bloco.place(x=0, y=205, width=500, height=590)

img_conteudo = tk.Label(bloco, bg="#131313")
img_conteudo.place(x=20, y=-30, relwidth=1, relheight=1, width=-40, height=50)

conteudo_atual = None

diretorio = "imagens/Tipos"
pastas_ignoradas = ["icones", "anuncios"]

def carregar_conteudos():
    conteudos = []

    for categoria in os.listdir(diretorio):
        if categoria in pastas_ignoradas:
            continue

        pasta = os.path.join(diretorio, categoria)

        if os.path.isdir(pasta):
            for img in os.listdir(pasta):
                caminho = os.path.join(pasta, img)

                conteudos.append({"img": caminho,"tags": [categoria]})

    return conteudos

canvas = None
fig = None
ax = None

grafico_framet = tk.Frame(frame_dir, bg="#202020")
grafico_framet.place(x=5, y=0)

def atualizar_graficot():
    global canvas, fig, ax

    for widget in grafico_framet.winfo_children():
        widget.destroy()
        
    fig, ax = plt.subplots(figsize=(9,4))

    tags = list(usuario.keys())
    valores = list(usuario.values())

    cores = ["#00ff88" if v >= 0 else "#ff4444" for v in valores]

    ax.barh(tags, valores, color=cores)

    ax.axvline(0, color="white", linewidth=1, alpha=0.3)

    ax.set_xlim(-10, 10)

    ax.set_title("Interesses do usuário", color="Gray")

    ax.set_facecolor("#2a2a2a")
    fig.patch.set_facecolor("#2a2a2a")

    ax.tick_params(colors="white")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#444")
    ax.spines["bottom"].set_color("#444")

    canvas = FigureCanvasTkAgg(fig, master=grafico_framet)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

    plt.close(fig)

atencao = {
    "Likes": 0,
    "Dislikes": 0,
    "Pulos": 0
}

frame_interacoes = tk.Frame(frame_dir, bg="#202020", width=500, height=240)
frame_interacoes.place(x=50, y=675)
frame_interacoes.pack_propagate(False)

canvas_interacoes = None
fig_i = None
ax_i = None

def mostrar_graficoi():
    global canvas_interacoes, fig_i, ax_i

    fig, ax = plt.subplots(figsize=(5, 3))

    nomes = ["Likes", "Dislikes", "Pulos"]
    valores = [
        atencao["Likes"],
        atencao["Dislikes"],
        atencao["Pulos"]
    ]

    if canvas_interacoes is None:

        fig_i, ax_i = plt.subplots(figsize=(5, 3))

        canvas_interacoes = FigureCanvasTkAgg(fig_i, master=frame_interacoes)
        canvas_interacoes.get_tk_widget().pack(fill="both", expand=True)

    ax_i.clear()

    bars = ax_i.barh(nomes, valores, color="#00ff88")

    ax_i.set_title("Interações", color="gray", pad=10)

    ax_i.set_facecolor("#2a2a2a")
    fig_i.patch.set_facecolor("#2a2a2a")

    ax_i.tick_params(colors="white")
    ax_i.set_xticks([])

    for spine in ax_i.spines.values():
        spine.set_visible(False)

    for bar in bars:
        valor = bar.get_width()

        if valor > 0:
            ax_i.text(
                valor / 2,
                bar.get_y() + bar.get_height() / 2,
                str(int(valor)),
                va="center",
                ha="center",
                color="white",
                fontweight="bold"
            )

    canvas_interacoes.draw()

conteudos = carregar_conteudos()

usuario = {
    "tecnologia": 0,
    "esporte" : 0,
    "games": 0,
    "educação": 0,
    "humor": 0,
    "animais": 0,
    "outros": 0
}

atualizar_graficot()

def score(conteudo):
    return sum(usuario.get(tag, 0) for tag in conteudo["tags"])

def tags_favoritas():

    maior = max(usuario.values())

    favoritas = []

    for tag, valor in usuario.items():

        if valor == maior:
            favoritas.append(tag)

    return favoritas

def reset_distribuicao():
    return {
        "Relacionados": 0,
        "Neutros": 0,
        "Fora do perfil": 0,
        "Random": 0
    }

distribuicao = reset_distribuicao()

frame_recomendacao = tk.Frame(frame_dir, bg="#202020", width=350, height=350)
frame_recomendacao.place(x=550, y=680)
frame_recomendacao.pack_propagate(False)

canvas_recomendacao = None
fig_r = None
ax_r = None

def grafico_recomendacao():
    global canvas_recomendacao, fig_r, ax_r

    pontos = {
        "Relacionados": (0, 1),
        "Neutros": (1, 0),
        "Fora": (0, -1),
        "Random": (-1, 0)  
    }

    cores = {
        "Relacionados": "#00ff88",
        "Neutros": "#ffaa00",
        "Fora": "#ff4444",
        "Random": "#2f00ff"
    }

    if canvas_recomendacao is None:
        fig_r, ax_r = plt.subplots(figsize=(3, 3))

        canvas_recomendacao = FigureCanvasTkAgg(fig_r, master=frame_recomendacao)
        canvas_recomendacao.get_tk_widget().pack(fill="both", expand=True)

    ax_r.clear()

    ax_r.axhline(0, color="gray", linewidth=2)
    ax_r.axvline(0, color="gray", linewidth=2)

    ax_r.text(0, 1.1, "Relacionados", color="white", ha="center", va="bottom")
    ax_r.text(1.1, 0, "Neutros", color="white", ha="left", va="center")
    ax_r.text(0, -1.1, "Fora", color="white", ha="center", va="top")
    ax_r.text(-1.1, 0, "Random", color="white", ha="right", va="center")

    for key, val in distribuicao.items():
        x, y = pontos.get(key, (0, 0))

        ax_r.scatter(x, y, s=val * 200 + 50, color=cores.get(key, "white"))

        ax_r.text(
            x, y,
            str(val),
            color="white",
            ha="center",
            va="center",
            fontweight="bold"
        )

    ax_r.set_xlim(-1.3, 1.3)
    ax_r.set_ylim(-1.3, 1.3)

    ax_r.set_facecolor("#2a2a2a")
    fig_r.patch.set_facecolor("#2a2a2a")

    ax_r.set_xticks([])
    ax_r.set_yticks([])

    for spine in ax_r.spines.values():
        spine.set_visible(False)

    ax_r.set_title("Distribuição do Algoritmo", color="gray", pad=15)

    canvas_recomendacao.draw()

historico = []

def recomendacao(conteudo):

    favoritas = tags_favoritas()

    relacionados = []
    outros = []

    for conteudo in conteudos:

        if conteudo not in historico:

            tem_favorito = False

            for tag in conteudo["tags"]:

                if tag.lower() in favoritas:
                    relacionados.append(conteudo)
                    tem_favorito = True
                    break
            if not tem_favorito:
                outros.append(conteudo)

    chance = rd.random()

    if relacionados and chance < 0.65:
        escolhido = rd.choice(relacionados)
        distribuicao["Relacionados"] += 1

    elif outros and chance < 0.9:
        escolhido = rd.choice(outros)
        distribuicao["Neutros"] += 1

    elif outros:
        escolhido = rd.choice(conteudos)
        distribuicao["Fora do perfil"] += 1

    else:
        escolhido = rd.choice(conteudos)
        distribuicao["Random"] += 1

    return escolhido

curtiu = False
ja_curtiu = False
deslike_ativo = False

deslike_img = Image.open("imagens/icones/deslike.png")
deslike_img = deslike_img.resize((50, 50))
deslike_icone = ImageTk.PhotoImage(deslike_img)

def atualizar_dashboard():
    atualizar_graficot()
    mostrar_anuncio()
    mostrar_graficoi()
    grafico_recomendacao()

def mostrar_conteudo():
    global foto, conteudo_atual, curtiu, ja_curtiu, deslike_img

    curtiu = False
    ja_curtiu = False
    btn_curtir.config(image=curtir_icone)

    deslike_ativo = False
    btn_deslike.config(image=deslike_icone)

    conteudo_atual = recomendacao(conteudos)

    img = Image.open(conteudo_atual["img"])

    w = 400
    h = 500

    img = img.resize((w, h), Image.LANCZOS)

    foto = ImageTk.PhotoImage(img)

    img_conteudo.config(image=foto)
    img_conteudo.image = foto

    atualizar_dashboard()

curtido_img = Image.open("imagens/icones/curtido.png")
curtido_img = curtido_img.resize((50, 50))
curtido_icone = ImageTk.PhotoImage(curtido_img) 

def curtir(conteudo):
    global curtiu, ja_curtiu, deslike_ativo

    if deslike_ativo:

        deslike_ativo = False

        btn_deslike.config(image=deslike_icone)
        btn_deslike.image = deslike_icone

        atencao["Dislikes"] = max(0, atencao["Dislikes"] - 1)

        for tag in conteudo["tags"]:
            usuario[tag] += 2


    curtiu = True
    
    if not ja_curtiu:

        ja_curtiu = True

        btn_curtir.config(image=curtido_icone)

        atencao["Likes"] += 1

        for tag in conteudo["tags"]:
            usuario[tag] += 1

        
    else:

        ja_curtiu = False

        btn_curtir.config(image=curtir_icone)

        atencao["Likes"] = max(0, atencao["Likes"] - 1)

        for tag in conteudo["tags"]:
            usuario[tag] -= 1

    atualizar_graficot()

desliker_img = Image.open("imagens/icones/remover.png")
desliker_img = desliker_img.resize((50, 50))
desliker_icone = ImageTk.PhotoImage(desliker_img) 

def deslike(conteudo):
    global deslike_ativo, ja_curtiu

    if ja_curtiu:

        ja_curtiu = False

        btn_curtir.config(image=curtir_icone)
        btn_curtir.image = curtir_icone

        atencao["Likes"] = max(0, atencao["Likes"] - 1)

        for tag in conteudo["tags"]:
            usuario[tag] -= 1

        

    if not deslike_ativo:

        deslike_ativo = True

        btn_deslike.config(image=desliker_icone)

        atencao["Dislikes"] += 1

        for tag in conteudo["tags"]:
            usuario[tag] -= 2

        

    else:

        deslike_ativo = False

        btn_deslike.config(image=deslike_icone)

        atencao["Dislikes"] = max(0, atencao["Dislikes"] - 1)

        for tag in conteudo["tags"]:
            usuario[tag] += 2

    atualizar_graficot()

def pular(conteudo):
    global curtiu, deslike_ativo, ja_curtiu

    atencao["Pulos"] += 1
    mostrar_graficoi()

    curtiu = False
    ja_curtiu = False
    deslike_ativo = False

    if not curtiu and not deslike_ativo:

        for tag in conteudo["tags"]:
            usuario[tag] = max(-5, usuario[tag] - 0.3)

    atualizar_graficot()
    mostrar_conteudo()

curtir_img = Image.open("imagens/icones/curtir.png")
curtir_img = curtir_img.resize((50, 50))
curtir_icone = ImageTk.PhotoImage(curtir_img)

btn_curtir = tk.Button(bloco, image=curtir_icone, bd=0, bg="#131313", activebackground="#131313", command=lambda: curtir(conteudo_atual))
btn_curtir.image = curtir_icone
btn_curtir.place(x=157, y=540)

btn_deslike = tk.Button(bloco, image=deslike_icone, bd=0, bg="#131313", activebackground="#131313", command=lambda: deslike(conteudo_atual))
btn_deslike.image = deslike_icone
btn_deslike.place(x=225, y=540)

pular_img = Image.open("imagens/icones/pular.png")
pular_img = pular_img.resize((50, 50))
pular_icone = ImageTk.PhotoImage(pular_img)

btn_pular = tk.Button(bloco, image=pular_icone, bd=0, bg="#131313", command=lambda: pular(conteudo_atual), activebackground="#131313")
btn_pular.image = pular_icone
btn_pular.place(x=295, y=540)

anuncios = [
    {"img": "imagens/anuncios/games/Controle.png", "tags": ["games"]},
    {"img": "imagens/anuncios/games/Mouse.png", "tags": ["games"]},
    {"img": "imagens/anuncios/games/Teclado.png", "tags": ["games"]},
    {"img": "imagens/anuncios/tecnologia/Cartão.png", "tags": ["tecnologia"]},
    {"img": "imagens/anuncios/tecnologia/Livro.png", "tags": ["tecnologia"]},
    {"img": "imagens/anuncios/tecnologia/mousepad.png", "tags": ["tecnologia"]},
    {"img": "imagens/anuncios/educacao/EVA.png", "tags": ["educacao"]},
    {"img": "imagens/anuncios/animais/animais.png", "tags": ["animais"]},
    {"img": "imagens/anuncios/humor/Chinelo.png", "tags": ["humor"]},
    {"img": "imagens/anuncios/esporte/Bola.png", "tags": ["esporte"]},
]

def top_tags():
    ordenado = sorted(usuario.items(), key=lambda x: x[1], reverse=True)
    return ordenado[:3]

def score_ad(ad, tags_user):
    return sum(1 for t in ad["tags"] if t in tags_user)

def escolher_anuncio():
    tops = top_tags()

    melhor_ad = None
    melhor_score = -1

    for ad in anuncios:

        score = 0

        for tag, valor in tops:

            if tag in ad["tags"]:
                score += valor  # peso real do usuário

        if score > melhor_score:
            melhor_score = score
            melhor_ad = ad

    return melhor_ad if melhor_ad else rd.choice(anuncios)

ad_label = None

def mostrar_anuncio():
    global ad_label

    ad = escolher_anuncio()

    img = Image.open(ad["img"])
    img = img.resize((250, 180), Image.LANCZOS)

    foto = ImageTk.PhotoImage(img)

    if ad_label is not None:
        ad_label.config(image=foto)
        ad_label.image = foto
    else:
        ad_label = tk.Label(frame_dir, image=foto, bg="#2a2a2a")
        ad_label.image = foto
        ad_label.place(x=350, y=450)

def atualizar_dashboard():
    atualizar_graficot()
    mostrar_anuncio()
    atualizar_top3()
    mostrar_graficoi()
    grafico_recomendacao()

def atualizar_top3():
    ordenado = sorted(usuario.items(), key=lambda x: x[1], reverse=True)
    tops = ordenado[:3]

    labels = [top1, top2, top3]

    for i in range(3):
        if i < len(tops):
            tag = tops[i][0]
            labels[i].config(text=f"{i+1}º {tag}")
        else:
            labels[i].config(text="")

top_frame = tk.Frame(frame_dir, bg="#2a2a2a")
top_frame.place(x=150, y=470)

top1 = tk.Label(top_frame, text="", bg="#2a2a2a", fg="white", font=("Arial", 18, "bold"))
top1.pack(anchor="w")

top2 = tk.Label(top_frame, text="", bg="#2a2a2a", fg="white", font=("Arial", 18))
top2.pack(anchor="w")

top3 = tk.Label(top_frame, text="", bg="#2a2a2a", fg="white", font=("Arial", 18))
top3.pack(anchor="w")

titulo = tk.Label(frame_dir, text="Recomendações de Anuncios", fg="gray", bg="#2a2a2a", font=("", 14))
titulo.place(x=340, y=400)

janela.after(100, mostrar_conteudo)

janela.mainloop()