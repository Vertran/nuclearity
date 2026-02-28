#version 330 core
layout (location = 0) in vec3 aPos;   // Позиция (x, y, z)
layout (location = 1) in vec3 aColor; // Цвет (r, g, b)

out vec3 ourColor;

void main() {
    // Просто прокидываем позицию. 
    // В будущем тут будет умножение на матрицу проекции
    gl_Position = vec4(aPos, 1.0);
    ourColor = aColor;
}