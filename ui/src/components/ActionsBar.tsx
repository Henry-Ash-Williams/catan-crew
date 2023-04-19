import { Container, Graphics, Sprite, Text } from "@pixi/react";
import {TextStyle} from "pixi.js"
import { useCallback, useState } from "react";
import Card from "./Card";

interface ActionBarProps{
    width: number;
    height: number;
    fontSize: number;
    methods: any;
}

export default function ActionsBar(props: ActionBarProps){

    //Functions for api calls and changing state
    const [devAmounts, setDevAmounts] = useState({
        'hidden' : 0,
        'monopoly' : 0,
        'plenty' : 0,
        'road' : 0,
        'knight' : 0,
    })
    const buildRoad = ()=>{
        console.log("built")
    }
    const buildSettlement = ()=>{
        
    }
    const buildCity = ()=>{
        
    }
    const trade = ()=>{
        props.methods[0][0](!props.methods[0][1])
    }
    const endTurn = ()=>{
        
    }
    const buyDevCards = ()=>{
        
    }

    const draw = (g:any) => {
        g.clear();
        g.lineStyle(2, 'brown', 2);
        g.beginFill('beige', 1);
        g.drawRoundedRect(props.width * 0.342, 0, props.width * 0.391, props.height * 1/4, 8)
        g.endFill();
        g.beginFill('yellow', 0.8);
        g.drawRoundedRect(0, 0, props.width * 0.341, props.height * 1/4, 8)
        g.endFill();
    }

    return(
        <Container y={props.height * 0.845}>
            <Graphics draw={draw}/>
            <Container y={props.height * 0.003} x={0}>
                <Card resourceType='hidden' width={props.width} height={props.height} y={0} amount={devAmounts['hidden']} fontSize={props.fontSize}/>
                <Card resourceType='monopoly' width={props.width} height={props.height} x={props.width * 0.07} y={0} amount={devAmounts['monopoly']} fontSize={props.fontSize}/>
                <Card resourceType='plenty' width={props.width} height={props.height} x={props.width * 0.138} y={0} amount={devAmounts['plenty']} fontSize={props.fontSize}/>
                <Card resourceType='road' width={props.width} height={props.height} x={props.width * 0.206} y={0} amount={devAmounts['road']} fontSize={props.fontSize}/>
                <Card resourceType='knight' width={props.width} height={props.height} x={props.width * 0.274} y={0} amount={devAmounts['knight']} fontSize={props.fontSize}/>
            </Container>
            <Container x={props.width * 0.265} y={props.height * 0.01}>
                <Container x={props.width * 0.08} y={props.height * 0.015}>
                    <Sprite width={props.width * 0.06} height={props.height * 0.11} image={'/assets/menu/panel_brown.png'} onclick={buildRoad} interactive={true}/>
                    <Sprite width={props.width * 0.05} height={props.height * 0.08} x={props.width * 0.005} y={props.height * 0.014} image={'/assets/action-board/road.png'}/>
                </Container>
                <Container x={0.145 * props.width} y={props.height * 0.015}>
                    <Sprite width={props.width * 0.06} height={props.height * 0.11} image={'/assets/menu/panel_brown.png'} onclick={buildSettlement} interactive={true}/>
                    <Sprite width={props.width * 0.05} height={props.height * 0.08} x={props.width * 0.005} y={props.height * 0.014} image={'/assets/action-board/house.png'}/>
                </Container>
                <Container x={0.21 * props.width} y={props.height * 0.015}>
                    <Sprite width={props.width * 0.06} height={props.height * 0.11} image={'/assets/menu/panel_brown.png'} onclick={buildCity} interactive={true}/>
                    <Sprite width={props.width * 0.06} height={props.height * 0.095} x={0} y={props.height * 0.014} image={'/assets/action-board/town.png'}/>
                </Container>
                <Container x={0.275 * props.width} y={props.height * 0.015}>
                    <Sprite width={props.width * 0.06} height={props.height * 0.11} image={'/assets/menu/panel_brown.png'} onclick={buyDevCards} interactive={true}/>
                    <Sprite width={props.width * 0.05} height={props.height * 0.07} x={props.width * 0.005} y={props.height * 0.014} image={'/assets/action-board/dev.png'}/>
                </Container>
                <Container x={0.34 * props.width} y={props.height * 0.015}>
                    <Sprite width={props.width * 0.06} height={props.height * 0.11} image={'/assets/menu/panel_brown.png'} onclick={trade} interactive={true}/>
                    <Sprite width={props.width * 0.05} height={props.height * 0.07} x={props.width * 0.005} y={props.height * 0.014} image={'/assets/action-board/trade.png'}/>
                </Container>
                <Container x={0.405 * props.width} y={props.height * 0.015}>
                    <Sprite width={props.width * 0.06} height={props.height * 0.11} image={'/assets/menu/panel_brown.png'} onclick={endTurn} interactive={true}/>
                    <Sprite width={props.width * 0.05} height={props.height * 0.07} x={props.width * 0.005} y={props.height * 0.014} image={'/assets/action-board/end.png'}/>
                </Container>
            </Container>

            {/* {actions.map((a:any) => {
                xOffset += 0.09;
                return <Container>
                    <Sprite width={props.width * 0.08} height={props.height * 1/8} x={props.width * (xOffset + 0.01)} image={'/assets/menu/panel_brown.png'}/>
                    <Sprite width={props.width * 0.05} height={props.height * 0.08} x={props.width} y={props.height * 0.014} image={a[1]} onclick={a[0]} interactive={true}/>
                </Container>
            })} */}
        </Container>
    )
}