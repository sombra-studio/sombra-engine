#version 330

in vec3 frag_normal;

void main() {
    vec3 color_normal = (normalize(frag_normal) + 1) / 2;
    gl_FragColor = vec4(color_normal, 1.0);
}
