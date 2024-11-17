import { Html, useAnimations, useGLTF } from "@react-three/drei";
import { useFrame } from "@react-three/fiber";
import { useEffect, useRef, useState } from "react";
import { MathUtils, MeshStandardMaterial } from "three";
import { randInt } from "three/src/math/MathUtils";

const ANIMATION_FADE_TIME = 0.5;

export function TalkingAvatar({ answer, isSpeaking, ...props }) {
  const group = useRef();
  const { scene } = useGLTF(`/models/Teacher_Ananya.glb`);
  useEffect(() => {
    scene.traverse((child) => {
      if (child.material) {
        child.material = new MeshStandardMaterial({
          map: child.material.map,
        });
      }
    });
  }, [scene]);

  const { animations } = useGLTF(`/models/animations_Ananya.glb`);
  const { actions, mixer } = useAnimations(animations, group);
  const [animation, setAnimation] = useState("Idle");
  const [blink, setBlink] = useState(false);

  useEffect(() => {
    let blinkTimeout;
    const nextBlink = () => {
      blinkTimeout = setTimeout(() => {
        setBlink(true);
        setTimeout(() => {
          setBlink(false);
          nextBlink();
        }, 100);
      }, randInt(1000, 5000));
    };
    nextBlink();
    return () => clearTimeout(blinkTimeout);
  }, []);

  useEffect(() => {
    if (isSpeaking) {
      setAnimation("Talking");
    } else {
      setAnimation("Idle");
    }
  }, [isSpeaking]);

  const visemeSequence = [1, 3, 21];
  var randomVisemeIndex;
  var visemeId;

  useFrame(({ camera }) => {
    // Smile
    lerpMorphTarget("mouthSmile", 0.2, 0.5);
    // Blinking
    lerpMorphTarget("eye_close", blink ? 1 : 0, 0.5);

    // Talking
    for (let i = 0; i <= 21; i++) {
      lerpMorphTarget(i, 0, 0.1); // reset morph targets
    }

    if (isSpeaking && answer && answer.visemes && answer.audioPlayer) {
      for (let i = answer.visemes.length - 1; i >= 0; i--) {
        const viseme = answer.visemes[i];
        if (answer.audioPlayer.currentTime * 1000 >= viseme[0]) {
          randomVisemeIndex = Math.floor(Math.random() * 3);
          visemeId = visemeSequence[randomVisemeIndex];
          lerpMorphTarget(visemeId, 1, 0.2);
          break;
        }
      }
    }
  });

  useEffect(() => {
    actions[animation]
      ?.reset()
      .fadeIn(mixer.time > 0 ? ANIMATION_FADE_TIME : 0)
      .play();
    return () => {
      actions[animation]?.fadeOut(ANIMATION_FADE_TIME);
    };
  }, [animation, actions]);

  const lerpMorphTarget = (target, value, speed = 0.1) => {
    scene.traverse((child) => {
      if (child.isSkinnedMesh && child.morphTargetDictionary) {
        const index = child.morphTargetDictionary[target];
        if (
          index === undefined ||
          child.morphTargetInfluences[index] === undefined
        ) {
          return;
        }
        child.morphTargetInfluences[index] = MathUtils.lerp(
          child.morphTargetInfluences[index],
          value,
          speed
        );
      }
    });
  };

  return (
    <group {...props} dispose={null} ref={group}>
      <primitive object={scene} />
    </group>
  );
}

useGLTF.preload(`/models/Teacher_Ananya.glb`);
useGLTF.preload(`/models/animations_Ananya.glb`);
