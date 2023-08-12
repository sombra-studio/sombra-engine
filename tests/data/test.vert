#version 330

uniform mat4 mv;
uniform mat4 proj;

in vec3 position;
in vec3 normal;
in vec2 tex_coords;

out vec3 fragPos;
out vec3 fragNormal;
out vec2 texCoords;

void main()
{
    gl_Position = proj * mv * vec4(position, 1.0);
    fragPos = position;
    fragNormal = normal;
    texCoords = tex_coords;
}
