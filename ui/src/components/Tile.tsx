import { Sprite, Text, Container } from "@pixi/react";
import { type } from "os";
import { TextStyle, Texture } from 'pixi.js';

interface Tile {
    type: string
    location: number
    harbor?: boolean //not implemented
    resource?: string | undefined
    number_token?: number | undefined 
    owner?: number | null
    isCity?: boolean | undefined
    direction?: number | undefined
}

interface TileComponentProps {
    x: number,
    y: number,
    width: number,
    height: number,
    t: Tile,

}

function TileComponent(props: TileComponentProps) {

    let tileBackground = "";
    // let tileImg = "";
    if(props.t.type == "SeaTile"){
        tileBackground = "/assets/board/water_N.png";
    } else if (props.t.type == "DesertTile") {
        tileBackground = "/assets/board/sand_rocks_N.png";
    } else if (props.t.type == "Intersection" || props.t.type == "PathTile") {
        tileBackground = "/assets/board/grass_N.png";
    } else if ( props.t.type == "ResourceTile" || props.t.type == "null") {
        tileBackground = "/assets/board/grass_forest_N.png";
    }

    console.log(tileBackground)
    // if(props.t.resource){
    //     tileImg = "/assets/board/" + props.t.resource + ".png";
    // }   else {
    //     tileImg = "/assets/board/" + props.t.type + ".png";
    // }
   
    return (
        <Container x={props.x} y={props.y} width={props.width} height={props.height}>
            {/* <Sprite x={props.width/2} y={props.height/2} width={props.width*1.8} height={props.height*2} anchor={0.5} image={tileImg}/> */}
            <Sprite x={0} y={0} width={props.width*5} height={props.height*5} anchor={0.5} image={tileBackground}/>
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