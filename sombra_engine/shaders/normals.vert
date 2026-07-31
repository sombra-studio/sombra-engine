#version 330

uniform WindowBlock
{
    mat4 projection;
    mat4 view;
} window;

in vec3 position;
in vec3 normal;

out vec3 frag_normal;

void main()
{
    frag_normal = normal;
    gl_Position = window.projection * window.view * vec4(position, 1.0);
}
