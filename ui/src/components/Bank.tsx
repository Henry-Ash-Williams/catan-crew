import {Container, Graphics, Sprite} from '@pixi/react'
import Card from './Card';

interface BankProps{
    height: number;
    width: number;
}

export default function Bank(props: BankProps){
    const draw = (g: any) => {
        g.clear();
        g.lineStyle(2, 'brown', 2);
        g.beginFill('beige', 0.8);
        g.drawRoundedRect(0, -props.height * 0.008, props.width * 0.31, props.height * 0.11, 8)
        g.endFill();
    }

    return(
        <Container x={props.width * 0.7}>
            <Graphics draw={draw}/>
            <Container y={props.height * 0.005}>
                <Card resourceType='ore' width={props.width * 0.6} height={props.height * 0.6} amount={19} x={props.width * 0.056} fontSize={props.height / 9}/>
                <Card resourceType='wool' width={props.width * 0.6} height={props.height * 0.6} amount={19} x={props.width * 0.104} fontSize={props.height / 9}/>
                <Card resourceType='lumber' width={props.width * 0.6} height={props.height * 0.6} amount={19} x={props.width * 0.152} fontSize={props.height / 9}/>
                <Card resourceType='grain' width={props.width * 0.6} height={props.height * 0.6} amount={19} x={props.width * 0.2} fontSize={props.height / 9}/>
                <Card resourceType='brick' width={props.width * 0.6} height={props.height * 0.6} amount={19} x={props.width * 0.248} fontSize={props.height / 9}/>
            </Container>
            <Sprite image={'/assets/leaderboard-icons/bank.png'} height={props.height * 0.07} width={props.width * 0.04} x={props.width * 0.007} y={props.height * 0.014}/>
        </Container>
    )
}