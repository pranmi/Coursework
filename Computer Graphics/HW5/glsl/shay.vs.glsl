out vec3 viewPosition;
out vec3 worldPosition;
out vec3 interpolatedNormal;
out vec2 texCoord;

void main() {
    vec4 vcsPos = modelViewMatrix * vec4(position, 1.0);
    worldPosition = (modelMatrix * vec4(position, 1.0)).xyz;

    viewPosition = (viewMatrix * vec4(worldPosition, 1.0)).xyz;

    interpolatedNormal = normalize(normalMatrix * normal);

    texCoord = uv;

    gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
 }