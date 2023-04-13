import { Container, Graphics, Sprite, Text } from "@pixi/react";
import {TextStyle} from "pixi.js"
import { useCallback } from "react";
import Card from "./Card";

interface ActionBarProps{
    width: number;
    height: number
}

export default function ActionsBar(props: ActionBarProps){

    
    //Functions for api calls and changing state

    const buildRoad = ()=>{
        console.log("built")
    }
    const buildSettlement = ()=>{
        
    }
    const buildCity = ()=>{
        
    }
    const trade = ()=>{
        
    }
    const endTurn = ()=>{
        
    }
    const buyDevCards = ()=>{
        
    }
    // const actions = [
    //     [buildRoad, '/assets/action-board/road.png'],
    //     [buildSettlement, '/assets/action-board/house.png'], 
    //     [buildCity, '/assets/action-board/town.png'],
    //     [trade, '/assets/action-board/trade.png'],
    //     [buyDevCards, '/assets/action-board/dev.png'],
    //     [endTurn, '/assets/action-board/end.png']
    // ]

    const draw = (g:any) => {
        g.clear();
        g.beginFill('beige', 0.8);
        g.drawRoundedRect(props.width * 0.28, 0, props.width * 0.405, props.height * 1/4, 8)
        g.endFill();
        g.beginFill('yellow', 0.8);
        g.drawRoundedRect(0, 0, props.width * 0.275, props.height * 1/4, 8)
        g.endFill();
    }

    return(
        <Container y={props.height * 0.845}>
            <Graphics draw={draw}/>
            <Container>
                <Card resourceType='ore' width={props.width} height={props.height} y={0} amount={2}/>
                <Card resourceType='grain' width={props.width} height={props.height} x={props.width * 0.07} y={0} amount={0}/>
                <Card resourceType='brick' width={props.width} height={props.height} x={props.width * 0.138} y={0} amount={1}/>
                <Card resourceType='ore' width={props.width} height={props.height} x={props.width * 0.206} y={0} amount={1}/>
            </Container>
            <Container x={props.width * 0.21}>
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