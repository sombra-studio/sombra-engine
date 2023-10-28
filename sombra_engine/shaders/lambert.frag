#version 330

uniform sampler2D ambientMap;
uniform sampler2D diffuseMap;
uniform sampler2D specularMap;

struct Material {
    vec3 ambient;
    vec3 diffuse;
};

uniform Material material;

struct Light {
    vec3 position;
    vec3 color;
};

uniform Light light;

in vec3 fragPos;
in vec2 fragTexCoords;
in vec3 fragNormal;


out vec4 finalColor;

void main() {
    vec3 ambient = light.color * (
        material.ambient * texture(ambientMap, fragTexCoords).rgb
    );
    vec3 l = normalize(light.position - fragPos);
    vec3 norm = normalize(fragNormal);
    float diff = max(dot(l, fragNormal), 0.0);
    vec3 diffuse = light.color * diff * (
        material.diffuse * texture(diffuseMap, fragTexCoords).rgb
    );
    vec3 result = ambient + diffuse;
    finalColor = vec4(result, 1.0);
//    finalColor = vec4(diffColor, 1.0);
}