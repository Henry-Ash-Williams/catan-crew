import {Container, Sprite, Graphics} from '@pixi/react';
import { useState } from 'react';

interface TradeParticipantsProps{
    height: number,
    width: number,
    available : any,
    offered: string[];
    updateMethod: Function;
}

export default function TradeParticipants(props: TradeParticipantsProps){
    let xOffset = -props.width * 0.08;
    const [alphaVal, setAlphaVal] = useState({
        'red' : 0.5,
        'blue' : 0.5,
        'green' : 0.5,
        'orange' : 0.5
    });

    function handleClick(player: keyof object){
        let tempArray = [...props.offered];
        setAlphaVal({...alphaVal, [player] : (alphaVal[player] === 1 ? 0.5 : 1)});
        tempArray.includes(player) ? tempArray = tempArray.filter(word => word != player) : tempArray.push(player);
        props.updateMethod(tempArray)
    }

    return(
        <Container y={props.height * 0.45}>
            {props.available.map((p:keyof object) => {
                const draw = ((g:any)=>{
                    g.clear();
                    g.beginFill(p, 1);
                    g.drawRect(props.width * 0.019, props.height * 0.09, props.width * 0.04, props.height * 0.04);
                    g.endFill();
                })
                xOffset += props.width * 0.07;
                return (
                    <Container x={xOffset} alpha={alphaVal[p]} eventMode='static' onclick={()=>{handleClick(p)}}>
                        <Graphics draw={draw} alpha={alphaVal[p]}/>
                        <Sprite image={'/assets/leaderboard-icons/player.png'} width={props.width * 0.08} height={props.height * 0.15}/>
                    </Container>
                )
            })}
            <Sprite image={'/assets/leaderboard-icons/bank.png'} height={props.height * 0.13} width={props.width * 0.07} x={props.width * 0.21} y={0}/>
        </Container>
    )
}