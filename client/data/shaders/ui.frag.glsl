#version 330 core

in vec2 vUV;
in float vType;

out vec4 FragColor;

uniform vec3 uBaseCol;
uniform vec3 uOutCol;
uniform vec3 uHoverBaseCol;
uniform vec3 uHoverOutCol;
uniform float uHoverState;
uniform int uUseTexture;
uniform sampler2D uTexture;

void main() {
    vec3 baseColor = mix(uOutCol, uBaseCol, vType);
    vec3 hoverColor = mix(uHoverOutCol, uHoverBaseCol, vType);
    vec3 finalColor = mix(baseColor, hoverColor, uHoverState);

    if (uUseTexture == 1) {
        vec4 texColor = texture(uTexture, vUV);
        FragColor = mix(vec4(finalColor, 1.0), texColor, texColor.a);
    } else {
        FragColor = vec4(finalColor, 1.0);
    }
}