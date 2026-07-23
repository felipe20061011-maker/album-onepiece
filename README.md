# One Piece Sticker Album 🏴‍☠️

Um álbum de figurinhas interativo e moderno com temática de **One Piece**, com ilustrações de personagens de alta qualidade em estilo anime/manga e enriquecidas com metadados de combate e história direto de uma API FastAPI.

## 🚀 Principais Funcionalidades
- **Coleção de 30 Figurinhas**: Álbum com design clássico contendo 30 slots ativos divididos por categorias (Mugiwara, Governo Mundial, Marinha, Lendas, Elbaf).
- **Metadados Detalhados (Modal Rico)**: Ao clicar em uma figurinha colada, abre-se um modal *glassmorphism* contendo informações do personagem (afiliação, cargo, fruta do diabo, haki, recompensa, primeira aparição e uma descrição).
- **Filtro de Categorias Dinâmico**: Botões de filtro no topo para destacar as figurinhas pertencentes a grupos específicos.
- **Efeitos e Animações Premium**:
  - Hover dinâmico com brilho adaptado à raridade do card (Lendário = Vermelho, Raro = Dourado, Comum = Prata).
  - Transições suaves e animações de folha ao virar a página.
  - Rolagem rápida com botão de voltar ao topo.
- **Cabeçalho Compacto & Progresso**: Barra superior enxuta mostrando o progresso da coleção de figurinhas coladas com animação em LED.
- **Bypass de Cache (Cache-Busting)**: Integração com cache-buster na carga de imagens para garantir atualizações em tempo real no browser.

## 🛠️ Tecnologias Utilizadas
- **Front-End**: HTML5, Vanilla CSS3 (Custom properties, grid, flexbox), Javascript Moderno (ES6), Biblioteca `page-flip` para o efeito 3D do livro.
- **Back-End**: Python 3.11+, FastAPI (ASGI Framework), Uvicorn.
- **Visual**: Ilustrações em proporção 2:3 estilo anime cinematográfico 4K.

## 📂 Estrutura do Projeto
```text
├── main.py              # Código do Backend FastAPI
├── index.html           # Layout do Álbum (HTML5)
├── style.css            # Estilização completa e efeitos (CSS3)
├── app.js               # Lógica de interação e consumo da API
├── vercel.json          # Configuração de Deploy na Vercel
├── requirements.txt     # Dependências Python
├── .gitignore           # Regras de exclusão Git
└── figurinhas/          # Pasta de imagens físicas das 30 figurinhas (IDs 01 a 30)
```

## 💻 Como Executar Localmente

### 1. Iniciar o Servidor Backend (FastAPI)
Certifique-se de que possui o Python instalado:
```bash
# Crie e ative o ambiente virtual (opcional)
python -m venv .venv
source .venv/bin/activate

# Instale as dependências
pip install -r requirements.txt

# Inicie o Uvicorn
uvicorn main:app --reload
```
O backend estará de pé no endereço `http://localhost:8000`.

### 2. Abrir o Front-End
Basta abrir o arquivo `index.html` diretamente no seu navegador de preferência ou usar uma extensão de Live Server. O front-end detectará automaticamente o backend local na porta 8000 e carregará as figurinhas.

## 🌐 Como Publicar (Deploy)

### Deploy na Vercel
O projeto já está 100% configurado para deploy automático na Vercel:
1. Conecte sua conta do GitHub à Vercel.
2. Importe este repositório.
3. Vercel detectará o `vercel.json` e o `requirements.txt` instalando as dependências de Python automaticamente.
4. O deploy estará concluído e a aplicação estará no ar!

## 📸 Screenshots
*(Marcadores para capturas de tela futuras)*
- `[Inserir Screenshot do Álbum Aberto]`
- `[Inserir Screenshot do Modal de Detalhes]`

## 📄 Licença
Este projeto é licenciado sob a licença MIT - consulte o arquivo de licença para detalhes.

## 👤 Autor
Desenvolvido com carinho por Felipe Silva e par de programação Antigravity.
