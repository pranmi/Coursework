in vec3 vcsNormal;
in vec3 vcsPosition;
in vec2 texCoord;
in vec4 lightSpaceCoords;

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

// Added ShadowMap
uniform sampler2D shadowMap;
uniform float textureSize;

//Q1d do the shadow mapping
//Q1d iii do PCF
// Returns 1 if point is occluded (saved depth value is smaller than fragment's depth value)

vec3 getShadowMapCoords() {
    vec3 projCoords = lightSpaceCoords.xyz / lightSpaceCoords.w;
    projCoords = projCoords * 0.5 + 0.5;
	projCoords.xy = clamp(projCoords.xy, 0.0, 1.0);
    return projCoords;
}


float inShadow(vec3 fragCoord) {
    float depthFromShadowMap = texture(shadowMap, fragCoord.xy).r;
    float bias = 0.001;
    return fragCoord.z - bias > depthFromShadowMap ? 1.0 : 0.0;
}




// TODO: Returns a value in [0, 1], 1 indicating all sample points are occluded
float calculateShadow() {
    vec3 fragCoord = getShadowMapCoords();
    float shadow = 0.0;

    float bias = 0.0005;
    float texelSize = 1.0 / 1024.0;
    for(int x = -3; x <= 3; ++x) {
        for(int y = -3; y <= 3; ++y) {
            vec2 offset = vec2(float(x), float(y)) * texelSize;
            vec2 sampleUV = fragCoord.xy + offset; 
            
            // Sample depth from shadow map
            float closestDepth = texture(shadowMap, sampleUV).r;

            // Compare fragment depth with depth in shadow map
            if(fragCoord.z - bias > closestDepth)
                shadow += 1.0;
        }
    }
    shadow /= 36.0;

    // Return 1 = lit, 0 = in shadow
    return 1.0 - shadow;
}


void main() {
	//PRE-CALCS
	vec3 N = normalize(vcsNormal);
	vec3 Nt = normalize(texture(normalMap, texCoord).xyz * 2.0 - 1.0);
	vec3 L = normalize(vec3(viewMatrix * vec4(lightDirection, 0.0)));
	vec3 V = normalize(-vcsPosition);
	vec3 H = normalize(V + L);

	//AMBIENT
	vec3 light_AMB = ambientColor * kAmbient;

	//DIFFUSE
	vec3 diffuse = kDiffuse * lightColor;
	vec3 light_DFF = diffuse * max(0.0, dot(N, L));

	//SPECULAR
	vec3 specular = kSpecular * lightColor;
	vec3 light_SPC = specular * pow(max(0.0, dot(H, N)), shininess);

	//SHADOW
	// TODO:
	//vec3 shadowCoords = getShadowMapCoords();
	//float shadow = 1.0 - inShadow(shadowCoords);

	float shadow = calculateShadow();


	//TOTAL
	vec3 colorSample = texture(colorMap, texCoord).rgb * (light_DFF + light_SPC);
	vec3 TOTAL = light_AMB*colorSample + shadow * (colorSample);

	vec3 projCoords = getShadowMapCoords();
	gl_FragColor = vec4(TOTAL,1.0);


}