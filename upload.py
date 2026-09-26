#!/usr/bin/env python3

import os
import requests

# Pasta onde ficam as imagens
PASTA_UPLOADS = os.path.expanduser("~/uploads")

# Extensões permitidas
EXTENSOES = (
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".gif"
)

# API do Catbox
URL_UPLOAD = "https://catbox.moe/user/api.php"


def listar_imagens():
    os.makedirs(PASTA_UPLOADS, exist_ok=True)

    arquivos = []

    for nome in os.listdir(PASTA_UPLOADS):
        caminho = os.path.join(PASTA_UPLOADS, nome)

        if os.path.isfile(caminho):
            if nome.lower().endswith(EXTENSOES):
                arquivos.append(caminho)

    arquivos.sort()

    return arquivos


def escolher_imagem(arquivos):

    print()
    print("📁 IMAGENS DISPONÍVEIS")
    print("-" * 40)

    for i, caminho in enumerate(arquivos, 1):

        nome = os.path.basename(caminho)

        tamanho = os.path.getsize(caminho)
        tamanho_mb = tamanho / (1024 * 1024)

        print(f"[{i}] {nome} ({tamanho_mb:.2f} MB)")

    print("-" * 40)

    while True:

        escolha = input("Digite o número da imagem: ").strip()

        try:

            numero = int(escolha)

            if 1 <= numero <= len(arquivos):
                return arquivos[numero - 1]

            print("❌ Número inválido.")

        except ValueError:

            print("❌ Digite apenas um número.")


def fazer_upload(caminho):

    nome = os.path.basename(caminho)

    print()
    print(f"⬆️ Enviando: {nome}")
    print()

    try:

        with open(caminho, "rb") as arquivo:

            arquivos = {
                "fileToUpload": (
                    nome,
                    arquivo,
                    "application/octet-stream"
                )
            }

            dados = {
                "reqtype": "fileupload"
            }

            resposta = requests.post(
                URL_UPLOAD,
                data=dados,
                files=arquivos,
                timeout=120
            )

        if resposta.status_code == 200:

            url = resposta.text.strip()

            if url.startswith("http"):

                return url

        print("❌ O servidor não aceitou o upload.")
        print()
        print("Código:", resposta.status_code)
        print("Resposta:", resposta.text)

        return None

    except requests.RequestException as erro:

        print()
        print("❌ Erro durante o upload:")
        print(erro)

        return None

    except Exception as erro:

        print()
        print("❌ Erro inesperado:")
        print(erro)

        return None


def main():

    print()
    print("=" * 45)
    print("        📤 UPLOAD DE IMAGENS")
    print("=" * 45)

    imagens = listar_imagens()

    if not imagens:

        print()
        print("❌ Nenhuma imagem encontrada.")
        print()
        print("Coloque uma imagem em:")
        print(PASTA_UPLOADS)
        print()

        return

    imagem = escolher_imagem(imagens)

    url = fazer_upload(imagem)

    if url:

        print("=" * 45)
        print("✅ UPLOAD CONCLUÍDO!")
        print("=" * 45)

        print()
        print("📄 Arquivo:")
        print(os.path.basename(imagem))

        print()
        print("🔗 URL:")
        print(url)

        print()
        print("=" * 45)

    else:

        print()
        print("❌ Não foi possível fazer o upload.")


if __name__ == "__main__":
    main()
