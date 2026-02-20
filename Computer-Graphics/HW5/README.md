See [A5.pdf](A5.pdf) for the assignment specifications.
Pranith Mullapudi pxm220087
Q1a:
Most of the work is done, just need to pass in the shayD texture to the object and also sample the texture in the fragment shader.
The original lighting in the fs worked but I thought there was a bug and rewrote it for no reason :( since the issue ended up being that the colors weren't being passed in
and thus whenever they were used in the lighting calcs made them 0. After fixing that it worked though
Important code changes:
A5.js:

Adding these to the ShayDMaterial:
ambientColor: ambientColorUniform,
lightColor: lightColorUniform,
colorMap: shayDTextureUniform,
normalMap: shayDNormalTexture

shay.vs: //calculating the different things that will be needed in the fragment shader
vec4 vcsPos = modelViewMatrix * vec4(position, 1.0);
worldPosition = (modelMatrix * vec4(position, 1.0)).xyz;

viewPosition = (viewMatrix * vec4(worldPosition, 1.0)).xyz;

interpolatedNormal = normalize(normalMatrix * normal);

texCoord = uv; 

shay.fs://sampling the texture using the uv and combining it with the lighting for the final color
//Here sample from the texture to get the output color
	vec2 uv = vec2(texCoord.x, 1.0 - texCoord.y);
    vec3 texCol = texture(colorMap, uv).rgb;

	//TOTAL
	// TODO: Q1a, sample from texture
	vec3 TOTAL = texCol *(light_AMB + light_DFF + light_SPC);
	vec3 justLight = (light_AMB+ light_DFF) + light_SPC;

	float diff = max(dot(N, L), 0.0);
	gl_FragColor = vec4(TOTAL, 1.0); 

Q1b:
For this just needed to load the different sides of the cube into the material and create the mesh 
Then passing in that cube to the material along with the camera position, also had to remove the 
translation in the viewmatrix for gl_position to achieve the infinitely far away effect

Changes:
A5.js:
const loader = new THREE.CubeTextureLoader(); //loading the actual images into the cubemap
const skyboxCubemap = loader.load([
  'images/cubemap/posx.jpg',
  'images/cubemap/negx.jpg',
  'images/cubemap/posy.jpg',
  'images/cubemap/negy.jpg',
  'images/cubemap/posz.jpg',
  'images/cubemap/negz.jpg',
])
const skyboxMaterial = new THREE.ShaderMaterial({
    uniforms: {
        skybox: { value: skyboxCubemap }, //creating the material and passing in the cubemap and camera
        cameraPos: { value: camera.position }
    },
    side: THREE.BackSide 
});
skyboxMaterial.depthWrite = false; //making sure it's behind
const skyboxGeometry = new THREE.BoxGeometry(100, 100, 100); // size doesn’t matter
const skyboxMesh = new THREE.Mesh(skyboxGeometry, skyboxMaterial); //creating the actual mesh
skyboxMesh.renderOrder = -1; //making sure it renders behind everything actually in the scene
scene.add(skyboxMesh);

skybox.vs:
vec3 worldPos = position + cameraPos;
wcsPosition = normalize(worldPos - cameraPos); //just calculating the position to be used

skybox.fs://using wcsposition to sample from the skybox and put into the fragcolor
vec3 texColor = texture(skybox, wcsPosition).rgb;
gl_FragColor = vec4(texColor, 1.0);  //Q1b looking up shader color from texturemap

Q1C
Guess I didn't learn my lesson from the last one since I ended up wasting time on trying to buxfig the shaders when the issue was with my uniform passing :(
Overall process was 1. adding the skybox and camera position to the material, 2. Doing calculating the reflection vector to use to sample the cubemap
3. sampling the cubemap and passing it's color into the final color for the shader
Changes:
A5.js://Adding needed uniforms to be passed in
skybox: { value: skyboxCubemap },
cameraPos: { value: camera.position }

envmap.fs:
uniform vec3 cameraPos; //new uniform passed in from A5.js changes

uniform samplerCube skybox; //new uniform passed in from A5.js changes

vec3 N = normalize(vcsNormal);
vec3 V = normalize(cameraPos - vcsPosition); // view vector
vec3 R = reflect(-V, N); //calculating reflect ray which "hits the cubemap"

R.x = -R.x; //reflecting x since it was specified in the assignment but I can't tell much of a difference to be honest

vec3 sampleColor = texture(skybox, R).rgb; //Use reflection ray and cubemap to sample the color

gl_FragColor = vec4(sampleColor, 1.0); //pass that color to the final FragColor

Q1d:
First part, had to update the render passes and the render shaders to get the actual shadow map

code changes:
A5:
    // Q1d Visualise the shadow map
    // TODO: First pass to get the depth value
    if (!shadowRenderTarget) {
        shadowRenderTarget = new THREE.WebGLRenderTarget(1024, 1024);
        shadowRenderTarget.depthBuffer = true;
        shadowRenderTarget.depthTexture = new THREE.DepthTexture();
        shadowRenderTarget.depthTexture.type = THREE.UnsignedShortType;
    }
    // First pass: render shadowScene to the shadow map
    renderer.setRenderTarget(shadowRenderTarget);
    renderer.clear();
    renderer.render(shadowScene, shadowCam);
    renderer.setRenderTarget(null);


    // TODO: Second Pass, visualise shadow map to quad
    postMaterial.uniforms.tDepth.value = shadowRenderTarget.depthTexture;
    postMaterial.uniforms.textureSize.value = 1024.0;

    
    renderer.setRenderTarget(null);
    renderer.clear();
    renderer.render(postScene, postCam); //Added these shadowRenderTarget to create the shadow map and visualize it in scene 2

render.vs:
//Q1d implement the whole thing to map the depth texture to a quad
// TODO:

uniform mat4 lightProjMatrix;
uniform mat4 lightViewMatrix;

out vec2 vUv;
void main() {
    vUv = uv; //added uv pass
    gl_Position = vec4(position.xy, 0.0, 1.0);
}

render.fs
float depth = texture(tDepth, vUv).r; //used passed uv to render the depth (shadows)
gl_FragColor = vec4(vec3(depth), 1.0); 

Then for part two, had to apply that shadow map by using a depth check

A5.js: //These changes are also for the last part with the smoothing, pretty much the same but also making sure the different materials involved with the shadows have the right uniforms to be used.
   // Q1d Do the multipass shadowing

    if (!shadowRenderTarget) {
        shadowRenderTarget = new THREE.WebGLRenderTarget(1024, 1024);
        shadowRenderTarget.depthBuffer = true;
        shadowRenderTarget.depthTexture = new THREE.DepthTexture();
        shadowRenderTarget.depthTexture.type = THREE.UnsignedShortType;
    }

    // TODO: First pass
    renderer.setRenderTarget(shadowRenderTarget);
    renderer.clear();
    renderer.render(shadowScene, shadowCam);
    renderer.setRenderTarget(null);

    floorMaterial.uniforms.shadowMap.value = shadowRenderTarget.depthTexture;
    floorMaterial.uniforms.lightViewMatrix.value.copy(shadowCam.matrixWorldInverse);
    floorMaterial.uniforms.lightProjMatrix.value.copy(shadowCam.projectionMatrix);

    shayDMaterial.uniforms.shadowMap.value = shadowRenderTarget.depthTexture;
    shayDMaterial.uniforms.lightViewMatrix.value.copy(shadowCam.matrixWorldInverse);
    shayDMaterial.uniforms.lightProjMatrix.value.copy(shadowCam.projectionMatrix);
    shayDMaterial.uniforms.shadowMap = shadowRenderTarget.depthTexture;
    shayDMaterial.uniforms.textureSize = 1024.0; //ended up being unecessary as I hardcoded the textureSize

    envmapMaterial.uniforms.shadowMap.value = shadowRenderTarget.depthTexture;
    envmapMaterial.uniforms.lightViewMatrix.value.copy(shadowCam.matrixWorldInverse);
    envmapMaterial.uniforms.lightProjMatrix.value.copy(shadowCam.projectionMatrix);

    // TODO: True second pass, change below
    renderer.setRenderTarget(null);
    renderer.clear();
    renderer.render(scene, camera);

//floor.vs already had everything needed passing into the fragment
floor.fs: //completed these two functions for the simple shadow 
vec3 getShadowMapCoords() { //this gets the coordinates to get the shadow check from
    vec3 projCoords = lightSpaceCoords.xyz / lightSpaceCoords.w;
    projCoords = projCoords * 0.5 + 0.5;
	projCoords.xy = clamp(projCoords.xy, 0.0, 1.0);
    return projCoords;
}


float inShadow(vec3 fragCoord) {
    float depthFromShadowMap = texture(shadowMap, fragCoord.xy).r;//This samples from the shadow map and checks if that spot should have a shadow
    float bias = 0.001; //to avoid aliasing, but not too large to cause noticable peter panning
    return fragCoord.z - bias > depthFromShadowMap ? 1.0 : 0.0; //returns if there is a shadow or not
}

//this is then used in the main in these lines
vec3 shadowCoords = getShadowMapCoords(); //get the coords to pass in
float shadow = 1.0 - inShadow(shadowCoords);//if 1, no shadow, if 0 yes shadow and makes it black
vec3 colorSample = texture(colorMap, texCoord).rgb * (light_DFF + light_SPC); //get the base color without ambient
vec3 TOTAL = light_AMB*colorSample + shadow * (colorSample); //add the ambient plus the diff and spec * shad
vec3 projCoords = getShadowMapCoords();// remenant of some debugging
gl_FragColor = vec4(TOTAL,1.0); //use that total

For the last part adding the smoothing there were just some further modifications to the fragment shader:
float calculateShadow() {//this method replaces the simple shadow check used in the 2nd part,
    vec3 fragCoord = getShadowMapCoords();
    float shadow = 0.0;//declaring shadow

    float bias = 0.0005;
    float texelSize = 1.0 / 1024.0; //geting texel size of the shadowmap, hardcoded as it wasn't working without that for me
    for(int x = -3; x <= 3; ++x) { //nested for loop searches through a 3x3 grid of texels around the main point
        for(int y = -3; y <= 3; ++y) {
            vec2 offset = vec2(float(x), float(y)) * texelSize;
            vec2 sampleUV = fragCoord.xy + offset; 
            
            // Sample depth from shadow map
            float closestDepth = texture(shadowMap, sampleUV).r;

            // Compare fragment depth with depth in shadow map
            if(fragCoord.z - bias > closestDepth)
                shadow += 1.0; //each texel contributes to the total 
        }
    }
    shadow /= 36.0; //divide by total number to get average of all texels in shadow

    // Return 1 = lit, 0 = in shadow
    return 1.0 - shadow; //finally return 1- that 
}

//Then in the main just replace the shadow calculation and leave everything else as was in part 2
float shadow = calculateShadow();