import {Container, Graphics, Sprite} from '@pixi/react'

interface TradeProps{
    height: number;
    width: number;
    visible: boolean;
}

export default function Trade(props: TradeProps){
    const draw = (g:any) => {
        g.lineStyle(2, 'brown', 2);
        g.beginFill('beige', 0.5);
        g.drawRoundedRect(props.width * 0.342, 0, props.width * 0.391, props.height * 1/4, 8)
        g.endFill();
    }

    return(
        <Container visible={true}>
            <Graphics draw={draw}/>
            
        </Container>
    )
}