import { setup, loadAndPlaceGLB } from "./js/setup.js";
import * as THREE from "./js/three.module.js";
import { SourceLoader } from "./js/SourceLoader.js";
import { THREEx } from "./js/KeyboardState.js";

// Setup and return the scene and related objects.
// You should look into js/setup.js to see what exactly is done here.
const { renderer, scene, camera, worldFrame } = setup();

// Used THREE.Clock for animation
var clock = new THREE.Clock();

/////////////////////////////////
//   YOUR WORK STARTS BELOW    //
/////////////////////////////////

// Initialize uniforms
let tailBone;

// As in A1 we position the sphere in the world solely using this uniform
// So the initial y-offset being 1.0 here is intended.
const sphereOffset = { type: "v3", value: new THREE.Vector3(0.0, 1.0, 0.0) };

// Distance threshold beyond which the dog should shoot lasers at the sphere (needed for Q1c).
const LaserDistance = 15.0;

const waveDistance = 10.0;

// TODO: you may want to add more const's or var's to implement
const dogPosition = new THREE.Vector3(0, 0, -8);
const dogScale = new THREE.Vector3(5, 5, 5);
// the dog waving its tail

// Materials: specifying uniforms and shaders
const sphereMaterial = new THREE.ShaderMaterial({
  uniforms: {
    sphereOffset: sphereOffset,
  },
});

const eyeMaterial = new THREE.ShaderMaterial();

const laserMaterial = new THREE.ShaderMaterial(); //Don't need to pass anything in since it will already be from eye to sphere

// TODO: make necessary changes to implement the laser eyes

// Load shaders.
const shaderFiles = [
  "glsl/sphere.vs.glsl",
  "glsl/sphere.fs.glsl",
  "glsl/eye.vs.glsl",
  "glsl/eye.fs.glsl",
  "glsl/laser.vs.glsl",
  "glsl/laser.fs.glsl",
];

new SourceLoader().load(shaderFiles, function (shaders) {
  sphereMaterial.vertexShader = shaders["glsl/sphere.vs.glsl"];
  sphereMaterial.fragmentShader = shaders["glsl/sphere.fs.glsl"];

  eyeMaterial.vertexShader = shaders["glsl/eye.vs.glsl"];
  eyeMaterial.fragmentShader = shaders["glsl/eye.fs.glsl"];

  //Adding new laser material for laser eyes
  laserMaterial.vertexShader = shaders["glsl/laser.vs.glsl"];
  laserMaterial.fragmentShader = shaders["glsl/laser.fs.glsl"];
});

// Load and place the dog geometry
// Look at the definition of loadOBJ to familiarize yourself with how each parameter
// affects the loaded object.

// TODO: Load and place the dog geometry in GLB format, a simple example is provided
loadAndPlaceGLB("glb/dog.glb", scene, function (dog) {
  dog.traverse(function (child) {
    if (child instanceof THREE.SkinnedMesh) {
      var skeleton = new THREE.Skeleton(child.skeleton.bones);
      for (var i = 0; i < skeleton.bones.length; i++) {
        console.log(skeleton.bones[i].name);
        if (skeleton.bones[i].name == "Dog_Tail_01_02SHJnt_42") {
           tailBone = skeleton.bones[i];
        }
      }
    }
  });
  dog.scale.set(dogScale.x, dogScale.y, dogScale.z);
  dog.position.set(dogPosition.x, dogPosition.y, dogPosition.z);
});


// Create the main covid sphere geometry
// https://threejs.org/docs/#api/en/geometries/SphereGeometry
const sphereGeometry = new THREE.SphereGeometry(1.0, 32.0, 32.0);
const sphere = new THREE.Mesh(sphereGeometry, sphereMaterial);
scene.add(sphere);

const sphereLight = new THREE.PointLight(0xffffff, 50.0, 100);
scene.add(sphereLight);

// Example for an eye ball
// TODO: Create two eye ball meshes from the same geometry



const dogQuaternion = new THREE.Quaternion();
const dogMatrix = new THREE.Matrix4();
dogMatrix.compose(dogPosition,dogQuaternion, dogScale)

const eyeGeometry = new THREE.SphereGeometry(1.0, 32, 32);
const eyeScale = 0.5;

const leftEyeSocket = new THREE.Object3D();
const leftEyeSocketPos = new THREE.Vector4(-0.8, 9.2, 6, 1);
const leftWorldPos = new THREE.Vector3().setFromMatrixPosition(
    new THREE.Matrix4().makeTranslation(
        leftEyeSocketPos.x,
        leftEyeSocketPos.y,
        leftEyeSocketPos.z
    ).multiply(dogMatrix)
);
leftEyeSocket.position.copy(leftWorldPos);

const rightEyeSocket = new THREE.Object3D();
const rightEyeSocketPos = new THREE.Vector4(0.8, 9.2, 6, 1);
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
rightEye.scale.set(eyeScale, eyeScale, eyeScale);
rightEyeSocket.add(rightEye);
scene.add(leftEyeSocket);
scene.add(rightEyeSocket);


// Lasers
// https://threejs.org/docs/index.html#api/en/geometries/CylinderGeometry
// These could also be made with a two camera facing trinagles or quads instead of a full blown cylinder.
// The reason is that lasers have a simple geometry and don't have any fancy angle based shading (for now)


const laserGeometry = new THREE.CylinderGeometry(0.05, 0.05, 1.0, 8); //Trying with cylinder
const leftLaser = new THREE.Mesh(laserGeometry, laserMaterial);
const rightLaser = new THREE.Mesh(laserGeometry, laserMaterial);
scene.add(leftLaser);
scene.add(rightLaser);

// Listen to keyboard events.
const keyboard = new THREEx.KeyboardState();
function checkKeyboard() {
  if (keyboard.pressed("W")) sphereOffset.value.z -= 0.1;
  else if (keyboard.pressed("S")) sphereOffset.value.z += 0.1;

  if (keyboard.pressed("A")) sphereOffset.value.x -= 0.1;
  else if (keyboard.pressed("D")) sphereOffset.value.x += 0.1;

  if (keyboard.pressed("E")) sphereOffset.value.y -= 0.1;
  else if (keyboard.pressed("Q")) sphereOffset.value.y += 0.1;

  // The following tells three.js that some uniforms might have changed.
  sphereMaterial.needsUpdate = true;
  eyeMaterial.needsUpdate = true;

  // Move the sphere light in the scene. This allows the floor to reflect the light as it moves.
  sphereLight.position.set(
    sphereOffset.value.x,
    sphereOffset.value.y,
    sphereOffset.value.z
  );
}

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
  
}

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
}

function updateTail() {
    if (!tailBone) return; 
    const dx = sphereOffset.value.x - dogPosition.x;
    const dz = sphereOffset.value.z - dogPosition.z;
    const horizontalDist = Math.sqrt(dx * dx + dz * dz);
    const time = clock.getElapsedTime(); 
    const baseAmplitude = .5; 
    const baseSpeed = 3.0; 
    let wagAmplitude = baseAmplitude;
    let wagSpeed = baseSpeed;
    if (horizontalDist < waveDistance) {
        const factor = (waveDistance - horizontalDist) / waveDistance; // tends to 1 as it gets closer
        wagAmplitude += factor * 1;  // scale the variables based on that factor
        wagSpeed += factor * 10;      
    }
    tailBone.rotation.set(0, 0, 0);
    const centerY = .5 //offset so it's actually centered
    tailBone.rotation.y = centerY + wagAmplitude * Math.sin(wagSpeed * time);
    
}

// Setup update callback
function update() {
  // TODO: make neccesary changes to implement gazing, the dog waving its tail, etc.
  checkKeyboard();
  
  const target = updateLook();
  updateLaser(target);
  updateTail(); 
  // Requests the next update call, this creates a loop
  requestAnimationFrame(update);
  renderer.render(scene, camera);
}

// Start the animation loop.
update();
