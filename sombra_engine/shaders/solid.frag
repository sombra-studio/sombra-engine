#version 330

struct Material {
    vec3 diffuse;
};

uniform Material material;

out vec4 color;

void main() {
    color = vec4(material.diffuse, 1.0);
}
