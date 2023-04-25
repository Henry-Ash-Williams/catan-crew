import { Container, Graphics, Sprite, Text } from "@pixi/react";
import {TextStyle} from "pixi.js"
import { useCallback, useState } from "react";
import Card from "./Card";

interface ActionBarProps{
    getLocationsFor: Function;
    action: Function;
    tradeFunction : [Function, boolean];
    width: number;
    height: number;
    fontSize: number;
    availableActions: string[];
    // devCards: any
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
    const actions : any = {} 
    props.availableActions.forEach((action: string) => {
        actions[action] = true;
    })

    const buildRoad = ()=>{
        props.getLocationsFor('roads', true)
    }
    const buildSettlement = ()=>{
        props.getLocationsFor('settlements', true)
    }
    const buildCity = ()=>{
        props.getLocationsFor('cities', true)
    }
    const trade = ()=>{
        props.tradeFunction[0](!props.tradeFunction[1])
    }
    const endTurn = ()=>{
        props.action('end_turn')
    }
    const buyDevCards = ()=>{
        props.action('buy_dev_card')
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
                <Container x={props.width * 0.08} y={props.height * 0.015} alpha={actions['Build a road'] ? 1 : 0.5}>
                    <Sprite width={props.width * 0.06} height={props.height * 0.11} image={'/assets/menu/panel_brown.png'} onclick={buildRoad} eventMode={actions['Build a road'] ? "static" : 'none'}/>
                    <Sprite width={props.width * 0.05} height={props.height * 0.08} x={props.width * 0.005} y={props.height * 0.014} image={'/assets/action-board/road.png'}/>
                </Container>
                <Container x={0.145 * props.width} y={props.height * 0.015} alpha={actions['Build a settlement'] ? 1 : 0.5}>
                    <Sprite width={props.width * 0.06} height={props.height * 0.11} image={'/assets/menu/panel_brown.png'} onclick={buildSettlement} eventMode={actions['Build a settlement'] ? "static" : 'none'}/>
                    <Sprite width={props.width * 0.05} height={props.height * 0.08} x={props.width * 0.005} y={props.height * 0.014} image={'/assets/action-board/house.png'}/>
                </Container>
                <Container x={0.21 * props.width} y={props.height * 0.015} alpha={actions['Upgrade a settlement'] ? 1 : 0.5}>
                    <Sprite width={props.width * 0.06} height={props.height * 0.11} image={'/assets/menu/panel_brown.png'} onclick={buildCity} eventMode={actions['Upgrade a settlement'] ? "static" : 'none'}/>
                    <Sprite width={props.width * 0.06} height={props.height * 0.095} x={0} y={props.height * 0.014} image={'/assets/action-board/town.png'}/>
                </Container>
                <Container x={0.275 * props.width} y={props.height * 0.015} alpha={actions['Buy a development card'] ? 1 : 0.5}>
                    <Sprite width={props.width * 0.06} height={props.height * 0.11} image={'/assets/menu/panel_brown.png'} onclick={buyDevCards} eventMode={actions['Buy a development card'] ? "static" : 'none'}/>
                    <Sprite width={props.width * 0.05} height={props.height * 0.07} x={props.width * 0.005} y={props.height * 0.014} image={'/assets/action-board/dev.png'}/>
                </Container>
                <Container x={0.34 * props.width} y={props.height * 0.015} alpha={actions['Propose a trade'] ? 1 : 0.5}>
                    <Sprite width={props.width * 0.06} height={props.height * 0.11} image={'/assets/menu/panel_brown.png'} onclick={trade} eventMode={actions['Propose a trade'] ? "static" : 'none'}/>
                    <Sprite width={props.width * 0.05} height={props.height * 0.07} x={props.width * 0.005} y={props.height * 0.014} image={'/assets/action-board/trade.png'}/>
                </Container>
                <Container x={0.405 * props.width} y={props.height * 0.015} alpha={actions['End turn'] ? 1 : 0.5}>
                    <Sprite width={props.width * 0.06} height={props.height * 0.11} image={'/assets/menu/panel_brown.png'} onclick={endTurn} eventMode={actions['End turn'] ? "static" : 'none'}/>
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