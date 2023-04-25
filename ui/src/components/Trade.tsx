import {Container, Graphics, Sprite, Text} from '@pixi/react';
import TradeResourceSelection from './TradeResourceSelection';
import { useEffect, useRef, useState } from 'react';
import TradeParticipants from './TradeParticipants';
import { TextStyle } from 'pixi.js';
import {isEqual} from 'lodash';
import { Resources } from '../App';

interface TradeProps{
    height: number;
    width: number;
    visible: boolean;
    fontSize: number;
    resourcesAvailable: Resources;
    players?: any
}

export default function Trade(props: TradeProps){

    const baseValues = {'ore': 0, 'brick': 0, 'lumber': 0, 'wool': 0, 'grain': 0};
    const [resourcesOffered, setResourcesOffered] = useState({
        'ore': 0, 'brick': 0, 'lumber': 0, 'wool': 0, 'grain': 0
    })
    const [resourcesRequested, setResourcesRequested] = useState({
        'ore': 0, 'brick': 0, 'lumber': 0, 'wool': 0, 'grain': 0
    })
    const availablePlayers = useRef(['red', 'blue', 'green'])
    const [playersOfferedTo, setPlayersOfferedTo] = useState([])
    const draw = (g:any) => {
        g.clear();
        g.lineStyle(2, 'brown', 2);
        g.beginFill('beige', 1);
        g.drawRoundedRect(0, 0, props.width * 0.291, props.height * 0.75, 8)
        g.endFill();
    }

    function tradeHanlde(){

    }

    return(
        <Container x={props.width * 0.35} y={props.height * 0.05} visible={props.visible}>
            <Graphics draw={draw}/>
            <TradeResourceSelection offeredResources={resourcesOffered} height={props.height} width={props.width} updateMethod={setResourcesOffered} resources={props.resourcesAvailable}/>
            <Sprite image={'/assets/trade/transfer.png'} x={props.width * 0.126} y={props.height * 0.19} height={props.height * 0.04} width={props.width * 0.03}/>
            <TradeResourceSelection requestedResources={resourcesRequested}  height={props.height} width={props.width} updateMethod={setResourcesRequested} y={props.height * 0.25}/>
            <TradeParticipants height={props.height} width={props.width} updateMethod={setPlayersOfferedTo} available={availablePlayers.current} offered={playersOfferedTo}/>
            <Container x={props.width * 0.05} y={props.height * 0.63} alpha={(playersOfferedTo.length > 0 && !isEqual(resourcesOffered, baseValues) && !isEqual(resourcesRequested, baseValues)) ? 1 : 0.3} onclick={tradeHanlde}>
                <Sprite image={'/assets/trade/buttonLong_blue.png'} width={props.width * 0.2} height={props.height * 0.1}/>
                <Text x={props.width * 0.045} y={props.height * 0.005} text='Trade' alpha={(playersOfferedTo.length > 0 && !isEqual(resourcesOffered, baseValues) && !isEqual(resourcesRequested, baseValues)) ? 1 : 0.3} style={
                    new TextStyle({
                    fontFamily: 'sans-serif',
                    fontSize:  props.fontSize * 0.6,
                    fontWeight: '200',
                    fill: '#ffffff', // gradient
                    strokeThickness: 6,
                    letterSpacing: 5,
                    wordWrap: true,
                    wordWrapWidth: 440,
                })}/>
            </Container>
        </Container>
    )
}