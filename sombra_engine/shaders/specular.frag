#version 420


layout(binding = 2) uniform sampler2D specular_map;

struct Material {
    vec3 specular;
    float specular_exponent;
};

uniform Material material;

struct Light {
    vec3 position;
    vec3 color;
};

uniform Light light;
uniform vec3 eye;

in vec3 frag_pos;
in vec2 frag_tex_coords;
in vec3 frag_normal;


out vec4 final_color;

void main() {
    vec3 l = normalize(light.position - frag_pos);
    vec3 norm = normalize(frag_normal);
    vec3 v = normalize(eye - frag_pos);
    vec3 h = normalize(l + v);
    float spec_factor = clamp(dot(h, norm), 0.0, 1.0);
    vec3 Ks = max(
        material.specular, texture(specular_map, frag_tex_coords).rgb
    );
    vec3 intensity = light.color * (
        Ks * pow(spec_factor, material.specular_exponent)
    );
    vec3 result = clamp(intensity, 0.0, 1.0);
    final_color = vec4(result, 1.0);
}