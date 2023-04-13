import { Container } from "@pixi/react";
import PlayerInfo from "./PlayerInfo";
import info from './players.json'

interface LeaderBoardProps{
    width: number;
    height: number;
    fontSize: number;
    players?: any;
}

export default function LeaderBoard(props : LeaderBoardProps){

    let yOffset = 1.01;

    return(
        <Container x={props.width * 0.86} y={0}>
            {info.players.map((p : any) =>{
                yOffset -= 0.12;
                return <PlayerInfo key={p.colour} colour={p.colour} fontSize={props.fontSize * 0.3} score={p.victory_points} height={props.height * 0.07} width={props.width * 0.04} y={props.height * yOffset}/>
            })}
        </Container>
    )
}