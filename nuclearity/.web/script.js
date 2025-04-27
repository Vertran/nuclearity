const noise = document.createElement('div');
noise.style.position = 'absolute';
noise.style.top = '0';
noise.style.left = '0';
noise.style.width = '100vw';
noise.style.height = '100vh';
noise.style.backgroundImage = 'url("https://upload.wikimedia.org/wikipedia/commons/7/76/1k_Dissolve_Noise_Texture.png")';
noise.style.backgroundRepeat = 'repeat';
noise.style.opacity = '0.1';
noise.style.zIndex = '9999';  // Make sure it's on top of other elements

// Test if image loads
const testImage = new Image();
testImage.onload = () => {
    console.log('Noise texture loaded successfully');
};
testImage.onerror = () => {
    console.error('Failed to load noise texture');
};
testImage.src = 'https://upload.wikimedia.org/wikipedia/commons/7/76/1k_Dissolve_Noise_Texture.png';

document.body.appendChild(noise);

function animateNoise() {
    noise.style.left = (Math.random() * window.innerWidth) + 'px';
    noise.style.top = (Math.random() * window.innerHeight) + 'px';
    requestAnimationFrame(animateNoise);
}

animateNoise();