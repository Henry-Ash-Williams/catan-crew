import { Container, Graphics } from "@pixi/react";
import { useCallback } from "react";

interface ActionBarProps{
    width: number;
    height: number
}

export default function ActionsBar(props: ActionBarProps){

    const draw = (g:any) => {
        g.clear();
        g.beginFill(0x0000ff, 0.2);
        g.drawRoundedRect(3, 0, props.width * 0.85, props.height * 1/8)
        g.endFill();
    }

    return(
        <Container y={props.height * 0.875}>
            <Graphics draw={draw}/>
            
        </Container>
    )
}