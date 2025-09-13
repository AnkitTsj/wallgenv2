
document.addEventListener('DOMContentLoaded', () => {
    const elements = {
        generateBtn: document.getElementById('generate-btn'),
        surpriseBtn: document.getElementById('surprise-btn'),
        randomSeedBtn: document.getElementById('random-seed-btn'),
        resultImage: document.getElementById('result-image'),
        paletteContainer: document.getElementById('palette-container'),
        loader: document.getElementById('loader'),
        backgroundContainer: document.getElementById('background-container'),
        statusDisplay: document.getElementById('status-display'),
        styleSelect: document.getElementById('style-select'),
        seedInput: document.getElementById('seed-input'),
        colorInput: document.getElementById('color-input'),
        postGenerationTools: document.getElementById('post-generation-tools'),
        copySeedBtn: document.getElementById('copy-seed-btn'),
        downloadBtn: document.getElementById('download-btn'),
        copySeedFeedback: document.getElementById('copy-seed-feedback'),
        tagline: document.getElementById('tagline'),
        recentCreationsSection: document.getElementById('recent-creations'),
        recentGallery: document.getElementById('recent-gallery'),
        particlesContainer: document.getElementById('particles'),
    };

    // API URL for your Python backend
    const API_URL = 'http://127.0.0.1:8000';

    // State Variables
    let backgroundImages = [];
    let recentCreations = [];
    let statusInterval;
    const MAX_BG_IMAGES = 6;
    const MAX_RECENTS = 8;

    // Enhanced Particles System
    function createParticles() {
        const colors = ['#4D6473', '#A58A73', '#B59B67', '#F4C2C2', '#E6CFC1'];
        for (let i = 0; i < 20; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            particle.style.width = Math.random() * 8 + 4 + 'px';
            particle.style.height = particle.style.width;
            particle.style.left = Math.random() * 100 + '%';
            particle.style.top = Math.random() * 100 + '%';
            particle.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
            particle.style.animationDelay = Math.random() * 15 + 's';
            particle.style.animationDuration = (Math.random() * 10 + 10) + 's';
            elements.particlesContainer.appendChild(particle);
        }
    }

    // Enhanced Typing Animation
    function typeText(element, text, speed = 100) {
        let i = 0;
        element.innerHTML = "";
        const typing = setInterval(() => {
            if (i < text.length) {
                element.innerHTML += text.charAt(i);
                i++;
            } else {
                clearInterval(typing);
                setTimeout(() => {
                    element.style.textShadow = '0 0 20px rgba(77, 100, 115, 0.5)';
                    setTimeout(() => {
                        element.style.textShadow = 'none';
                    }, 1000);
                }, 500);
            }
        }, speed);
    }

    // Enhanced Floating Background Logic
    function addFloatingImage(imageUrl) {
        const img = document.createElement('img');
        img.src = imageUrl;
        img.className = 'floating-bg';
        if (backgroundImages.length >= MAX_BG_IMAGES) {
            const oldImg = backgroundImages.shift();
            oldImg.style.opacity = '0';
            oldImg.style.transform = 'scale(0.8)';
            setTimeout(() => oldImg.remove(), 1000);
        }
        const size = Math.random() * 180 + 120;
        img.style.width = `${size}px`;
        img.style.height = 'auto';
        img.style.top = `${Math.random() * 80 + 10}%`;
        img.style.left = `${Math.random() * 80 + 10}%`;
        img.style.animationDuration = `${Math.random() * 15 + 20}s`;
        img.style.zIndex = Math.floor(Math.random() * 3) + 1;
        elements.backgroundContainer.appendChild(img);
        backgroundImages.push(img);
    }

    // Enhanced Status Messages
    function startStatusUpdates() {
        const messages = [
            " Mixing digital paint...",
            " Consulting the AI muse...",
            " Channeling creative energy...",
            " Weaving visual magic...",
            " Launching imagination...",
            " Almost there..."
        ];
        let msgIndex = 0;
        elements.statusDisplay.textContent = messages[msgIndex];
        statusInterval = setInterval(() => {
            msgIndex = (msgIndex + 1) % messages.length;
            elements.statusDisplay.textContent = messages[msgIndex];
        }, 2500);
    }

    function stopStatusUpdates(finalMessage) {
        clearInterval(statusInterval);
        elements.statusDisplay.textContent = finalMessage;
        elements.statusDisplay.style.transform = 'scale(1.1)';
        elements.statusDisplay.style.color = '#4D6473';
        setTimeout(() => {
            elements.statusDisplay.style.transform = 'scale(1)';
            elements.statusDisplay.style.color = '';
        }, 300);
    }

    // Enhanced Recent Creations
    function renderRecents() {
        if (recentCreations.length === 0) return;
        elements.recentGallery.innerHTML = "";
        recentCreations.forEach((creation, index) => {
            const img = document.createElement('img');
            img.src = creation.src;
            img.title = `Style: ${creation.style}, Seed: ${creation.seed}`;
            img.style.animationDelay = `${index * 0.1}s`;
            img.addEventListener('click', () => {
                elements.styleSelect.value = creation.style;
                elements.seedInput.value = creation.seed;
                elements.colorInput.value = creation.color || "";
                window.scrollTo({
                    top: 0,
                    behavior: 'smooth'
                });
                elements.styleSelect.style.boxShadow = '0 0 20px rgba(77, 100, 115, 0.5)';
                setTimeout(() => {
                    elements.styleSelect.style.boxShadow = '';
                }, 2000);
            });
            elements.recentGallery.appendChild(img);
        });
        elements.recentCreationsSection.classList.remove('hidden');
    }

    // Enhanced Color Palette Display
    function displayColorPalette(colors) {
        elements.paletteContainer.innerHTML = '';
        colors.forEach((color, index) => {
            const wrapper = document.createElement('div');
            wrapper.className = 'color-swatch-wrapper';
            wrapper.style.animationDelay = `${index * 0.1}s`;
            const swatch = document.createElement('div');
            swatch.className = 'color-swatch';
            swatch.style.backgroundColor = color;
            const hexCode = document.createElement('span');
            hexCode.className = 'hex-code';
            hexCode.textContent = color;
            swatch.addEventListener('click', () => {
                navigator.clipboard.writeText(color).then(() => {
                    hexCode.textContent = 'Copied!';
                    swatch.style.transform = 'scale(1.3) rotate(10deg)';
                    setTimeout(() => {
                        hexCode.textContent = color;
                        swatch.style.transform = '';
                    }, 1500);
                });
            });
            wrapper.appendChild(swatch);
            wrapper.appendChild(hexCode);
            elements.paletteContainer.appendChild(wrapper);
        });
    }

    // **UPDATED** Generation Function with actual API call
    async function performGeneration() {
        elements.loader.classList.remove('hidden');
        elements.resultImage.classList.add('hidden');
        elements.paletteContainer.innerHTML = '';
        elements.generateBtn.disabled = true;
        elements.surpriseBtn.disabled = true;
        elements.postGenerationTools.classList.add('hidden');
        startStatusUpdates();

        const generationData = {
            style: elements.styleSelect.value,
            resolution: document.getElementById('resolution-select').value,
            seed: parseInt(elements.seedInput.value, 10),
            color: elements.colorInput.value,
            steps: 4,
        };

        try {
            const response = await fetch(`${API_URL}/generate-wallpaper/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(generationData),
            });

            if (!response.ok) {
                throw new Error(`Server error! Status: ${response.status}`);
            }

            const data = await response.json();

            // Display result
            elements.resultImage.src = data.image;
            elements.resultImage.classList.remove('hidden');

            // Add to floating background
            addFloatingImage(data.image);

            // Show tools and palette
            elements.postGenerationTools.classList.remove('hidden');
            displayColorPalette(data.palette);

            // Add to recents
            recentCreations.unshift({ ...generationData,
                src: data.image
            });
            if (recentCreations.length > MAX_RECENTS) {
                recentCreations.pop();
            }
            renderRecents();

            stopStatusUpdates(' Masterpiece created!');

        } catch (error) {
            console.error('Generation failed:', error);
            stopStatusUpdates(`Error: ${error.message}`);
        } finally {
            elements.loader.classList.add('hidden');
            elements.generateBtn.disabled = false;
            elements.surpriseBtn.disabled = false;
        }
    }

    // **UPDATED** Random Seed Generator with actual API call
    async function updateRandomSeed() {
        try {
            const response = await fetch(`${API_URL}/random-seed/`);
            if (!response.ok) {
                throw new Error('Failed to fetch seed from server.');
            }
            const data = await response.json();
            elements.seedInput.value = data.seed;

            // Visual feedback
            elements.seedInput.style.background = 'rgba(77, 100, 115, 0.2)';
            setTimeout(() => {
                elements.seedInput.style.background = '';
            }, 500);

        } catch (error) {
            console.error('Failed to get random seed:', error);
            elements.seedInput.value = Math.floor(Math.random() * 999999);
        }
    }

    elements.generateBtn.addEventListener('click', performGeneration);
    elements.randomSeedBtn.addEventListener('click', updateRandomSeed);

    elements.surpriseBtn.addEventListener('click', async () => {
        const options = elements.styleSelect.options;
        const randomIndex = Math.floor(Math.random() * options.length);
        elements.styleSelect.value = options[randomIndex].value;
        elements.colorInput.value = "";
        await updateRandomSeed();
        elements.surpriseBtn.style.transform = 'rotate(360deg)';
        setTimeout(() => {
            elements.surpriseBtn.style.transform = '';
            performGeneration();
        }, 500);
    });

    elements.copySeedBtn.addEventListener('click', () => {
        const seedValue = elements.seedInput.value;
        navigator.clipboard.writeText(seedValue).then(() => {
            elements.copySeedFeedback.textContent = 'Copied!';
            elements.copySeedBtn.style.background = 'rgba(77, 100, 115, 0.3)';
            setTimeout(() => {
                elements.copySeedFeedback.textContent = 'Copy Seed';
                elements.copySeedBtn.style.background = '';
            }, 2000);
        });
    });

    elements.downloadBtn.addEventListener('click', () => {
        if (!elements.resultImage.src || elements.resultImage.src.startsWith('http')) return;
        const link = document.createElement('a');
        link.href = elements.resultImage.src;
        const style = elements.styleSelect.value.replace(/\s+/g, '-').toLowerCase();
        const seed = elements.seedInput.value;
        link.download = `wallpaper-${style}-${seed}.png`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        elements.downloadBtn.style.transform = 'scale(1.1)';
        setTimeout(() => {
            elements.downloadBtn.style.transform = '';
        }, 200);
    });

    // Enhanced Input Interactions
    [elements.styleSelect, elements.colorInput, elements.seedInput].forEach(input => {
        input.addEventListener('focus', (e) => {
            e.target.style.transform = 'translateY(-2px)';
        });
        input.addEventListener('blur', (e) => {
            e.target.style.transform = '';
        });
    });

    // Initialize Everything
    createParticles();
    typeText(elements.tagline, "Create unique, high-resolution wallpapers with AI magic ");
    initThemeSelector();

    // Smooth scrolling for better UX
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        const parallax = elements.backgroundContainer;
        const speed = scrolled * 0.5;
        parallax.style.transform = `translateY(${speed}px)`;
    });

    // Add keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        if (e.ctrlKey || e.metaKey) {
            switch (e.key) {
                case 'Enter':
                    e.preventDefault();
                    performGeneration();
                    break;
                case 'r':
                    e.preventDefault();
                    updateRandomSeed();
                    break;
                case 's':
                    e.preventDefault();
                    elements.surpriseBtn.click();
                    break;
            }
        }
    });

    console.log('AI Wallpaper Generator initialized successfully!');
});