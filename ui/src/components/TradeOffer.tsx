import { Container, Graphics, Sprite } from "@pixi/react"

interface TradeOfferProps{
    height: number;
    width: number;
    fontSize: number;

}

export default function TradeOffer(props: TradeOfferProps){
    const draw = (g:any) => {
        g.clear();
        g.lineStyle(2, 'brown', 2);
        g.beginFill('beige', 1);
        g.drawRoundedRect(0, 0, props.width * 0.291, props.height * 0.55, 8)
        g.endFill();
    }

    return(
        <Container>
            <Graphics/>
        </Container>
    )
}