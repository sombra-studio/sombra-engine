#version 330

const int MAX_BONES = 100;
const int MAX_WEIGHTS = 4;


uniform WindowBlock
{
    mat4 projection;
    mat4 view;
} window;

uniform mat4 model;
uniform mat4 bones_transforms[MAX_BONES];

in vec3 position;
in vec2 tex_coords;
in vec3 normal;
in vec3 tangent;
in ivec4 bones_ids;
in vec4 weights;

out vec3 frag_pos;
out vec2 frag_tex_coords;
out vec3 frag_normal;
out mat3 TBN;

void main()
{
    // Calculate new vectors with influence of bones
    mat4 total_bones_transform = mat4(0.0);
    for (int i = 0; i < MAX_WEIGHTS; i++) {
        total_bones_transform += bones_transforms[bones_ids[i]] * weights[i];
    }

    frag_pos = vec3(total_bones_transform * model * vec4(position, 1.0));
    frag_tex_coords = tex_coords;
    frag_normal = normalize(mat3(transpose(inverse(
        total_bones_transform * model
    ))) * normal);
    vec3 T = normalize(mat3(transpose(inverse(
        total_bones_transform * model
    ))) * tangent);
    vec3 N = frag_normal;
    // re-orthogonalize T with respect to N
    T = normalize(T - dot(T, N) * N);
    // then retrieve perpendicular vector B with the cross product of T and N
    vec3 B = cross(N, T);
    TBN = mat3(T, B, N);
    gl_Position = (
        window.projection * window.view * model *
        total_bones_transform * vec4(position, 1.0)
    );
}
