import { Container, Text, Sprite, Graphics } from "@pixi/react";
import { TextStyle } from "pixi.js";

interface PlayerInfoProps{
    width: number;
    height: number;
    score: number;
    colour: string;
    fontSize?: number | string;
    y?: number;
    x?: number
}

export default function PlayerInfo(props: PlayerInfoProps){

    const draw = ((g:any)=>{
        g.clear();
        g.beginFill('beige', 0.7);
        g.drawRoundedRect(0, 0, props.width * 3.6, props.height * 1.45, 10)
        g.endFill()
        g.beginFill(props.colour, 0.7);
        g.drawRoundedRect(props.width * 0.1, 0, props.width * 0.75, props.height * 0.95, 10);
        g.endFill();
    })
    
    return(
        <Container y={props.y} x={0}>
            <Graphics draw={draw}/>
            <Sprite image={'/assets/leaderboard-icons/player.png'} tint={0xFFAFFF} width={props.width} height={props.height}/>
            <Container>
                <Sprite image={'/assets/leaderboard-icons/victory-points.png'} width={props.width * 0.5} height={props.height * 0.5} x={props.width * 0.1} y={props.height * 0.95}/>
                <Text style={new TextStyle({fontSize: props.fontSize})} text={props.score.toString()} x={props.width * 0.55} y={props.height * 0.95} />           
            </Container>
            <Container x={props.width} y={props.height * 0.1}>
                <Sprite image={'/assets/leaderboard-icons/path.png'} width={props.width * 0.7} height={props.height * 0.7}/>
                <Text style={new TextStyle({fontSize: props.fontSize})} text={props.score.toString()} x={props.width * 0.8} y={props.height * 0.05} />           
            </Container>
            <Container x={props.width * 2.15} y={props.height * 0.1}>
                <Sprite image={'/assets/leaderboard-icons/shield.png'} width={props.width * 0.7} height={props.height * 0.7}/>
                <Text style={new TextStyle({fontSize: props.fontSize})} text={props.score.toString()} x={props.width * 0.8} y={props.height * 0.05} />           
            </Container>
            <Container x={props.width} y={props.height * 0.75}>
                <Sprite image={'/assets/action-board/dev.png'} width={props.width * 0.7} height={props.height * 0.6}/>
                <Text style={new TextStyle({fontSize: props.fontSize})} text={props.score.toString()} x={props.width * 0.8} y={props.height * 0.05} />           
            </Container>
            <Container x={props.width * 2.15} y={props.height * 0.75}>
                <Sprite image={'/assets/leaderboard-icons/shield.png'} width={props.width * 0.7} height={props.height * 0.7}/>
                <Text style={new TextStyle({fontSize: props.fontSize})} text={props.score.toString()} x={props.width * 0.8} y={props.height * 0.05} />           
            </Container>
        </Container>
    )
}