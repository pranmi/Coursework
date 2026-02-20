// Uniform to transform vertices into light space
uniform mat4 lightMatrix;

varying vec4 vLightSpacePos;

void main() {
    vLightSpacePos = lightMatrix * modelMatrix * vec4(position, 1.0);

    gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
}
