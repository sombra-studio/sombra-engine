#version 330

uniform mat4 light_transform;
uniform mat4 model;

in vec3 position;

void main()
{
  gl_Position = light_transform * model * vec4(position, 1.0);
}
