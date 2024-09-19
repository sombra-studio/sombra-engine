#version 330


uniform sampler2D diffuse_map;

struct Material {
    vec3 diffuse;
};

uniform Material material;
in vec2 frag_tex_coords;
out vec4 final_color;

void main() {
    finalColor = (
        texture(diffuse_map, frag_tex_coords) * vec4(material.diffuse, 1.0)
    );
}