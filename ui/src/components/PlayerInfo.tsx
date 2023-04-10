import { Container, Text, Sprite, Graphics } from "@pixi/react";
import { TextStyle } from "pixi.js";

interface PlayerInfoProps{
    width: number;
    height: number;
    score: number;
    fontSize?: number | string;
    y?: number;
    x?: number
}

export default function PlayerInfo(props: PlayerInfoProps){

    return(
        <Container y={props.y} x={props.x}>
            <Sprite image={'/assets/leaderboard-icons/player.png'} width={props.width} height={props.height}/>
            <Container>
                <Sprite image={'/assets/leaderboard-icons/victory-points.png'} width={props.width * 0.5} height={props.height * 0.5} x={props.width * 0.1} y={props.height * 0.95}/>
            </Container>
            <Container width={props.width} x={props.width} y={props.height * 0.25}>
                <Sprite image={'/assets/leaderboard-icons/path.png'} width={props.width * 0.7} height={props.height * 0.7}/>
            </Container>
            <Container>
                <Sprite image={'/assets/leaderboard-icons/shield.png'} width={props.width * 0.7} height={props.height * 0.7} x={props.width * 1.8} y={props.height * 0.25}/>
                <Text style={new TextStyle({fontSize: props.fontSize})} text={props.score.toString()} x={props.width * 0.55} y={props.height} />           
            </Container>
        </Container>
    )
}