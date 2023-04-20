import { Container } from "@pixi/react";
import PlayerInfo from "./PlayerInfo";

interface LeaderBoardProps{
    state: any;
    width: number;
    height: number;
    fontSize: number;
}

export default function LeaderBoard(props : LeaderBoardProps){

    let yOffset = 1.01;

    return(
        <Container x={props.width * 0.86} y={0}>
            {props.state.map((p : any) =>{
                yOffset -= 0.12;
                return <PlayerInfo key={p.player} colour={p.player} devCards={p.total_dev_card} resources={p.total_resources} army={p.knights_played} road={p.road_len} fontSize={props.fontSize * 0.3} score={p.visible_vp} height={props.height * 0.07} width={props.width * 0.04} y={props.height * yOffset}/>
            })}
        </Container>
    )
}