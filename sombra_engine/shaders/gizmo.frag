#version 330

in vec3 frag_color;

void main() {
    gl_FragColor = vec4(frag_color, 1.0);
}