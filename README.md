# One Piece Album 🏴‍☠️

Um álbum de figurinhas digital e interativo com a temática de **One Piece**. O projeto consome uma API local em FastAPI para listar personagens e exibir detalhes sobre recompensas, afiliações e habilidades em um modal interativo.

## 🔗 Link da Aplicação
Você pode visualizar o projeto publicado na Vercel aqui:  
👉 [One Piece Album na Vercel](https://album-onepiece-9p7m0hxzg-felipe20061011-makers-projects.vercel.app/)

## 🚀 Principais Funcionalidades
- **Álbum Interativo**: Efeito virtual de virar páginas em 3D.
- **Filtros por Categoria**: Organização das cartas por grupos (Mugiwara, Governo Mundial, Marinha e Lendas).
- **Modal de Detalhes**: Exibição de informações detalhadas do personagem (afiliação, cargo, recompensa, etc.) ao clicar no card correspondente.
- **Coleção de 30 Figurinhas**: Álbum contendo 30 cartas temáticas exclusivas.

## 🛠️ Tecnologias Utilizadas
- **Front-End**: HTML5, CSS3 (Vanilla), JavaScript (ES6), Biblioteca `page-flip` (efeito de livro 3D).
- **Back-End**: Python, FastAPI, Uvicorn.

## 📂 Estrutura do Projeto
```text
├── main.py              # Backend FastAPI (rotas e dados das figurinhas)
├── index.html           # Estrutura do álbum
├── style.css            # Estilização e posicionamento das cartas
├── app.js               # Lógica de integração e PageFlip
├── vercel.json          # Configuração de deploy da Vercel
├── requirements.txt     # Dependências de Python (FastAPI e Uvicorn)
├── .gitignore           # Regras de exclusão do Git
├── fundos/              # Pasta de imagens de fundo das páginas
└── figurinhas/          # Pasta das 30 imagens das figurinhas
```

## 💻 Como Executar Localmente

### 1. Iniciar o Servidor Backend (FastAPI)
1. Crie e ative um ambiente virtual:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # No Linux/macOS
   # ou
   .venv\Scripts\activate     # No Windows
   ```
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Inicie o servidor local:
   ```bash
   uvicorn main:app --reload
   ```
O servidor estará rodando no endereço `http://localhost:8000`.

### 2. Abrir o Front-End
Abra o arquivo `index.html` diretamente no seu navegador (ou utilizando uma extensão de Live Server). O front-end carregará automaticamente os dados e as figurinhas servidos pela API local na porta 8000.

---

## 📄 Créditos e Autoria
Projeto adaptado e personalizado por **Felipe Silva**, com apoio de ferramentas de inteligência artificial para refinamento de código, enquadramentos e visual das cartas durante o processo de desenvolvimento.
