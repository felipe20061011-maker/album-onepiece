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
# Todas as 30 figurinhas estão ativas agora, com metadados enriquecidos para o modal de detalhes.
figurinhas = [
    {
        "id": 1,
        "nome": "Monkey D. Luffy",
        "categoria": "Chapéu de Palha",
        "imagem_url": "/figurinhas/1/imagem",
        "afiliacao": "Piratas do Chapéu de Palha",
        "cargo": "Capitão / Yonkou",
        "fruta_do_diabo": "Hito Hito no Mi, Modelo: Nika",
        "haki": "Observação, Armamento, Rei (Avançado)",
        "primeira_aparicao": "Capítulo 1 / Episódio 1",
        "recompensa": "3.000.000.000 Berries",
        "descricao": "Luffy é o capitão alegre e determinado dos Chapéus de Palha, cujo sonho é encontrar o lendário tesouro One Piece e se tornar o Rei dos Piratas.",
        "raridade": "Lendário"
    },
    {
        "id": 2,
        "nome": "Roronoa Zoro",
        "categoria": "Chapéu de Palha",
        "imagem_url": "/figurinhas/2/imagem",
        "afiliacao": "Piratas do Chapéu de Palha",
        "cargo": "Combatente / Imediato",
        "fruta_do_diabo": "Nenhuma",
        "haki": "Observação, Armamento, Rei",
        "primeira_aparicao": "Capítulo 3 / Episódio 2",
        "recompensa": "1.111.000.000 Berries",
        "descricao": "Zoro é o primeiro membro a se juntar a Luffy, um mestre espadachim que usa o estilo de três espadas e busca se tornar o maior espadachim do mundo.",
        "raridade": "Raro"
    },
    {
        "id": 3,
        "nome": "Nami",
        "categoria": "Chapéu de Palha",
        "imagem_url": "/figurinhas/3/imagem",
        "afiliacao": "Piratas do Chapéu de Palha",
        "cargo": "Navegadora",
        "fruta_do_diabo": "Nenhuma",
        "haki": "Nenhum",
        "primeira_aparicao": "Capítulo 8 / Episódio 1",
        "recompensa": "366.000.000 Berries",
        "descricao": "Nami é a navegadora inteligente do bando, com o sonho de desenhar um mapa completo de todo o mundo de One Piece.",
        "raridade": "Comum"
    },
    {
        "id": 4,
        "nome": "Usopp",
        "categoria": "Chapéu de Palha",
        "imagem_url": "/figurinhas/4/imagem",
        "afiliacao": "Piratas do Chapéu de Palha",
        "cargo": "Atirador",
        "fruta_do_diabo": "Nenhuma",
        "haki": "Observação",
        "primeira_aparicao": "Capítulo 23 / Episódio 8",
        "recompensa": "500.000.000 Berries",
        "descricao": "Usopp é o atirador do bando e um grande contador de histórias, que busca se tornar um bravo guerreiro do mar.",
        "raridade": "Comum"
    },
    {
        "id": 5,
        "nome": "Sanji",
        "categoria": "Chapéu de Palha",
        "imagem_url": "/figurinhas/5/imagem",
        "afiliacao": "Piratas do Chapéu de Palha",
        "cargo": "Cozinheiro",
        "fruta_do_diabo": "Nenhuma",
        "haki": "Observação, Armamento",
        "primeira_aparicao": "Capítulo 43 / Episódio 20",
        "recompensa": "1.032.000.000 Berries",
        "descricao": "Sanji é o cozinheiro cavalheiro do bando, que luta usando apenas as pernas para proteger suas mãos, e sonha em encontrar o All Blue.",
        "raridade": "Raro"
    },
    {
        "id": 6,
        "nome": "Tony Tony Chopper",
        "categoria": "Chapéu de Palha",
        "imagem_url": "/figurinhas/6/imagem",
        "afiliacao": "Piratas do Chapéu de Palha",
        "cargo": "Médico",
        "fruta_do_diabo": "Hito Hito no Mi",
        "haki": "Nenhum",
        "primeira_aparicao": "Capítulo 134 / Episódio 81",
        "recompensa": "1.000 Berries",
        "descricao": "Chopper é uma rena amável que comeu a fruta do humano e serve como o médico genial do bando dos Chapéus de Palha.",
        "raridade": "Comum"
    },
    {
        "id": 7,
        "nome": "Nico Robin",
        "categoria": "Chapéu de Palha",
        "imagem_url": "/figurinhas/7/imagem",
        "afiliacao": "Piratas do Chapéu de Palha",
        "cargo": "Arqueóloga",
        "fruta_do_diabo": "Hana Hana no Mi",
        "haki": "Armamento (Indireto)",
        "primeira_aparicao": "Capítulo 114 / Episódio 67",
        "recompensa": "930.000.000 Berries",
        "descricao": "Robin é a arqueóloga do bando e a única pessoa sobrevivente capaz de ler os Poneglyphs para descobrir a história perdida do mundo.",
        "raridade": "Raro"
    },
    {
        "id": 8,
        "nome": "Franky",
        "categoria": "Chapéu de Palha",
        "imagem_url": "/figurinhas/8/imagem",
        "afiliacao": "Piratas do Chapéu de Palha",
        "cargo": "Carpinteiro",
        "fruta_do_diabo": "Nenhuma",
        "haki": "Nenhum",
        "primeira_aparicao": "Capítulo 329 / Episódio 233",
        "recompensa": "394.000.000 Berries",
        "descricao": "Franky é o carpinteiro ciborgue super extravagante que construiu o Thousand Sunny e sonha em fazê-lo navegar até o fim do mundo.",
        "raridade": "Comum"
    },
    {
        "id": 9,
        "nome": "Brook",
        "categoria": "Chapéu de Palha",
        "imagem_url": "/figurinhas/9/imagem",
        "afiliacao": "Piratas do Chapéu de Palha",
        "cargo": "Músico",
        "fruta_do_diabo": "Yomi Yomi no Mi",
        "haki": "Observação, Armamento",
        "primeira_aparicao": "Capítulo 442 / Episódio 337",
        "recompensa": "383.000.000 Berries",
        "descricao": "Brook é um esqueleto vivo e o músico do bando, um espadachim habilidoso que sonha em se reencontrar com a baleia Laboon.",
        "raridade": "Comum"
    },
    {
        "id": 10,
        "nome": "Jinbe",
        "categoria": "Chapéu de Palha",
        "imagem_url": "/figurinhas/10/imagem",
        "afiliacao": "Piratas do Chapéu de Palha",
        "cargo": "Timoneiro",
        "fruta_do_diabo": "Nenhuma",
        "haki": "Observação, Armamento",
        "primeira_aparicao": "Capítulo 528 / Episódio 430",
        "recompensa": "1.100.000.000 Berries",
        "descricao": "Jinbe é o timoneiro sábio do bando, um Tritão ex-Shichibukai e mestre supremo do Caratê Tritão.",
        "raridade": "Raro"
    },
    {
        "id": 11,
        "nome": "Imu",
        "categoria": "Governo Mundial",
        "imagem_url": "/figurinhas/11/imagem",
        "afiliacao": "Governo Mundial",
        "cargo": "Soberano Supremo",
        "fruta_do_diabo": "Desconhecida",
        "haki": "Desconhecido",
        "primeira_aparicao": "Capítulo 906 / Episódio 885",
        "recompensa": "Nenhuma",
        "descricao": "A figura misteriosa e sombria que se assenta no Trono Vazio, governando o mundo secretamente acima dos Gorosei.",
        "raridade": "Lendário"
    },
    {
        "id": 12,
        "nome": "Saint Garling Figarland",
        "categoria": "Governo Mundial",
        "imagem_url": "/figurinhas/12/imagem",
        "afiliacao": "Governo Mundial / Nobres Mundiais",
        "cargo": "Comandante dos Cavaleiros Sagrados",
        "fruta_do_diabo": "Nenhuma",
        "haki": "Observação, Armamento",
        "primeira_aparicao": "Capítulo 1086 / Episódio 1109",
        "recompensa": "Nenhuma",
        "descricao": "Líder implacável dos Cavaleiros Sagrados e figura influente de God Valley.",
        "raridade": "Raro"
    },
    {
        "id": 13,
        "nome": "Saint Shamrock Figarland",
        "categoria": "Governo Mundial",
        "imagem_url": "/figurinhas/13/imagem",
        "afiliacao": "Governo Mundial",
        "cargo": "Cavaleiro Sagrado",
        "fruta_do_diabo": "Nenhuma",
        "haki": "Observação, Armamento",
        "primeira_aparicao": "Capítulo 1086 / Episódio 1109",
        "recompensa": "Nenhuma",
        "descricao": "Um dos Cavaleiros Sagrados que impõe a justiça do Governo Mundial contra os rebeldes.",
        "raridade": "Lendário"
    },
    {
        "id": 14,
        "nome": "Gunko",
        "categoria": "Governo Mundial",
        "imagem_url": "/figurinhas/14/imagem",
        "afiliacao": "Governo Mundial",
        "cargo": "Agente do Governo",
        "fruta_do_diabo": "Aro Aro no Mi",
        "haki": "Armamento",
        "primeira_aparicao": "Capítulo 1086",
        "recompensa": "Nenhuma",
        "descricao": "Um temido executor das ordens do Governo Mundial.",
        "raridade": "Lendário"
    },
    {
        "id": 15,
        "nome": "Akainu (Sakazuki)",
        "categoria": "Marinha",
        "imagem_url": "/figurinhas/15/imagem",
        "afiliacao": "Marinha",
        "cargo": "Almirante de Frota",
        "fruta_do_diabo": "Magu Magu no Mi",
        "haki": "Observação, Armamento",
        "primeira_aparicao": "Capítulo 397 / Episódio 278",
        "recompensa": "Nenhuma",
        "descricao": "O líder supremo da Marinha que defende ferozmente a Doutrina da Justiça Absoluta usando o poder do magma.",
        "raridade": "Lendário"
    },
    {
        "id": 16,
        "nome": "Kizaru (Borsalino)",
        "categoria": "Marinha",
        "imagem_url": "/figurinhas/16/imagem",
        "afiliacao": "Marinha",
        "cargo": "Almirante",
        "fruta_do_diabo": "Pika Pika no Mi",
        "haki": "Observação, Armamento",
        "primeira_aparicao": "Capítulo 504 / Episódio 398",
        "recompensa": "Nenhuma",
        "descricao": "Um Almirante descontraído com o poder de se transformar, mover e atacar na velocidade da luz.",
        "raridade": "Raro"
    },
    {
        "id": 17,
        "nome": "Aokiji (Kuzan)",
        "categoria": "Marinha",
        "imagem_url": "/figurinhas/17/imagem",
        "afiliacao": "Marinha (Ex-membro) / Piratas do Barba Negra",
        "cargo": "Ex-Almirante",
        "fruta_do_diabo": "Hie Hie no Mi",
        "haki": "Observação, Armamento",
        "primeira_aparicao": "Capítulo 303 / Episódio 225",
        "recompensa": "Desconhecida",
        "descricao": "Ex-Almirante da Marinha que segue sua própria Justiça Preguiçosa e aliou-se ao bando do Barba Negra.",
        "raridade": "Raro"
    },
    {
        "id": 18,
        "nome": "Ryokugyu (Aramaki)",
        "categoria": "Marinha",
        "imagem_url": "/figurinhas/18/imagem",
        "afiliacao": "Marinha",
        "cargo": "Almirante",
        "fruta_do_diabo": "Mori Mori no Mi",
        "haki": "Observação, Armamento",
        "primeira_aparicao": "Capítulo 905 / Episódio 882",
        "recompensa": "Nenhuma",
        "descricao": "Almirante da Marinha com a habilidade de controlar, gerar e se transformar na própria vida vegetal da floresta.",
        "raridade": "Raro"
    },
    {
        "id": 19,
        "nome": "Fujitora (Issho)",
        "categoria": "Marinha",
        "imagem_url": "/figurinhas/19/imagem",
        "afiliacao": "Marinha",
        "cargo": "Almirante",
        "fruta_do_diabo": "Zushi Zushi no Mi",
        "haki": "Observação, Armamento",
        "primeira_aparicao": "Capítulo 701 / Episódio 630",
        "recompensa": "Nenhuma",
        "descricao": "Um honrado Almirante cego que manipula as forças da gravidade e busca a verdadeira proteção dos cidadãos.",
        "raridade": "Raro"
    },
    {
        "id": 20,
        "nome": "Saint Jaygarcia Saturn",
        "categoria": "Governo Mundial",
        "imagem_url": "/figurinhas/20/imagem",
        "afiliacao": "Governo Mundial / Gorosei",
        "cargo": "Deus Guerreiro da Defesa Científica",
        "fruta_do_diabo": "Desconhecida (Forma Zoan Desperta)",
        "haki": "Observação, Armamento, Rei",
        "primeira_aparicao": "Capítulo 1073 / Episódio 1093",
        "recompensa": "Nenhuma",
        "descricao": "Um dos cinco anciãos que governam o mundo, capaz de invocar transformações demoníacas aterradoras.",
        "raridade": "Lendário"
    },
    {
        "id": 21,
        "nome": "Joy Boy",
        "categoria": "Lendas",
        "imagem_url": "/figurinhas/21/imagem",
        "afiliacao": "Desconhecida (Século Perdido)",
        "cargo": "Desconhecido",
        "fruta_do_diabo": "Hito Hito no Mi, Modelo: Nika",
        "haki": "Observação, Armamento, Rei",
        "primeira_aparicao": "Mencionado no Capítulo 628",
        "recompensa": "Nenhuma",
        "descricao": "A figura enigmática e histórica do Século Perdido que deixou o lendário tesouro na última ilha, Laugh Tale.",
        "raridade": "Lendário"
    },
    {
        "id": 22,
        "nome": "Gol D. Roger",
        "categoria": "Lendas",
        "imagem_url": "/figurinhas/22/imagem",
        "afiliacao": "Piratas do Roger",
        "cargo": "Rei dos Piratas / Capitão",
        "fruta_do_diabo": "Nenhuma",
        "haki": "Observação, Armamento, Rei (Mestre)",
        "primeira_aparicao": "Capítulo 1 / Episódio 1",
        "recompensa": "5.564.800.000 Berries",
        "descricao": "O lendário Rei dos Piratas que conquistou a Grand Line inteira e deu início à Grande Era dos Piratas antes de sua morte.",
        "raridade": "Lendário"
    },
    {
        "id": 23,
        "nome": "Rocks D. Xebec",
        "categoria": "Lendas",
        "imagem_url": "/figurinhas/23/imagem",
        "afiliacao": "Piratas do Rocks",
        "cargo": "Capitão",
        "fruta_do_diabo": "Desconhecida",
        "haki": "Observação, Armamento, Rei",
        "primeira_aparicao": "Mencionado no Capítulo 957",
        "recompensa": "Desconhecida",
        "descricao": "O pirata mais formidável e violento da história que liderou o bando mais perigoso do mundo antes de ser derrotado em God Valley.",
        "raridade": "Lendário"
    },
    {
        "id": 24,
        "nome": "Edward Newgate",
        "categoria": "Lendas",
        "imagem_url": "/figurinhas/24/imagem",
        "afiliacao": "Piratas do Barba Branca",
        "cargo": "Capitão",
        "fruta_do_diabo": "Gura Gura no Mi",
        "haki": "Observação, Armamento, Rei",
        "primeira_aparicao": "Capítulo 234 / Episódio 151",
        "recompensa": "5.046.000.000 Berries",
        "descricao": "Conhecido como Barba Branca, o homem mais forte do mundo e rival de Roger, que considerava sua tripulação como sua família.",
        "raridade": "Lendário"
    },
    {
        "id": 25,
        "nome": "Shanks",
        "categoria": "Lendas",
        "imagem_url": "/figurinhas/25/imagem",
        "afiliacao": "Piratas do Ruivo / Yonkou",
        "cargo": "Capitão",
        "fruta_do_diabo": "Nenhuma",
        "haki": "Observação, Armamento, Rei (Avançado)",
        "primeira_aparicao": "Capítulo 1 / Episódio 4",
        "recompensa": "4.048.900.000 Berries",
        "descricao": "O capitão dos Piratas do Ruivo e um dos Yonkou, lendário por seu formidável Haki do Conquistador e por inspirar Luffy a ir ao mar.",
        "raridade": "Lendário"
    },
    {
        "id": 26,
        "nome": "Monkey D. Garp",
        "categoria": "Marinha",
        "imagem_url": "/figurinhas/26/imagem",
        "afiliacao": "Marinha",
        "cargo": "Vice-Almirante / Herói da Marinha",
        "fruta_do_diabo": "Nenhuma",
        "haki": "Observação, Armamento, Rei",
        "primeira_aparicao": "Capítulo 92 / Episódio 68",
        "recompensa": "3.000.000.000 Berries (Cross Guild)",
        "descricao": "O Herói Lendário da Marinha que lutou de igual para igual contra Gol D. Roger e é avô de Luffy.",
        "raridade": "Lendário"
    },
    {
        "id": 27,
        "nome": "Monkey D. Dragon",
        "categoria": "Outros",
        "imagem_url": "/figurinhas/27/imagem",
        "afiliacao": "Exército Revolucionário",
        "cargo": "Comandante Supremo",
        "fruta_do_diabo": "Desconhecida",
        "haki": "Observação, Armamento, Rei",
        "primeira_aparicao": "Capítulo 100 / Episódio 52",
        "recompensa": "A pior do mundo (Desconhecida)",
        "descricao": "O pai de Luffy e o líder do Exército Revolucionário, rotulado como o homem mais procurado do mundo pelo Governo Mundial.",
        "raridade": "Lendário"
    },
    {
        "id": 28,
        "nome": "Loki",
        "categoria": "Outros",
        "imagem_url": "/figurinhas/28/imagem",
        "afiliacao": "Reino de Elbaf",
        "cargo": "Príncipe",
        "fruta_do_diabo": "Lendária de Elbaf",
        "haki": "Observação, Armamento",
        "primeira_aparicao": "Capítulo 1130",
        "recompensa": "Desconhecida",
        "descricao": "O príncipe gigante rebelde e insano do Reino de Elbaf que ambiciona trazer o apocalipse ao mundo.",
        "raridade": "Raro"
    },
    {
        "id": 29,
        "nome": "Rei Harald",
        "categoria": "Outros",
        "imagem_url": "/figurinhas/29/imagem",
        "afiliacao": "Reino de Elbaf",
        "cargo": "Rei (Histórico)",
        "fruta_do_diabo": "Nenhuma",
        "haki": "Observação, Armamento",
        "primeira_aparicao": "Mencionado em Elbaf",
        "recompensa": "Nenhuma",
        "descricao": "Um antigo rei guerreiro dos gigantes do Reino de Elbaf que governou com orgulho e força lendária.",
        "raridade": "Lendário"
    },
    {
        "id": 30,
        "nome": "Sogeking",
        "categoria": "Chapéu de Palha",
        "imagem_url": "/figurinhas/30/imagem",
        "afiliacao": "Ilha dos Atiradores",
        "cargo": "Rei dos Atiradores / Herói",
        "fruta_do_diabo": "Nenhuma",
        "haki": "Observação",
        "primeira_aparicao": "Capítulo 367 / Episódio 257",
        "recompensa": "30.000.000 Berries",
        "descricao": "O herói lendário e misterioso vindo da Ilha dos Atiradores, famoso por sua mira perfeita e coração valente.",
        "raridade": "Lendário"
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


# Rotas para servir os arquivos estáticos do frontend em ambiente local
@app.get("/")
def obter_index():
    return FileResponse(os.path.join(PASTA_BASE, "index.html"))


@app.get("/style.css")
def obter_style():
    return FileResponse(os.path.join(PASTA_BASE, "style.css"))


@app.get("/app.js")
def obter_app():
    return FileResponse(os.path.join(PASTA_BASE, "app.js"))


