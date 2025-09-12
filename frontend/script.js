document.addEventListener('DOMContentLoaded', () => {
    const allElements = {
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
    };
    const API_URL = 'http://127.0.0.1:8000';

    let backgroundImages = [];
    const MAX_BG_IMAGES = 5;
    let recentCreations = [];
    const MAX_RECENTS = 5;
    let statusInterval;

    const typeText = (element, text, speed = 75) => {
        let i = 0;
        element.innerHTML = ""; 
        const typing = setInterval(() => {
            if (i < text.length) {
                element.innerHTML += text.charAt(i);
                i++;
            } else {
                clearInterval(typing);
            }
        }, speed);
    };
    typeText(allElements.tagline, "Create unique, high-resolution wallpapers with AI.");

    const addFloatingImage = (imageUrl) => {
        const img = document.createElement('img');
        img.src = imageUrl;
        img.className = 'floating-bg';
        if (backgroundImages.length >= MAX_BG_IMAGES) {
            const oldImg = backgroundImages.shift();
            oldImg.style.opacity = 0;
            setTimeout(() => oldImg.remove(), 1000);
        }
        const size = Math.random() * 200 + 150;
        img.style.width = `${size}px`;
        img.style.height = 'auto';
        img.style.top = `${Math.random() * 100 - 10}%`;
        img.style.left = `${Math.random() * 100 - 10}%`;
        img.style.animationDuration = `${Math.random() * 20 + 25}s`;
        allElements.backgroundContainer.appendChild(img);
        backgroundImages.push(img);
    };

    const startStatusUpdates = () => {
        const messages = [
            "Painting with pixels...",
            "Consulting the digital muse...",
            "Reticulating splines...",
            "Unleashing creative algorithms...",
            "Herding electrons...",
            "Almost there..."
        ];
        let msgIndex = 0;
        allElements.statusDisplay.textContent = messages[msgIndex];
        statusInterval = setInterval(() => {
            msgIndex = (msgIndex + 1) % messages.length;
            allElements.statusDisplay.textContent = messages[msgIndex];
        }, 2000);
    };

    const stopStatusUpdates = (finalMessage) => {
        clearInterval(statusInterval);
        allElements.statusDisplay.textContent = finalMessage;
    };

    const renderRecents = () => {
        if (recentCreations.length === 0) return;
        allElements.recentGallery.innerHTML = "";
        recentCreations.forEach(creation => {
            const img = document.createElement('img');
            img.src = creation.src;
            img.title = `Style: ${creation.style}, Seed: ${creation.seed}`;
            img.addEventListener('click', () => {
                allElements.styleSelect.value = creation.style;
                allElements.seedInput.value = creation.seed;
                allElements.colorInput.value = creation.color || "";
                window.scrollTo({ top: 0, behavior: 'smooth' });
            });
            allElements.recentGallery.appendChild(img);
        });
        allElements.recentCreationsSection.classList.remove('hidden');
    };

    const performGeneration = async () => {
        allElements.loader.classList.remove('hidden');
        allElements.resultImage.classList.add('hidden');
        allElements.paletteContainer.innerHTML = '';
        allElements.generateBtn.disabled = true;
        allElements.surpriseBtn.disabled = true;
        allElements.postGenerationTools.classList.add('hidden');
        startStatusUpdates();

        const generationData = {
            style: allElements.styleSelect.value,
            resolution: document.getElementById('resolution-select').value,
            seed: parseInt(allElements.seedInput.value, 10),
            color: allElements.colorInput.value,
            steps: 4,
        };

        try {
            const response = await fetch(`${API_URL}/generate-wallpaper/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(generationData),
            });
            if (!response.ok) { throw new Error(`Server error! Status: ${response.status}`); }
            const data = await response.json();
            
            allElements.resultImage.src = data.image;
            allElements.resultImage.classList.remove('hidden');
            addFloatingImage(data.image);
            allElements.postGenerationTools.classList.remove('hidden');
                        data.palette.forEach(color => {
                const wrapper = document.createElement('div');
                wrapper.className = 'color-swatch-wrapper';

                const swatch = document.createElement('div');
                swatch.className = 'color-swatch';
                swatch.style.backgroundColor = color;
                swatch.title = `Click to copy ${color}`;
                
                const hexCode = document.createElement('div');
                hexCode.className = 'hex-code';
                hexCode.textContent = color;

                swatch.addEventListener('click', () => {
                    navigator.clipboard.writeText(color);
                    hexCode.textContent = 'Copied!';
                    setTimeout(() => { hexCode.textContent = color; }, 1500);
                });
                
                wrapper.appendChild(swatch);
                wrapper.appendChild(hexCode); 
                paletteContainer.appendChild(wrapper);
            });
            
            recentCreations.unshift({ ...generationData, src: data.image });
            if (recentCreations.length > MAX_RECENTS) {
                recentCreations.pop();
            }
            renderRecents();

            stopStatusUpdates('Done! ✨');
        } catch (error) {
            console.error('Failed to generate wallpaper:', error);
            stopStatusUpdates(`Error: ${error.message}`);
        } finally {
            allElements.loader.classList.add('hidden');
            allElements.generateBtn.disabled = false;
            allElements.surpriseBtn.disabled = false;
        }
    };

    const updateRandomSeed = async () => {
        try {
            const response = await fetch(`${API_URL}/random-seed/`);
            const data = await response.json();
            allElements.seedInput.value = data.seed;
        } catch (error) {
            console.error('Failed to get random seed:', error);
            allElements.seedInput.value = Math.floor(Math.random() * 999999);
        }
    };

    allElements.generateBtn.addEventListener('click', performGeneration);
    allElements.randomSeedBtn.addEventListener('click', updateRandomSeed);
    
    allElements.surpriseBtn.addEventListener('click', async () => {
        const options = allElements.styleSelect.options;
        const randomIndex = Math.floor(Math.random() * options.length);
        allElements.styleSelect.value = options[randomIndex].value;
        allElements.colorInput.value = ""; 
        await updateRandomSeed();
        performGeneration();
    });
    allElements.copySeedBtn.addEventListener('click', () => {
        const seedValue = seedInput.value;
        navigator.clipboard.writeText(seedValue).then(() => {
            copySeedFeedback.textContent = 'Copied!';
            setTimeout(() => { copySeedFeedback.textContent = 'Copy Seed'; }, 2000);
        });
    });

    allElements.downloadBtn.addEventListener('click', () => {
        const link = document.createElement('a');
        link.href = resultImage.src;
        const style = styleSelect.value.replace(/\s+/g, '-').toLowerCase();
        const seed = seedInput.value;
        link.download = `wallpaper-${style}-${seed}.png`;
        
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    });
});