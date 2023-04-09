import { Container, Sprite, Text } from "@pixi/react";
import PlayerInfo from "./PlayerInfo";

interface LeaderBoardProps{
    width: number;
    height: number
}

export default function LeaderBoard(props : LeaderBoardProps){

    return(
        <Container x={props.width * 0.75} y={props.height * 0.37}>
            <PlayerInfo fontSize={'1.8rem'} score={1} height={props.height * 0.07} width={props.width * 0.04} y={props.height * 0}/>
            <PlayerInfo fontSize={'1.8rem'} score={1} height={props.height * 0.07} width={props.width * 0.04} y={props.height * 0.1}/>
            <PlayerInfo fontSize={'1.8rem'} score={1} height={props.height * 0.07} width={props.width * 0.04} y={props.height * 0.2}/>
            <PlayerInfo fontSize={'1.8rem'} score={1} height={props.height * 0.07} width={props.width * 0.04} y={props.height * 0.3}/>
        </Container>
    )
}