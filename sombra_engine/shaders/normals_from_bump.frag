#version 430

layout(binding = 3) uniform sampler2D bump_map;

struct Material {
    float bump_scale;
    bool has_bump_map;
};

uniform Material material;

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
    // Calculate normal
    vec3 norm = normalize(frag_normal);
    if (material.has_bump_map) {
        norm = calculate_normal_from_bump();
        norm = normalize(TBN * norm);
    }

    // Convert normal to color
    vec3 normal_color = (norm + 1) / 2;
    final_color = vec4(normal_color, 1.0);
}