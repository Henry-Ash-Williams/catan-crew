import { useCallback, ComponentProps } from "react";
import { Graphics, Text } from "@pixi/react";
import { TextStyle, Geometry } from 'pixi.js';

// type Draw = ComponentProps<typeof Graphics>['draw'];

interface props {
    x: number,
    y: number,
    tileID: number,
    radius: number
}


function Tile(props: props) {


        const x = props.x;
        const y = props.y;
        const tileID = props.tileID;
        const HEXAGON_RADIUS = props.radius;
        const HEXAGON_POINTS = [
            0, -HEXAGON_RADIUS,
            HEXAGON_RADIUS * Math.sqrt(3) / 2, -HEXAGON_RADIUS / 2,
            HEXAGON_RADIUS * Math.sqrt(3) / 2, HEXAGON_RADIUS / 2,
            0, HEXAGON_RADIUS,
            -HEXAGON_RADIUS * Math.sqrt(3) / 2, HEXAGON_RADIUS / 2,
            -HEXAGON_RADIUS * Math.sqrt(3) / 2, -HEXAGON_RADIUS / 2,
            ];
            // const draw = useCallback<Draw>((g) => {
            // });

        return (
            <Graphics x={x} y={y} draw={((g) => {
                        g.beginFill(randomColour());
                        g.drawPolygon(HEXAGON_POINTS);
                        g.endFill();
            })}>
  
                 <Text
                    text={tileID.toString()}
                    anchor={0.5}
                    x={0}
                    y={0}
                    style={
                        new TextStyle({
                        align: 'center',
                        fontFamily: '"Source Sans Pro", Helvetica, sans-serif',
                        fontSize: 30,
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
                    })
              }
          />

          </Graphics>
      
        );
    }

    function randomColour() {
        return Math.floor(Math.random()*16777215)
    }
    
    export { Tile };