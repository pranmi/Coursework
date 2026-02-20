//Q1d implement the whole thing to map the depth texture to a quad
// TODO:

uniform mat4 lightProjMatrix;
uniform mat4 lightViewMatrix;

out vec2 vUv;
void main() {
    vUv = uv;
    gl_Position = vec4(position.xy, 0.0, 1.0);
}