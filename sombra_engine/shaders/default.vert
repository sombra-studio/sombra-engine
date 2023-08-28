#version 330

uniform WindowBlock
{
    mat4 projection;
    mat4 view;
} window;

in vec3 position;
in vec2 texCoords;
in vec3 normal;

out vec3 fragPos;
out vec2 fragTexCoords;
out vec3 fragNormal;

void main()
{
    gl_Position = window.projection * window.view * vec4(position, 1.0);
    fragPos = position;
    fragTexCoords = texCoords;
    fragNormal = normal;
}
