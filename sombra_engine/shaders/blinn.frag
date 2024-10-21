#version 330

uniform sampler2D ambient_map;
uniform sampler2D diffuse_map;
uniform sampler2D specular_map;

struct Material {
    vec3 ambient;
    vec3 diffuse;
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
    vec3 ambient = material.ambient * texture(ambient_map, frag_tex_coords).rgb;

    // Calculate diffuse
    vec3 l = normalize(light.position - frag_pos);
    vec3 norm = normalize(frag_normal);
    float lambert = clamp(dot(norm, l), 0.0, 1.0);
    vec3 diffuse = material.diffuse * texture(diffuse_map, frag_tex_coords).rgb;

    // Calculate specular
    vec3 v = normalize(eye - frag_pos);
    vec3 h = normalize(l + v);
    float spec_factor = clamp(dot(h, norm), 0.0, 1.0);
    vec3 Ks = max(
        material.specular, texture(specular_map, frag_tex_coords).rgb
    );
//    vec3 Ks = vec3(0.0, 0.0, 0.0);

    vec3 intensity = light.color * (
        diffuse * lambert + Ks * pow(spec_factor, material.specular_exponent)
    );
    vec3 color = diffuse * ambient + intensity;
    vec3 result = clamp(color, 0.0, 1.0);
    final_color = vec4(result, 1.0);
}