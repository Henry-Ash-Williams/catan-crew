import React, { useState, useEffect } from "react";
import { Container, Sprite, Text } from "@pixi/react";
import { TextStyle } from "pixi.js";


interface DiceComponentProps {
  canRoll: boolean;
  numbersToDisplay: [number, number];
  setNumbersToDisplay: (numbers: [number, number]) => void;
  onClick: () => void;
  x: number;
  y: number;
  fontSize: number;
}

function DiceComponent(props: DiceComponentProps) {
  const [diceOpacity, setDiceOpacity] = useState(0.5);

//   sound.add('dice', '/assets/dice/dieShuffle1.ogg')

  useEffect(() => {
    if (props.canRoll) {
      setDiceOpacity(1);
    } else {
      setDiceOpacity(0.5);
    }
  }, [props.canRoll]);

  const handleClick = () => {
    if (props.canRoll) {
    //   sound.play('dice')
      // const randomNumber1 = Math.floor(Math.random() * 6) + 1;
      // const randomNumber2 = Math.floor(Math.random() * 6) + 1;
      // props.setNumbersToDisplay([randomNumber1, randomNumber2]);
      props.onClick();
    }
  };

  return (
    <Container x={props.x * 1.004} y={props.y}>
      <Sprite
        width={props.x * 0.06}
        height={props.y * 0.09}
        x={props.x * 0.01}
        y={0}
        image={`/assets/dice/dieWhite${props.numbersToDisplay[0]}.png`}  
      />
      <Sprite
        width={props.x * 0.06}
        height={props.y * 0.09}
        x={props.x * 0.09}
        y={0}
        image={`/assets/dice/dieWhite${props.numbersToDisplay[1]}.png`}
      />
      <Sprite
        width={props.x * 0.16}
        height={props.y * 0.055}
        x={0}
        y={props.y * 0.1}
        image={'/assets/menu/buttonLong_beige.png'}
        alpha={diceOpacity}
        eventMode={props.canRoll ? 'static' : 'none'}
        onclick={handleClick}
      />
      <Text
        text={"Roll dice"}
        alpha={diceOpacity}
        anchor={0.5}
        x={props.x * 0.08}
        y={props.y * 0.127}
        style={
            new TextStyle({
            align: 'center',
            fontFamily: '"Source Sans Pro", Helvetica, sans-serif',
            fontSize: props.fontSize * 0.25,
            fontWeight: '200',
            fill: '#ffffff', // gradient
            stroke: '#01d27e',
            strokeThickness: 5,
            letterSpacing: 5,
            dropShadow: true,
            dropShadowColor: '#ccced2',
            dropShadowBlur: 4,
            dropShadowAngle: Math.PI / 6,
            dropShadowDistance: 6,
            wordWrap: true,
            wordWrapWidth: 440,
        })}
            />
    </Container>
  );
}

export { DiceComponent };
