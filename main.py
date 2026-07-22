from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import glob

# Cria a instância da aplicação FastAPI, que será usada para gerenciar as rotas e o servidor.
app = FastAPI()

# Configure o middleware CORS para aceitar requisições de qualquer origem
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Defina caminhos absolutos para a pasta de imagens
PASTA_BASE = os.path.dirname(os.path.abspath(__file__))
PASTA_IMAGENS = os.path.join(PASTA_BASE, "figurinhas")

# Lista das 30 figurinhas do álbum de acordo com a numeração de slots no frontend (index.html).
# O 'id' corresponde ao slot no HTML. O 'imagem_url' aponta para a rota da imagem física correspondente.
# Como alguns personagens estão sem imagens no projeto (Jinbe no ID 10 e Fujitora no ID 19), eles estão comentados.
figurinhas = [
    {
        "id": 1,
        "nome": "Monkey D. Luffy",
        "categoria": "Chapéu de Palha",
        "imagem_url": "/figurinhas/1/imagem"
    },
    {
        "id": 2,
        "nome": "Roronoa Zoro",
        "categoria": "Chapéu de Palha",
        "imagem_url": "/figurinhas/2/imagem"
    },
    {
        "id": 3,
        "nome": "Nami",
        "categoria": "Chapéu de Palha",
        "imagem_url": "/figurinhas/3/imagem"
    },
    {
        "id": 4,
        "nome": "Usopp",
        "categoria": "Chapéu de Palha",
        "imagem_url": "/figurinhas/4/imagem"
    },
    {
        "id": 5,
        "nome": "Sanji",
        "categoria": "Chapéu de Palha",
        "imagem_url": "/figurinhas/5/imagem"
    },
    {
        "id": 6,
        "nome": "Tony Tony Chopper",
        "categoria": "Chapéu de Palha",
        "imagem_url": "/figurinhas/6/imagem"
    },
    {
        "id": 7,
        "nome": "Nico Robin",
        "categoria": "Chapéu de Palha",
        "imagem_url": "/figurinhas/7/imagem"
    },
    {
        "id": 8,
        "nome": "Franky",
        "categoria": "Chapéu de Palha",
        "imagem_url": "/figurinhas/8/imagem"
    },
    {
        "id": 9,
        "nome": "Brook",
        "categoria": "Chapéu de Palha",
        "imagem_url": "/figurinhas/9/imagem"
    },
    # O ID 10 (Jinbe) está comentado porque não há imagem dele na pasta física original
    # {
    #     "id": 10,
    #     "nome": "Jinbe",
    #     "categoria": "Chapéu de Palha",
    #     "imagem_url": "/figurinhas/10/imagem"
    # },
    {
        "id": 11,
        "nome": "Imu",
        "categoria": "Governo Mundial",
        "imagem_url": "/figurinhas/10/imagem"
    },
    {
        "id": 12,
        "nome": "Saint Garling Figarland",
        "categoria": "Governo Mundial",
        "imagem_url": "/figurinhas/11/imagem"
    },
    {
        "id": 13,
        "nome": "Saint Shamrock Figarland",
        "categoria": "Governo Mundial",
        "imagem_url": "/figurinhas/12/imagem"
    },
    {
        "id": 14,
        "nome": "Gunko",
        "categoria": "Governo Mundial",
        "imagem_url": "/figurinhas/13/imagem"
    },
    {
        "id": 15,
        "nome": "Akainu (Sakazuki)",
        "categoria": "Marinha",
        "imagem_url": "/figurinhas/15/imagem"
    },
    {
        "id": 16,
        "nome": "Kizaru (Borsalino)",
        "categoria": "Marinha",
        "imagem_url": "/figurinhas/16/imagem"
    },
    {
        "id": 17,
        "nome": "Aokiji (Kuzan)",
        "categoria": "Marinha",
        "imagem_url": "/figurinhas/17/imagem"
    },
    {
        "id": 18,
        "nome": "Ryokugyu (Aramaki)",
        "categoria": "Marinha",
        "imagem_url": "/figurinhas/18/imagem"
    },
    # O ID 19 (Fujitora / Issho) está comentado porque não há imagem dele na pasta física original
    # {
    #     "id": 19,
    #     "nome": "Fujitora (Issho)",
    #     "categoria": "Marinha",
    #     "imagem_url": "/figurinhas/19/imagem"
    # },
    {
        "id": 20,
        "nome": "Saint Jaygarcia Saturn",
        "categoria": "Governo Mundial",
        "imagem_url": "/figurinhas/19/imagem"
    },
    {
        "id": 21,
        "nome": "Joy Boy",
        "categoria": "Lendas",
        "imagem_url": "/figurinhas/20/imagem"
    },
    {
        "id": 22,
        "nome": "Gol D. Roger",
        "categoria": "Lendas",
        "imagem_url": "/figurinhas/21/imagem"
    },
    {
        "id": 23,
        "nome": "Rocks D. Xebec",
        "categoria": "Lendas",
        "imagem_url": "/figurinhas/22/imagem"
    },
    {
        "id": 24,
        "nome": "Edward Newgate",
        "categoria": "Lendas",
        "imagem_url": "/figurinhas/23/imagem"
    },
    {
        "id": 25,
        "nome": "Shanks",
        "categoria": "Lendas",
        "imagem_url": "/figurinhas/24/imagem"
    },
    {
        "id": 26,
        "nome": "Monkey D. Garp",
        "categoria": "Marinha",
        "imagem_url": "/figurinhas/25/imagem"
    },
    {
        "id": 27,
        "nome": "Monkey D. Dragon",
        "categoria": "Outros",
        "imagem_url": "/figurinhas/26/imagem"
    },
    {
        "id": 28,
        "nome": "Loki",
        "categoria": "Outros",
        "imagem_url": "/figurinhas/27/imagem"
    },
    {
        "id": 29,
        "nome": "Rei Harald",
        "categoria": "Outros",
        "imagem_url": "/figurinhas/28/imagem"
    },
    {
        "id": 30,
        "nome": "Sogeking",
        "categoria": "Chapéu de Palha",
        "imagem_url": "/figurinhas/29/imagem"
    }
]


# Endpoint GET /figurinhas: retorna a lista das figurinhas disponíveis
@app.get("/figurinhas")
def listar_figurinhas():
    return figurinhas


# Endpoint GET /figurinhas/{id}/imagem: retorna a imagem correspondente ao ID físico do arquivo
@app.get("/figurinhas/{id}/imagem")
def obter_imagem_figurinha(id: int):
    # Usa glob para encontrar o arquivo com prefixo "{id:02d}[!0-9]*" na pasta figurinhas/
    padrao_busca = os.path.join(PASTA_IMAGENS, f"{id:02d}[!0-9]*")
    arquivos_encontrados = glob.glob(padrao_busca)

    # Retorna 404 se não encontrar o arquivo
    if not arquivos_encontrados:
        raise HTTPException(status_code=404, detail="Imagem não encontrada")

    # Retorna FileResponse com o arquivo encontrado
    caminho_arquivo = arquivos_encontrados[0]
    return FileResponse(caminho_arquivo)

