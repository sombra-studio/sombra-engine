#version 330

const int MAX_BONES = 100;
const int MAX_WEIGHTS = 4;

uniform mat4 light_transform;
uniform mat4 model;
uniform mat4 bones_transforms[MAX_BONES];

in vec3 position;
in ivec4 bones_ids;
in vec4 weights;

void main()
{
  mat4 total_bones_transform = mat4(0.0);
  for (int i = 0; i < MAX_WEIGHTS; i++) {
      total_bones_transform += bones_transforms[bones_ids[i]] * weights[i];
  }

  gl_Position = light_transform * model * total_bones_transform * vec4(
    position, 1.0
  );
}
