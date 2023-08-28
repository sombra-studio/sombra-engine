#version 330

uniform Material {
    vec3 ambient;
    vec3 diffuse;
    vec3 specular;
    float specular_exponent;
} material;

uniform Light {
    vec3 position;
    vec3 color;
} light;

in vec3 fragPos;
in vec3 fragNormal;

const float c0 = 0.2;

out vec4 finalColor;

void main() {
    vec3 ambient = material.ambient;
    vec3 l = normalize(light.position - fragPos);
    vec3 diffuse = clamp(dot(l, fragNormal), 0.0, 1.0) * material.diffuse;
    vec3 color = light.color * (c0 * ambient + (1.0 - c0) * diffuse);
    finalColor = vec4(color, 1.0);
    //finalColor = vec4(1.0);
}