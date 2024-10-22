import os

import barcode
from barcode.writer import ImageWriter
from PIL import Image, ImageDraw
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


# Função para gerar código de barras
def gerar_codigo_barra(data, output_file):
    codigo_barra = barcode.get("code128", data, writer=ImageWriter())
    file_path = codigo_barra.save(output_file)
    return file_path  # Retorna o caminho sem adicionar ".png" novamente


# Função para redimensionar imagens
def redimensionar_imagem(imagem, largura_desejada, altura_desejada):
    img = Image.open(imagem)
    img = img.resize(
        (int(largura_desejada), int(altura_desejada)), Image.Resampling.LANCZOS
    )  # Garantir que as dimensões sejam inteiros
    img.save(imagem)
    return imagem


# Função para gerar a página com os códigos de barras
def gerar_pagina_pdf(codigos, output_pdf):
    c = canvas.Canvas(output_pdf, pagesize=A4)
    largura, altura = A4
    x_offset = 50
    y_offset = altura - 100
    max_codigos_por_linha = 3

    # Definir tamanho dos códigos de barras
    largura_codigo = (
        largura - 100
    ) // max_codigos_por_linha  # margem total de 100 (50 de cada lado)
    altura_codigo = (
        largura_codigo // 2
    )  # Proporção de altura para manter o formato

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


# Função para pedir dados e gerar códigos de barras
def solicitar_dados():
    dados = []
    while True:
        dado = input(
            "Insira o código de barras (ou pressione Enter para finalizar): "
        )
        if not dado:
            break
        dados.append(dado)
    return dados


# Programa principal
if __name__ == "__main__":
    dados = solicitar_dados()
    if dados:
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

        print("PDF gerado com sucesso!")
    else:
        print("Nenhum dado inserido.")
