#version 330

uniform mat4 mv;
uniform mat4 proj;

in vec3 position;

void main()
{
    gl_Position = proj * mv * vec4(position, 1.0);
}
