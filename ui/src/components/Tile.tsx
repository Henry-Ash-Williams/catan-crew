import { Sprite, Text, Container } from "@pixi/react";
import { type } from "os";
import { TextStyle, Texture } from 'pixi.js';

interface Tile {
    type: string,
    location: number,
    harbor?: boolean, //not implemented
    resource?: string | null,
    number_token?: number | null
}

interface TileComponentProps {
    x: number,
    y: number,
    width: number,
    height: number,
    t: Tile,

}

function TileComponent(props: TileComponentProps) {
    const tileSvg = "/assets/board/" + props.t.resource + ".svg";
    const svg = Texture.from(tileSvg);

    // const x = props.x;
    // const y = props.y;
    // const tileID = props.tileID;
    // const HEXAGON_RADIUS = props.radius;
    // const HEXAGON_POINTS = [
    //     0, -HEXAGON_RADIUS,
    //     HEXAGON_RADIUS * Math.sqrt(3) / 2, -HEXAGON_RADIUS / 2,
    //     HEXAGON_RADIUS * Math.sqrt(3) / 2, HEXAGON_RADIUS / 2,
    //     0, HEXAGON_RADIUS,
    //     -HEXAGON_RADIUS * Math.sqrt(3) / 2, HEXAGON_RADIUS / 2,
    //     -HEXAGON_RADIUS * Math.sqrt(3) / 2, -HEXAGON_RADIUS / 2,
    //     ];
        // const draw = useCallback<Draw>((g) => {
        // });

    return (
        <Container x={props.x} y={props.y} width={props.width} height={props.height}>
            <Sprite x={props.width/2} y={props.height/2} width={50} height={50} anchor={0.5} texture={svg}/>
            {props.t.number_token ? <Text
                text={props.t.number_token.toString()}
                anchor={0.5}
                x={props.width/2}
                y={props.height/2}
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
                })}
            /> : null}
            
        </Container>
    
    );
}

export { TileComponent };