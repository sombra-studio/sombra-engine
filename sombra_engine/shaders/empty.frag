#version 330

out float fragment_depth;

void main() {
    fragment_depth = gl_FragCoord.z;
}
