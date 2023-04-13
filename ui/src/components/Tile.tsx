import { Sprite, Text, Container } from "@pixi/react";
import { type } from "os";
import { TextStyle, Texture } from 'pixi.js';
import { IntersectionComponent } from './Intersection';


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
    // let tile: React.ReactElement
    // if(props.t.type == "SeaTile"){
    //     tileBackground = "/assets/board/resource/sea/water_N.png";
    // } else if (props.t.type == "DesertTile") {
    //     tileBackground = "/assets/board/resource/desert/sand_rocks_N.png";
    // } else if (props.t.type == "PathTile") {
    //     tileBackground = "/assets/board/path/tile/grass_N.png";
    //     if(props.t.direction == 1){
    //         tileImg = "/assets/board/path/path_straight_N.png"
    //     } else if(props.t.direction == 2){
    //         tileImg = "/assets/board/path/path_straight_NW.png"
    //     }else if(props.t.direction == 3){
    //         tileImg = "/assets/board/path/path_straight_NE.png"
    //     }
    // } else if ( props.t.type == "ResourceTile" || props.t.type == "null") {
    //     tileBackground = "/assets/board/resource/desert/sand_rocks_N.png";
    // } else if(props.t.type == "Intersection"){
    //     tile = <IntersectionComponent x={props.x} y={props.y}/>
    // }



    // console.log(tileBackground)
   
    return (
        <Container x={props.x} y={props.y} width={props.width} height={props.height}>
            {/* <Sprite x={0} y={0} width={props.width*5} height={props.height*5} anchor={0.5} image={tileBackground}/>
            {props.t.number_token ? <Text
                text={props.t.number_token.toString()}
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
                })}
            /> : null}
            {
                props.t.type == "Intersection" ? <Sprite x={0} y={-15} width={props.width*5} height={props.height*5} anchor={0.5} image={tileImg} tint={0xffffff}/> : null
            }
            
            {
                props.t.type == "PathTile" 
                    ? <Sprite x={0} y={-15} width={props.width*5} height={props.height*5} anchor={0.5} image={tileImg} /> : null
            }
             */}
            
        </Container>
    
    );
}

export { TileComponent };