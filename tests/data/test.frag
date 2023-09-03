#version 330

struct Material {
    vec3 diffuse;
};

uniform Material material;

out vec4 f_color;

void main() {
    f_color = vec4(material.diffuse, 1.0);
}
