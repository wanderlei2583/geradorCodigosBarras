import os
import tkinter as tk
from tkinter import messagebox

import barcode
from barcode.writer import ImageWriter
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


# Função para gerar código de barras
def gerar_codigo_barra(data, output_file):
    codigo_barra = barcode.get("code128", data, writer=ImageWriter())
    file_path = codigo_barra.save(output_file)
    return file_path


# Função para redimensionar imagens
def redimensionar_imagem(imagem, largura_desejada, altura_desejada):
    img = Image.open(imagem)
    img = img.resize(
        (int(largura_desejada), int(altura_desejada)), Image.Resampling.LANCZOS
    )
    img.save(imagem)
    return imagem


# Função para gerar a página com os códigos de barras
def gerar_pagina_pdf(codigos, output_pdf):
    c = canvas.Canvas(output_pdf, pagesize=A4)
    largura, altura = A4
    x_offset = 50
    y_offset = altura - 100
    max_codigos_por_linha = 3

    largura_codigo = (largura - 100) // max_codigos_por_linha
    altura_codigo = largura_codigo // 2

    for idx, codigo in enumerate(codigos):
        codigo = redimensionar_imagem(codigo, largura_codigo, altura_codigo)
        img = Image.open(codigo)
        img_width, img_height = img.size

        if idx % max_codigos_por_linha == 0 and idx != 0:
            y_offset -= img_height + 20
            x_offset = 50

        c.drawImage(
            codigo, x_offset, y_offset, width=img_width, height=img_height
        )
        x_offset += img_width + 20

    c.showPage()
    c.save()


# Função para gerar o PDF a partir dos códigos inseridos
def gerar_pdf():
    dados = entrada_codigos.get("1.0", tk.END).strip().split("\n")
    if not dados or dados == [""]:
        messagebox.showerror("Erro", "Insira pelo menos um código.")
        return

    imagens_codigos = []
    for idx, dado in enumerate(dados):
        file_name = f"codigo_barra_{idx}"
        caminho_imagem = gerar_codigo_barra(dado, file_name)
        imagens_codigos.append(caminho_imagem)

    # Gerar o PDF
    gerar_pagina_pdf(imagens_codigos, "codigos_barra.pdf")

    # Limpar os arquivos de imagem temporários
    for img in imagens_codigos:
        os.remove(img)

    messagebox.showinfo("Sucesso", "PDF gerado com sucesso!")


# Configuração da interface gráfica
root = tk.Tk()
root.title("Gerador de Códigos de Barras")

# Criação do campo de entrada para os códigos
entrada_codigos = tk.Text(root, height=15, width=50)
entrada_codigos.pack(pady=10)

# Botão para gerar o PDF
botao_gerar_pdf = tk.Button(root, text="Gerar PDF", command=gerar_pdf)
botao_gerar_pdf.pack(pady=10)

# Iniciar o loop da interface gráfica
root.mainloop()
