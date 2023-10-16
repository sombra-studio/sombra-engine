#version 330

in vec3 fragNormal;

void main() {
    vec3 colorNormal = (fragNormal + 1) / 2;
    gl_FragColor = vec4(colorNormal, 1.0);
}
