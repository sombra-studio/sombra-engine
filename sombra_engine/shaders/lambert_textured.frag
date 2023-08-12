#version 330

uniform TexturedMaterial {
    sampler2D ambient_map;
    sampler2D diffuse_map;
    sampler2D specular_map;
    float specular_exponent;
} material;


void main() {
    gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0);
}
