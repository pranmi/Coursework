# Assignment 3
# Pranith Mullapudi PXM220087


## Part A
Basically just copy pasted the given documentation code for the gltf loader

### Changed Code:
#### setup.js
**const loader = new GLTFLoader();
    loader.load(
        'glb/dog.glb',
        function(gltf){
            const model = gltf.scene;
            scene.add(gltf.scene)

            if(place){
                place(model);
            }

            gltf.animations;
            gltf.scene;
            gltf.scenes;
            gltf.cameras;
            gltf.asset;
        },
        function(xhr) {
            console.log((xhr.loaded/xhr.total*100) + '% loaded');
        },
        
    )**
#### A3.js
loadAndPlaceGLB("glb/dog.glb", **scene**, function (dog)) #added the scene parameter

## Part B
For this section there are two main things, having the spheres in the right position, and rendering them with the pupil and iris,
For the first part I manually calculated the model matrix for dog since we know the inputs and used that to essentially make the eye's children of the dog.
This way they are always in the right spot regardless of where the dog is.
For the second part I use the passed in modelPos to render the iris and pupil depending on how far the point is from the center in the xy plane, then make sure only the front is done by checking that z > 0
as without that check the pupil and eye get rendered on both the +z and -z ends of the eye
See A3.pdf for the assignment specifications.

### Changed Code:
#### A3.js (This is all for the first part I talked about in the description)
const dogPosition = new THREE.Vector3(0, 0, -8);
const dogScale = new THREE.Vector3(5, 5, 5); //Added these at the beginning so they can be changed in one spot but make sure the changes apply to the dog itself and the eyes at the same time



const dogQuaternion = new THREE.Quaternion();
const dogMatrix = new THREE.Matrix4();
dogMatrix.compose(dogPosition,dogQuaternion, dogScale)  //Manually create the ModelMatrix for dog since we know all the component transformations

const eyeGeometry = new THREE.SphereGeometry(1.0, 32, 32);
const eyeScale = 0.5; //pre-existings

const leftEyeSocket = new THREE.Object3D();
const leftEyeSocketPos = new THREE.Vector4(-0.8, 9.2, 6, 1); //For each socket, set it's position relative to the dog, then calculate the final world position by applying the dog model matrix
const leftWorldPos = new THREE.Vector3().setFromMatrixPosition(
    new THREE.Matrix4().makeTranslation(
        leftEyeSocketPos.x,
        leftEyeSocketPos.y,
        leftEyeSocketPos.z
    ).multiply(dogMatrix)
);
leftEyeSocket.position.copy(leftWorldPos); //copy that calculated position into the actual position value

const rightEyeSocket = new THREE.Object3D();
const rightEyeSocketPos = new THREE.Vector4(0.8, 9.2, 6, 1); //Repeat the exact same process for the right eye
const rightWorldPos = new THREE.Vector3().setFromMatrixPosition(
    new THREE.Matrix4().makeTranslation(
        rightEyeSocketPos.x,
        rightEyeSocketPos.y,
        rightEyeSocketPos.z
    ).multiply(dogMatrix)
);
rightEyeSocket.position.copy(rightWorldPos);
const leftEye = new THREE.Mesh(eyeGeometry, eyeMaterial);
const rightEye = new THREE.Mesh(eyeGeometry, eyeMaterial);
leftEye.scale.set(eyeScale, eyeScale, eyeScale);
leftEyeSocket.add(leftEye);
rightEye.scale.set(eyeScale, eyeScale, eyeScale); //Finally, perform the final scaling and adding to scene
rightEyeSocket.add(rightEye);
scene.add(leftEyeSocket);
scene.add(rightEyeSocket);

#### eye.fs.glsl (For the second part of the pupil and iris)

vec3 scleraColor = vec3(1.0, 1.0, 1.0); //the default color already there
	vec3 irisColor = vec3(0.1, 0.4, 0.8);
	vec3 pupilColor = vec3(0.0, 0.0, 0.0); //some preset colors for the eye, blue and black
	vec3 color = scleraColor; //Start by setting the fragment to the default sclera first
	if(modelPos.z > 0.0){ //Then check if its on the right side of the eye (+z)
		vec2 uv = modelPos.xy; //If so, get it's position on the xy plane of the eye
		float r = length(uv); // distance from center on the xy plane
		
		
		if(r < 0.5){          // if within this radius, set to iris color
			color = irisColor;
		}
		if(r < 0.2){          // if within this smaller radius, set to pupil color
			color = pupilColor;
		}
	}
	gl_FragColor = vec4(color, 1.0); //Apply the final color landed upon after the earlier conditions

## Part C
For this, I already did the pupil and iris in the earlier part, so only part that needed to be done was the orientation itself. Simply just call the lookAt method during each update to make them track the sphere

### Changed Code
#### A3.js
leftEyeSocket.lookAt(sphereOffset.value); //Added these two lines so each frame the eyes update to track whereever the sphere is (sphereOffset)
rightEyeSocket.lookAt(sphereOffset.value);


## Part D
3 parts for this one,
1. Add the lasershader material and create the lasers themselves
2. make it so they are only visible when the sphere is close enough
3. orient them so they are from the eyes to the sphere

### Changed Code
#### A3.js 
const LaserDistance = 15.0; //just made this a bit bigger so that it was easier to test partway through

const laserMaterial = new THREE.ShaderMaterial(); //creating the laser shader material

"glsl/laser.vs.glsl",
"glsl/laser.fs.glsl",// added the files to shaderFiles


laserMaterial.vertexShader = shaders["glsl/laser.vs.glsl"]; //Added the material to be loaded
aserMaterial.fragmentShader = shaders["glsl/laser.fs.glsl"];

const laserGeometry = new THREE.CylinderGeometry(0.05, 0.05, 1.0, 8); //creating the actual laser objects, one for each eye
const leftLaser = new THREE.Mesh(laserGeometry, laserMaterial);
const rightLaser = new THREE.Mesh(laserGeometry, laserMaterial);
scene.add(leftLaser);
scene.add(rightLaser);

function updateLaser(){ //Full function to update laser's, called during update
  const spherePos = sphereOffset.value.clone();
  const dogMiddleLocal = new THREE.Vector4(0, 1.2, 0, 1); //defining a local point in the dog coordinate as the center, then transforming to world to use for distance
  const dogWorldMiddle = dogMiddleLocal.clone().applyMatrix4(dogMatrix);
  const dogWorldMiddle3 = new THREE.Vector3(dogWorldMiddle.x, dogWorldMiddle.y, dogWorldMiddle.z); //transform the local center to world, then transform it to a vector3
  const dist = dogWorldMiddle3.distanceTo(spherePos); //Use that new vector three for the center to get the distance
  if(dist > LaserDistance){ //first check if the distance is too big, if so don't render them
    leftLaser.visible = false;
    rightLaser.visible = false;
  }
  else{ //If within the distance:
    leftLaser.visible = true; //make the lasers visible
    rightLaser.visible = true;
    const leftStart = leftEyeSocket.position.clone(); //get the start of the laser
    const leftDir = new THREE.Vector3().subVectors(spherePos, leftStart); //use the start and the sphere to get the vector of it's direction
    const leftLen = leftDir.length(); //use direction to get length for the cylinder
    const leftMid = new THREE.Vector3().addVectors(leftStart, spherePos).multiplyScalar(0.5); // get the midpoint where it needs to be centered

    leftLaser.position.copy(leftMid); //place it at the midpoint
    leftLaser.scale.set(1, leftLen, 1); //make it as long as the direction
    leftLaser.lookAt(spherePos); //orient it at the sphere
    leftLaser.rotateX(Math.PI / 2); //Had to rotate this way since lookAt orients it such that it's perpendicular

    const rightStart = rightEyeSocket.position.clone(); //repeat exact same steps for the right eye
    const rightDir = new THREE.Vector3().subVectors(spherePos, rightStart); 
    const rightLen = rightDir.length(); 
    const rightMid = new THREE.Vector3().addVectors(rightStart, spherePos).multiplyScalar(0.5); 

    rightLaser.position.copy(rightMid);
    rightLaser.scale.set(1, rightLen, 1); 
    rightLaser.lookAt(spherePos); 
    rightLaser.rotateX(Math.PI / 2);
  }
  
}


## Part E
need to get the tailbone, add some extra condition logic so the eyes look at camera if too close
make an update function for the tail so it wags (based on a sin function with the clock), and have the wag adjust based on how close the sphere is

let tailBone; //added so the variable exists since it's async

//within the GLB load
tailBone = skeleton.bones[i]; //actually get the base tailbone

function updateLaser(targetPos){
  const dogMiddleLocal = new THREE.Vector4(0, 1.2, 0, 1); //defining a local point in the dog coordinate as the center, then transforming to world to use for distance
  const dogWorldMiddle = dogMiddleLocal.clone().applyMatrix4(dogMatrix);
  const dogWorldMiddle3 = new THREE.Vector3(dogWorldMiddle.x, dogWorldMiddle.y, dogWorldMiddle.z);
  const dist = dogWorldMiddle3.distanceTo(sphereOffset.value);
  if(dist > LaserDistance){
    leftLaser.visible = false;
    rightLaser.visible = false;
  }
  else{
    leftLaser.visible = true;
    rightLaser.visible = true;
    const leftStart = leftEyeSocket.position.clone(); // eye world position
    const leftDir = new THREE.Vector3().subVectors(targetPos, leftStart); // vector from eye → sphere
    const leftLen = leftDir.length(); // laser length
    const leftMid = new THREE.Vector3().addVectors(leftStart, targetPos).multiplyScalar(0.5); // midpoint

    leftLaser.position.copy(leftMid);
    leftLaser.scale.set(1, leftLen, 1); // stretch laser
    leftLaser.lookAt(targetPos); // orient laser toward sphere
    leftLaser.rotateX(Math.PI / 2);

    const rightStart = rightEyeSocket.position.clone(); // eye world position
    const rightDir = new THREE.Vector3().subVectors(targetPos, rightStart); // vector from eye → sphere
    const rightLen = rightDir.length(); // laser length
    const rightMid = new THREE.Vector3().addVectors(rightStart, targetPos).multiplyScalar(0.5); // midpoint

    rightLaser.position.copy(rightMid);
    rightLaser.scale.set(1, rightLen, 1); // stretch laser
    rightLaser.lookAt(targetPos); // orient laser toward sphere
    rightLaser.rotateX(Math.PI / 2);

  }
  
} //Very similar to the logic from part D, I added an input so instead of defaulting to the sphere it looks at the input instead

function updateLook() {
    const dx = sphereOffset.value.x - dogPosition.x;
    const dz = sphereOffset.value.z - dogPosition.z;
    const dist = Math.sqrt(dx * dx + dz * dz);

    if(dist > waveDistance){
        leftEyeSocket.lookAt(sphereOffset.value);
        rightEyeSocket.lookAt(sphereOffset.value);
        return sphereOffset.value.clone(); 
    } else {
        leftEyeSocket.lookAt(camera.position);
        rightEyeSocket.lookAt(camera.position);
        return camera.position.clone(); 
    }
}// correspondingly updated the look update so it returns the target being looked at, and making it look at the camera if within the wave distance

function updateTail() {
    if (!tailBone) return; //make sure we have the tailbone, had some problems with async in the beginning
    const dx = sphereOffset.value.x - dogPosition.x;
    const dz = sphereOffset.value.z - dogPosition.z;
    const horizontalDist = Math.sqrt(dx * dx + dz * dz); //get the horizontal distance for the tailwagging
    const time = clock.getElapsedTime(); //get the time for the sin function
    const baseAmplitude = .5; //some base values when not too close
    const baseSpeed = 3.0; 
    let wagAmplitude = baseAmplitude; // have variable set to them
    let wagSpeed = baseSpeed;
    if (horizontalDist < waveDistance) { //if the sphere is within the wavedistance
        const factor = (waveDistance - horizontalDist) / waveDistance; // tends to 1 as it gets closer 
        wagAmplitude += factor * 1;  // scale the variables based on that factor
        wagSpeed += factor * 10;      
    }
    tailBone.rotation.set(0, 0, 0); 
    const centerY = .5 //offset so it's actually centered
    tailBone.rotation.y = centerY + wagAmplitude * Math.sin(wagSpeed * time); //actual wag rotation
    
}

const target = updateLook(); //another slight change within the update function so that the target is passed from look to laser and the updatetail is called
updateLaser(target);
updateTail();