#version 330

uniform WindowBlock
{
    mat4 projection;
    mat4 view;
} window;

in vec3 position;
in vec2 tex_coords;
in vec3 normal;

out vec3 frag_pos;
out vec2 frag_tex_coords;
out vec3 frag_normal;

void main()
{
    frag_pos = position;
    frag_tex_coords = tex_coords;
    frag_normal = normal;
    gl_Position = window.projection * window.view * vec4(position, 1.0);
}
