#version 430

layout(binding = 0) uniform sampler2D ambient_map;
layout(binding = 1) uniform sampler2D diffuse_map;
layout(binding = 2) uniform sampler2D specular_map;
layout(binding = 3) uniform sampler2D bump_map;

struct Material {
    vec3 ambient;
    vec3 diffuse;
    vec3 specular;
    float specular_exponent;
    float bump_scale;
    bool has_bump_map;
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
in mat3 TBN;

out vec4 final_color;

vec3 calculate_normal_from_bump() {
    float lod_scale = textureQueryLod(bump_map, frag_tex_coords).y;
    float u_dist_for_pixel = 1.0 / (textureSize(bump_map, 0).x * lod_scale);
    float v_dist_for_pixel = 1.0 / (textureSize(bump_map, 0).y * lod_scale);
    float height_left = texture(
        bump_map, frag_tex_coords + vec2(-1.0 * u_dist_for_pixel, 0.0)
    ).r;
    float height_right = texture(
        bump_map, frag_tex_coords + vec2(1.0 * u_dist_for_pixel, 0.0)
    ).r;
    float height_down = texture(
        bump_map, frag_tex_coords + vec2(0.0, -1.0 * v_dist_for_pixel)
    ).r;
    float height_up = texture(
        bump_map, frag_tex_coords + vec2(0.0, 1.0 * v_dist_for_pixel)
    ).r;
    float dx = (height_right - height_left) * material.bump_scale;
    float dy = (height_up - height_down) * material.bump_scale;
    vec3 normal = vec3(dx, dy, 1.0);
    return normal;
}

void main() {
    vec3 ambient = material.ambient * texture(ambient_map, frag_tex_coords).rgb;

    // Calculate normal
    vec3 norm = normalize(frag_normal);
    if (material.has_bump_map) {
        norm = calculate_normal_from_bump();
        norm = normalize(TBN * norm);
    }

    // Calculate diffuse
    vec3 l = normalize(light.position - frag_pos);
    float lambert = clamp(dot(norm, l), 0.0, 1.0);
    vec3 diffuse = material.diffuse * texture(diffuse_map, frag_tex_coords).rgb;

    // Calculate specular
    vec3 v = normalize(eye - frag_pos);
    vec3 h = normalize(l + v);
    float spec_factor = clamp(dot(h, norm), 0.0, 1.0);
    vec3 Ks = max(
        material.specular, texture(specular_map, frag_tex_coords).rgb
    );

    vec3 intensity = light.color * (
        diffuse * lambert + Ks * pow(spec_factor, material.specular_exponent)
    );
    vec3 color = diffuse * ambient + intensity;
    vec3 result = clamp(color, 0.0, 1.0);
    final_color = vec4(result, 1.0);
}