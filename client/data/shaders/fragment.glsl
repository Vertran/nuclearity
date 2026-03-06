#version 330 core

in vec2 vUV;
in float vType;

out vec4 FragColor;

uniform vec3 uBaseCol;
uniform vec3 uOutCol;

uniform vec3 uHoverBaseCol;
uniform vec3 uHoverOutCol;

uniform float uHoverState;
uniform float uUseTexture;

uniform sampler2D uTexture;

void main() {
    vec3 startColor = mix(uOutCol, uBaseCol, vType);
    vec3 endColor   = mix(uHoverOutCol, uHoverBaseCol, vType);

    vec3 finalColor = mix(startColor, endColor, uHoverState);
    
    FragColor = mix(vec4(finalColor, 1.0), texture(uTexture, vUV), uUseTexture);
}