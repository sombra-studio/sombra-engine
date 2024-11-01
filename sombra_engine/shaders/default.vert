#version 330

uniform WindowBlock
{
    mat4 projection;
    mat4 view;
} window;

uniform mat4 model;

in vec3 position;
in vec2 tex_coords;
in vec3 normal;
in vec3 tangent;

out vec3 frag_pos;
out vec2 frag_tex_coords;
out vec3 frag_normal;
out mat3 TBN;

void main()
{
    frag_pos = vec3(model * vec4(position, 1.0));
    frag_tex_coords = tex_coords;
    frag_normal = normalize(mat3(transpose(inverse(model))) * normal);
    vec3 T = normalize(mat3(transpose(inverse(model))) * tangent);
    vec3 N = frag_normal;
    // re-orthogonalize T with respect to N
    T = normalize(T - dot(T, N) * N);
    // then retrieve perpendicular vector B with the cross product of T and N
    vec3 B = cross(N, T);
    TBN = mat3(T, B, N);
    gl_Position = window.projection * window.view * model * vec4(position, 1.0);
}
