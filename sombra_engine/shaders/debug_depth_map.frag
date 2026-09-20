#version 330 core

uniform sampler2D depth_map;

in vec2 frag_tex_coords;

out vec4 final_color;

void main() {
    float depth = texture(depth_map, frag_tex_coords).r;
    final_color = vec4(vec3(depth), 1.0);
}
