#version 330 core

uniform float uAlpha;
in vec3 vertexColor;
out vec4 FragColor;

void main() {
    FragColor = vec4(vertexColor * (uAlpha*0.5), uAlpha);
}