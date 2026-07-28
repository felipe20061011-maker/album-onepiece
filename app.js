// ===================================================
// CONFIGURAÇÃO DA API
// Quando o frontend for servido pelo FastAPI (Dia 3), a API está
// no mesmo servidor — usamos uma URL relativa ou o endereço completo.
// ===================================================
const API_BASE_URL = window.location.protocol === "file:" || 
                      window.location.hostname === "localhost" || 
                      window.location.hostname === "127.0.0.1" || 
                      window.location.hostname === ""
    ? "http://localhost:8000"
    : window.location.origin;

// ===================================================
// FUNÇÃO: Preenche os slots do álbum com imagens da API
// Esta função é chamada após o álbum ser inicializado.
// ===================================================
// Global reference to sticker data mapping
window.figurinhasDataMap = new Map();

async function preencherFigurinhas() {
    try {
        // 1. Busca as figurinhas disponíveis na API
        const response = await fetch(`${API_BASE_URL}/figurinhas`);

        if (!response.ok) {
            throw new Error(`Erro na API: ${response.status} ${response.statusText}`);
        }

        // 2. Converte o JSON em array JavaScript
        const figurinhas = await response.json();

        // 3. Cria o Map global de id → figurinha para lookup rápido e interações
        window.figurinhasDataMap = new Map(figurinhas.map(f => [f.id, f]));

        // 4. Percorre todos os slots do HTML
        const slots = document.querySelectorAll(".sticker-slot");
        let activeImagesLoaded = 0;

        for (const slot of slots) {
            const slotNumeroEl = slot.querySelector(".slot-number");
            if (!slotNumeroEl) continue;

            // Extrai o número do slot: "#01" → 1
            const id = parseInt(slotNumeroEl.textContent.replace("#", ""), 10);

            if (!window.figurinhasDataMap.has(id)) continue;

            const figurinha = window.figurinhasDataMap.get(id);
            
            // Define o atributo de raridade no slot para aplicar os estilos de hover/brilho no CSS
            slot.setAttribute("data-rarity", figurinha.raridade || "Comum");

            const img = document.createElement("img");
            img.src = `${API_BASE_URL}${figurinha.imagem_url}?t=${Date.now()}`;
            img.alt = figurinha.nome;
            img.className = "sticker-img";
            img.setAttribute("data-id", id);

            img.onload = () => {
                slot.classList.add("slot-preenchido");
                activeImagesLoaded++;
                updateProgress();
            };
            img.onerror = () => {
                console.warn(`Imagem não encontrada: ${figurinha.nome}`);
            };

            slot.insertBefore(img, slot.firstChild);

            // Adiciona evento de clique para abrir o modal de detalhes
            slot.addEventListener("click", () => {
                if (slot.classList.contains("slot-preenchido")) {
                    abrirModal(figurinha);
                }
            });
        }

        // Atualiza a barra de progresso inicialmente
        updateProgress();
        console.log(`✅ ${figurinhas.length} figurinhas carregadas da API!`);

    } catch (erro) {
        console.warn("⚠️  Não foi possível conectar à API do backend:", erro.message);
        console.info("ℹ️  Inicie o servidor: cd backend && uvicorn main:app --reload");
    }
}

// Atualiza o contador de progresso
function updateProgress() {
    const total = 30;
    const loaded = document.querySelectorAll(".sticker-slot.slot-preenchido").length;
    const textEl = document.getElementById("progress-text");
    const fillEl = document.getElementById("progress-fill");
    
    if (textEl) textEl.textContent = `${loaded}/${total}`;
    if (fillEl) {
        const percentage = (loaded / total) * 100;
        fillEl.style.width = `${percentage}%`;
    }
}

// Abre o modal de detalhes com os dados dinâmicos da API
function abrirModal(item) {
    const modal = document.getElementById("sticker-modal");
    if (!modal) return;

    modal.setAttribute("data-rarity", item.raridade || "Comum");
    
    const imgEl = document.getElementById("modal-img");
    const nameEl = document.getElementById("modal-name");
    const rarityEl = document.getElementById("modal-rarity");
    const affEl = document.getElementById("modal-affiliation");
    const descEl = document.getElementById("modal-description");

    const catEl = document.getElementById("modal-category");

    if (imgEl) {
        imgEl.src = `${API_BASE_URL}${item.imagem_url}?t=${Date.now()}`;
        imgEl.alt = item.nome;
    }
    if (nameEl) nameEl.textContent = item.nome;
    if (rarityEl) rarityEl.textContent = item.raridade || "Comum";
    if (affEl) affEl.textContent = item.afiliacao || "Nenhuma";
    if (catEl) catEl.textContent = item.categoria || "Geral";
    if (descEl) descEl.textContent = item.descricao || "";

    // Configura e oculta linhas da tabela vazias/desconhecidas
    const configureField = (fieldId, rowId, value, allowUnknown = false) => {
        const el = document.getElementById(fieldId);
        const row = document.getElementById(rowId);
        if (el && row) {
            if (value && value !== "Nenhuma" && value !== "Nenhum" && (allowUnknown || (value !== "Desconhecido" && value !== "Desconhecida"))) {
                el.textContent = value;
                row.style.display = "";
            } else {
                row.style.display = "none";
            }
        }
    };

    configureField("modal-role", "row-role", item.cargo);
    configureField("modal-fruit", "row-fruit", item.fruta_do_diabo, true);
    configureField("modal-haki", "row-haki", item.haki);
    configureField("modal-bounty", "row-bounty", item.recompensa);

    modal.classList.add("open");
}

// Fecha o modal de detalhes
function fecharModal() {
    const modal = document.getElementById("sticker-modal");
    if (modal) modal.classList.remove("open");
}

document.addEventListener("DOMContentLoaded", () => {
    const bookElement = document.getElementById("book");
    const btnPrev = document.getElementById("btn-prev");
    const btnNext = document.getElementById("btn-next");
    const soundToggle = document.getElementById("sound-toggle");
    const iconOn = soundToggle.querySelector(".sound-icon-on");
    const iconOff = soundToggle.querySelector(".sound-icon-off");

    let isMuted = false;
    let pageFlip = null;

    // 1. Initialize St.PageFlip
    try {
        pageFlip = new St.PageFlip(bookElement, {
            width: 550, // Base page width
            height: 800, // Base page height
            size: "stretch",
            minWidth: 315,
            maxWidth: 1000,
            minHeight: 420,
            maxHeight: 1350,
            drawShadow: true,
            maxShadowOpacity: 0.4, // Aumenta levemente contraste da sombra
            showCover: true,
            mobileScrollSupport: true,
            useMouseEvents: false, // Desativa gestos padrão do StPageFlip para evitar cliques indesejados nas bordas/páginas
            showPageCorners: false, // Remove dobras dos cantos no hover
            disableFlipByClick: true, // Garante que a virada por cliques simples esteja desativada
            flippingTime: 800 // Transição mais ágil e snappier (800ms em vez de 1000ms)
        });

        // Load pages from HTML
        pageFlip.loadFromHTML(document.querySelectorAll(".page"));

        // Estado de arraste personalizado
        let activeDragPage = null;
        let isClicking = false;
        let startX = 0;
        let startY = 0;
        let dragStarted = false;

        // Monitora o mousedown/touchstart em cada página para iniciar a intenção de arraste
        document.querySelectorAll(".page").forEach((page, index) => {
            page.addEventListener("mousedown", (e) => {
                if (e.target.closest("button") || e.target.closest("a")) return;
                isClicking = true;
                startX = e.clientX;
                startY = e.clientY;
                dragStarted = false;
                activeDragPage = { page, index };
            });

            page.addEventListener("touchstart", (e) => {
                if (e.target.closest("button") || e.target.closest("a")) return;
                const touch = e.touches[0];
                isClicking = true;
                startX = touch.clientX;
                startY = touch.clientY;
                dragStarted = false;
                activeDragPage = { page, index };
            });
        });

        // Executa o movimento de dobra apenas se o mouse/dedo se mover além de um limiar (threshold)
        const handleMove = (clientX, clientY, isTouch = false) => {
            if (!isClicking || !activeDragPage) return;
            
            const deltaX = clientX - startX;
            const deltaY = clientY - startY;
            const distance = Math.sqrt(deltaX * deltaX + deltaY * deltaY);
            
            const bookRect = bookElement.getBoundingClientRect();

            // Só ativa o flip se mover mais de 10px (evita disparar ao clicar e soltar estático)
            if (distance > 10 && !dragStarted) {
                dragStarted = true;
                let cornerX, cornerY;
                
                // Determina canto vertical (topo vs base) em coordenadas relativas ao livro
                const centerY = bookRect.top + bookRect.height / 2;
                if (startY < centerY) {
                    cornerY = 0; // Canto superior
                } else {
                    cornerY = bookRect.height; // Canto inferior
                }

                // Determina canto horizontal (direita vs esquerda) em coordenadas relativas ao livro
                if (activeDragPage.index % 2 === 0) {
                    cornerX = bookRect.width; // Canto direito
                } else {
                    cornerX = 0; // Canto esquerdo
                }
                
                document.body.classList.add("dragging");
                pageFlip.startUserTouch({ x: cornerX, y: cornerY });
            }
            
            if (dragStarted) {
                const relX = clientX - bookRect.left;
                const relY = clientY - bookRect.top;
                pageFlip.userMove({ x: relX, y: relY }, isTouch);
            }
        };

        const handleRelease = (clientX, clientY, isTouch = false) => {
            if (dragStarted) {
                const bookRect = bookElement.getBoundingClientRect();
                const relX = clientX - bookRect.left;
                const relY = clientY - bookRect.top;
                pageFlip.userStop({ x: relX, y: relY }, isTouch);
            }
            isClicking = false;
            dragStarted = false;
            activeDragPage = null;
            document.body.classList.remove("dragging");
        };

        window.addEventListener("mousemove", (e) => {
            handleMove(e.clientX, e.clientY, false);
        });

        window.addEventListener("touchmove", (e) => {
            if (e.touches.length > 0) {
                const touch = e.touches[0];
                handleMove(touch.clientX, touch.clientY, true);
            }
        });

        window.addEventListener("mouseup", (e) => {
            handleRelease(e.clientX, e.clientY, false);
        });

        window.addEventListener("touchend", (e) => {
            const touch = e.changedTouches[0] || e.touches[0];
            if (touch) {
                handleRelease(touch.clientX, touch.clientY, true);
            } else {
                handleRelease(startX, startY, true);
            }
        });

        // Show book after successful initialization
        bookElement.style.display = "block";

        // Dia 3: Busca as figurinhas da API e preenche o álbum
        // A função é async, chamamos sem await para não bloquear a inicialização do álbum
        preencherFigurinhas();

    } catch (error) {
        console.error("Erro ao inicializar a biblioteca PageFlip:", error);
    }

    // 2. Sound Effect Generator (Web Audio API)
    function playPaperTurnSound() {
        if (isMuted) return;

        try {
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            if (!AudioContext) return;

            const audioCtx = new AudioContext();
            const duration = 0.45; // seconds
            const sampleRate = audioCtx.sampleRate;
            const bufferSize = sampleRate * duration;
            const buffer = audioCtx.createBuffer(1, bufferSize, sampleRate);
            const data = buffer.getChannelData(0);

            // Synthesize white noise with a custom page-flip volume envelope
            for (let i = 0; i < bufferSize; i++) {
                const progress = i / bufferSize;
                // Noise value between -1 and 1
                const noise = Math.random() * 2 - 1;

                // Volume envelope: smooth curve that peaks around 30% of the duration
                let envelope = 0;
                if (progress < 0.3) {
                    envelope = progress / 0.3; // Rapid ramp up
                } else {
                    envelope = (1 - progress) / 0.7; // Smooth decay
                }

                // Add minor irregular spikes to simulate paper friction/crackle
                const paperCrackle = Math.random() > 0.985 ? (Math.random() * 2 - 1) * 0.35 : 0;

                data[i] = (noise * 0.65 + paperCrackle) * envelope * 0.12;
            }

            // Create nodes
            const noiseNode = audioCtx.createBufferSource();
            noiseNode.buffer = buffer;

            // Bandpass filter to extract the "whoosh" sound of paper shuffling
            const bandpassFilter = audioCtx.createBiquadFilter();
            bandpassFilter.type = "bandpass";
            bandpassFilter.Q.value = 2.0;

            // Dynamic frequency sweep: starts at 1500Hz, sweeps down to 350Hz (sound of page moving away)
            bandpassFilter.frequency.setValueAtTime(1500, audioCtx.currentTime);
            bandpassFilter.frequency.exponentialRampToValueAtTime(350, audioCtx.currentTime + duration);

            // Lowpass filter to remove harsh high-frequency digital artifacts
            const lowpassFilter = audioCtx.createBiquadFilter();
            lowpassFilter.type = "lowpass";
            lowpassFilter.frequency.setValueAtTime(3800, audioCtx.currentTime);

            // Connect graph: Source -> Bandpass -> Lowpass -> Destination
            noiseNode.connect(bandpassFilter);
            bandpassFilter.connect(lowpassFilter);
            lowpassFilter.connect(audioCtx.destination);

            noiseNode.start();
        } catch (e) {
            console.warn("Falha ao tocar som de virada de página:", e);
        }
    }

    // 3. Audio State Controls
    soundToggle.addEventListener("click", () => {
        isMuted = !isMuted;
        if (isMuted) {
            iconOn.classList.add("hidden");
            iconOff.classList.remove("hidden");
        } else {
            iconOn.classList.remove("hidden");
            iconOff.classList.add("hidden");
        }
    });

    // 4. Navigation controls and events
    if (pageFlip) {
        // Play turn sound when page starts flipping
        pageFlip.on("changeState", (e) => {
            if (e.data === "flipping") {
                playPaperTurnSound();
            }
        });

        // Discrete arrow toggle depending on current page
        pageFlip.on("flip", (e) => {
            const currentPage = e.data;
            const totalPages = pageFlip.getPageCount();

            // Hide left button on cover page
            if (currentPage === 0) {
                btnPrev.classList.add("hidden");
            } else {
                btnPrev.classList.remove("hidden");
            }

            // Hide right button on back cover
            if (currentPage === totalPages - 1) {
                btnNext.classList.add("hidden");
            } else {
                btnNext.classList.remove("hidden");
            }
        });

        // Click events for navigational arrows
        btnPrev.addEventListener("click", () => {
            pageFlip.flipPrev();
        });

        btnNext.addEventListener("click", () => {
            pageFlip.flipNext();
        });

        // Keyboard events for navigational arrows
        document.addEventListener("keydown", (e) => {
            if (e.key === "ArrowLeft") {
                pageFlip.flipPrev();
            } else if (e.key === "ArrowRight") {
                pageFlip.flipNext();
            }
        });

        // Hide left button initially since start page is 0
        btnPrev.classList.add("hidden");

        // Modal close button click
        const closeBtn = document.getElementById("modal-close-btn");
        if (closeBtn) {
            closeBtn.addEventListener("click", fecharModal);
        }

        // Close modal when clicking on overlay background
        const modalOverlay = document.getElementById("sticker-modal");
        if (modalOverlay) {
            modalOverlay.addEventListener("click", (e) => {
                if (e.target === modalOverlay) {
                    fecharModal();
                }
            });
        }

        // Back to Top functionality
        const backToTopBtn = document.getElementById("back-to-top");
        if (backToTopBtn) {
            window.addEventListener("scroll", () => {
                if (window.scrollY > 300) {
                    backToTopBtn.classList.add("visible");
                } else {
                    backToTopBtn.classList.remove("visible");
                }
            });

            backToTopBtn.addEventListener("click", () => {
                window.scrollTo({ top: 0, behavior: "smooth" });
            });
        }

        // Category Filter logic
        const filterBtns = document.querySelectorAll(".filter-btn");

        function applyFilters() {
            const activeBtn = document.querySelector(".filter-btn.active");
            const activeCategory = activeBtn ? activeBtn.getAttribute("data-category") : "todos";

            const slots = document.querySelectorAll(".sticker-slot");
            slots.forEach(slot => {
                const slotNumeroEl = slot.querySelector(".slot-number");
                if (!slotNumeroEl) return;
                const id = parseInt(slotNumeroEl.textContent.replace("#", ""), 10);
                const item = window.figurinhasDataMap ? window.figurinhasDataMap.get(id) : null;

                if (!item) {
                    if (activeCategory !== "todos") {
                        slot.classList.add("dimmed");
                    } else {
                        slot.classList.remove("dimmed");
                    }
                    return;
                }

                const matchCategory = activeCategory === "todos" || item.categoria === activeCategory;

                if (matchCategory) {
                    slot.classList.remove("dimmed");
                    if (activeCategory !== "todos") {
                        slot.classList.add("highlighted");
                    } else {
                        slot.classList.remove("highlighted");
                    }
                } else {
                    slot.classList.add("dimmed");
                    slot.classList.remove("highlighted");
                }
            });
        }

        filterBtns.forEach(btn => {
            btn.addEventListener("click", () => {
                filterBtns.forEach(b => b.classList.remove("active"));
                btn.classList.add("active");
                applyFilters();
            });
        });

        // Add a smooth page-turn content animation
        pageFlip.on("flip", (e) => {
            const index = e.data;
            const pagesEl = document.querySelectorAll(".page");
            const activePage = pagesEl[index];
            if (activePage) {
                const content = activePage.querySelector(".page-content");
                if (content) {
                    content.style.animation = "none";
                    // Trigger reflow
                    void content.offsetHeight;
                    content.style.animation = "fadeIn 0.5s ease-out forwards";
                }
            }
        });
    }
});
