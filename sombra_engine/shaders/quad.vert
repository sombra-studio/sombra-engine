#version 330

in vec3 position;
in vec2 tex_coords;

out vec2 frag_tex_coords;

void main() {
    frag_tex_coords = tex_coords;
    gl_Position = vec4(position, 1.0);
}
