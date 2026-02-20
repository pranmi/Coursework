uniform vec3 cameraPos;
out vec3 wcsPosition;

void main() {
	// TODO: Q1b
	vec3 worldPos = position + cameraPos;
	wcsPosition = normalize(worldPos - cameraPos);
	gl_Position = projectionMatrix * mat4(mat3(viewMatrix)) * vec4(position, 1.0); //turn viewMatrix into mat3 to ignore translation for "infinitely far" effect
}