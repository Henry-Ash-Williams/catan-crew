import { Container, Graphics, Sprite, Text } from "@pixi/react"
import { useCallback } from "react";
import {TextStyle} from 'pixi.js';

interface CardProps {
    amount: number;
    resourceType: string;
    width : number;
    height: number;
    y: number;
    x?: number;
    fontSize: number;
}

export default function Card(props: CardProps){
    const resourceDict : {[resource: string]: string[]} = {
    'brick': ['../assets/board/archive/brick.svg', '#f55442'],
    'wool': ["../assets/board/archive/wool.svg", '#dec6c3'],
    'ore': ["../assets/board/archive/ore.svg", '#6dc0e3'],
    'lumber': ["../assets/board/archive/lumber.svg", '#93f542'],
    'grain': ["../assets/board/archive/grain.svg", 'orange'],
    'plenty': ["../assets/action-board-dev/plenty.png", 'green'],
    'hidden': ["../assets/action-board-dev/hidden.png", 'lightblue'],
    'monopoly': ["../assets/action-board-dev/monopoly.png", 'purple'],
    'road': ["../assets/action-board-dev/road.png", 'grey']
    }

    return(
        <Container x={(props.x? props.x : 2)} y={props.y}>
            <Sprite image={'/assets/menu/panel_beige.png'} width={props.width * 1/15} height={props.height * 0.15} tint={resourceDict[props.resourceType][1]}/>
            <Sprite image={resourceDict[props.resourceType][0]} width={props.width * 0.05} height={props.height * 0.08} x={props.width * 0.007} y={props.height * 0.045}/>
            <Text text={props.amount.toString()} x={5} y={5} style={new TextStyle({fontSize: props.fontSize * 0.3})}/>
        </Container>
    )
}