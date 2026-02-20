in vec3 interpolatedNormal;
in vec3 viewPosition;
in vec3 worldPosition;
in vec2 texCoord;
in vec4 lightSpacePos;

uniform vec3 lightColor;
uniform vec3 ambientColor;

uniform float kAmbient;
uniform float kDiffuse;
uniform float kSpecular;
uniform float shininess;

uniform vec3 cameraPos;
uniform vec3 lightPosition;
uniform vec3 lightDirection;

// Textures are passed in as uniforms
uniform sampler2D colorMap;
uniform sampler2D normalMap;

void main() {
	
	vec3 Nt = normalize(texture(normalMap, texCoord).xyz * 2.0 - 1.0);
    vec3 N = normalize(interpolatedNormal);
    vec3 V = normalize(-viewPosition);
	vec3 L = normalize((viewMatrix * vec4(lightDirection, 0.0)).xyz);
	vec3 H = normalize(V + L);

	//AMBIENT
	vec3 light_AMB = kAmbient * ambientColor;

	//DIFFUSE
	vec3 diffuse = kDiffuse * lightColor;
	vec3 light_DFF = diffuse * max(0.0, dot(N, L));

	//SPECULAR
	vec3 specular = kSpecular * lightColor;
	vec3 light_SPC = specular * pow(max(0.0, dot(H, N)), shininess);

	//Here sample from the texture to get the output color
	vec2 uv = vec2(texCoord.x, 1.0 - texCoord.y);
    vec3 texCol = texture(colorMap, uv).rgb;

	//TOTAL
	// TODO: Q1a, sample from texture
	vec3 TOTAL = texCol *(light_AMB + light_DFF + light_SPC);
	vec3 justLight = (light_AMB+ light_DFF) + light_SPC;

	float diff = max(dot(N, L), 0.0);
	gl_FragColor = vec4(TOTAL, 1.0); 
}