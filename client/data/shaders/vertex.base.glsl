#version 330 core

layout(location = 0) in vec3 aPos;
layout(location = 1) in vec2 aUV;
layout(location = 2) in float aType;

out float vType;
out vec2 vUV;

uniform mat4 uProjection;
uniform vec2 uMousePos; 
uniform float uDistortionStrength;

void main() {
    gl_Position = uProjection * vec4(aPos, 1.0);
    vType = aType;
    vUV = aUV;
}


