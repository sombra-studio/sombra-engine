#version 330

in vec3 frag_color;
out vec4 final_color;

void main() {
    final_color = vec4(frag_color, 1.0);
}
