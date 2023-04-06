import { Container, Graphics, Sprite, Text } from "@pixi/react"
import { useCallback } from "react"

interface CardProps {
    amount: number;
    resourceType: string;
    xPos : number;
    yPos: number;
}

export default function Card(props: CardProps){
    const resourceDict : {[resource: string]: string[]} = {
    'brick': ['../assets/board/archive/brick.svg', '#f55442'],
    'wool': ["../assets/board/archive/wool.svg", '#dec6c3'],
    'ore': ["../assets/board/archive/ore.svg", '#6dc0e3'],
    'lumber': ["../assets/board/archive/lumber.svg", '#93f542'],
    'grain': ["../assets/board/archive/grain.svg", '#f5d742']
    }

    // const draw = useCallback((g : any) => {
    //     g.clear();
    //     g.beginFill(resourceDict[props.resourceType][1], 1);
    //     g.drawRoundedRect(0, 0, 100, 120);
    //     g.endFill();
    // }, []);

    return(
        <Container x={props.xPos} y={props.yPos}>
            <Sprite image={'/assets/menu/panel_beige.png'} width={100} height={120} tint={resourceDict[props.resourceType][1]}/>
            <Sprite image={resourceDict[props.resourceType][0]} width={55} height={50} x={20} y={40}/>
            <Text text={props.amount.toString()} x={5} y={5}/>
        </Container>
    )
}