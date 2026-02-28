#version 330 core
out vec4 FragColor;
in vec3 ourColor;

void main() {
    // Устанавливаем итоговый цвет пикселя (r, g, b, alpha)
    FragColor = vec4(ourColor, 1.0);
}