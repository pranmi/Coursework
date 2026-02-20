in vec3 vcsNormal;
in vec3 vcsPosition;

uniform vec3 lightDirection;
uniform vec3 cameraPos;

uniform samplerCube skybox;

uniform mat4 matrixWorld;

void main( void ) {

  // Q1c : Calculate the vector that can be used to sample from the cubemap
  // TODO:
    vec3 N = normalize(vcsNormal);
    vec3 V = normalize(cameraPos - vcsPosition); // view vector
    vec3 R = reflect(-V, N);

    R.x = -R.x; 

    vec3 sampleColor = texture(skybox, R).rgb;

  gl_FragColor = vec4(sampleColor, 1.0);
}