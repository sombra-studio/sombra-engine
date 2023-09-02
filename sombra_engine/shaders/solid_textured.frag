#version 330


uniform sampler2D diffuseMap;

struct Material {
    vec3 diffuse;
};

uniform Material material;
in vec2 fragTexCoords;
out vec4 finalColor;

void main() {
    finalColor = (
        texture(diffuseMap, fragTexCoords) * vec4(material.diffuse, 1.0)
    );
}