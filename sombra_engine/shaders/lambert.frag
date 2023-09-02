#version 330

uniform sampler2D ambientMap;
uniform sampler2D diffuseMap;
uniform sampler2D specularMap;

struct Material {
    vec3 ambient;
    vec3 diffuse;
    vec3 specular;
    float specular_exponent;
};

uniform Material material;

//struct Light {
//    vec3 position;
//    vec3 color;
//};
//
//uniform Light light;

in vec3 fragPos;
in vec2 fragTexCoords;
in vec3 fragNormal;

const float c0 = 0.2;   // Barycentric shading parameter

out vec4 finalColor;

void main() {
//    vec3 ambient = material.ambient * texture(ambientMap, fragTexCoords).rgb;
//    vec3 l = normalize(light.position - fragPos);
//    float nDotL = clamp(dot(l, fragNormal), 0.0, 1.0);
//    vec3 diffuse = nDotL * (
//        material.diffuse * texture(diffuseMap, fragTexCoords).rgb
//    );
//    vec3 color = light.color * (c0 * ambient + (1.0 - c0) * diffuse);
    finalColor = texture(diffuseMap, fragTexCoords) * vec4(
        material.diffuse, 1.0
    );
//    finalColor = vec4(fragNormal, 1.0);
//    finalColor = vec4(1.0, 0.0, 1.0, 1.0);
}