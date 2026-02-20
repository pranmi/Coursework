in vec3 modelPos;

void main() {
	// TODO: Add some conditions to color the pupil
	// The eye is facing +z so that when it is initially positioned on the fox,
	// it should be facing backward.
	// The following color is Eye whites (the fox is tired, so the eye whites are pinkish).
	vec3 scleraColor = vec3(1.0, 1.0, 1.0);
	vec3 irisColor = vec3(0.1, 0.4, 0.8);
	vec3 pupilColor = vec3(0.0, 0.0, 0.0);
	vec3 color = scleraColor;
	if(modelPos.z > 0.0){
		vec2 uv = modelPos.xy;
		float r = length(uv); // distance from center
		
		
		if(r < 0.5){          // iris radius
			color = irisColor;
		}
		if(r < 0.2){          // pupil radius
			color = pupilColor;
		}
	}
	gl_FragColor = vec4(color, 1.0);
	
}
