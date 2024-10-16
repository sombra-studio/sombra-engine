#version 330

uniform sampler2D ambient_map;
uniform sampler2D diffuse_map;

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

in vec3 frag_pos;
in vec2 frag_tex_coords;
in vec3 frag_normal;


out vec4 final_color;

void main() {
    vec3 ambient = material.ambient * texture(ambient_map, frag_tex_coords).rgb;
    vec3 l = normalize(light.position - frag_pos);
    vec3 norm = normalize(frag_normal);
    float lambert = max(dot(norm, l), 0.0);
    vec3 intensity = light.color * lambert;
    vec3 diffuse = material.diffuse * texture(diffuse_map, frag_tex_coords).rgb;
    vec3 diffuse_color = diffuse * intensity;
    vec3 ambient_color = diffuse * ambient;
    vec3 color = max(ambient_color, diffuse_color);
    vec3 result = clamp(color, 0.0, 1.0);
    final_color = vec4(result, 1.0);
}