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
    vec3 pos = aPos;
    
    float dist = distance(pos.xy, uMousePos);
    
    if (dist < 100.0) {
        vec2 dir = normalize(pos.xy - uMousePos);
        float force = (100.0 - dist) / 100.0;
        pos.xy += dir * force * uDistortionStrength;
    }

    gl_Position = uProjection * vec4(pos, 1.0);
    vType = aType;
    vUV = aUV;
}


