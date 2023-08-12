#version 330

uniform Material {
    vec3 ambient;
    vec3 diffuse;
    vec3 specular;
    float specular_exponent;
} material;

uniform Light {         // TODO how do you deal with changing between multiple lights? T_T
    vec3 position;
    vec3 color;
} light;


in vec3 fragPos;
in vec3 fragNormal;

const float c0 = 0.2;

void main() {
    vec3 ambient = material.ambient;
    vec3 l = normalize(light.position - fragPos);
    float diffuse = clamp(dot(l, fragNormal), 0.0, 1.0) * material.diffuse;
    vec3 color = ligth.color * (c0 * ambient + (1.0 - c0) * diffuse);
    gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0);
}
