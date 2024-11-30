#version 330

uniform WindowBlock
{
    mat4 projection;
    mat4 view;
} window;

in vec3 position;
in vec3 color;

out vec3 frag_color;

void main()
{
    frag_color = color;
    gl_Position = window.projection * window.view * vec4(position, 1.0);
}
