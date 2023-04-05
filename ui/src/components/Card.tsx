import { Container, Graphics, Sprite } from "@pixi/react"
import { useCallback } from "react"

interface CardProps {
    resourceType: string
}

export default function Card(props: CardProps){
    const resourceDict : {[resource: string]: string[]} = {
    'brick': ['../assets/board/archive/brick.svg', '#f55442'],
    'wool': ["../assets/board/archive/wool.svg", '#dec6c3'],
    'ore': ["../assets/board/archive/ore.svg", '#6dc0e3'],
    'lumber': ["../assets/board/archive/lumber.svg", '#93f542'],
    'grain': ["../assets/board/archive/grain.svg", '#f5d742']
    }

    const draw = useCallback((g : any) => {
        g.clear();
        g.beginFill(resourceDict[props.resourceType][1], 1);
        g.drawRect(0, 0, 120, 120);
        g.endFill();
    }, []);

    return(
        <Container>
            <Graphics draw={draw}/>
            <Sprite image={resourceDict[props.resourceType][0]} width={50} height={50} x={25} y={40}/>
        </Container>
    )
}