import {Sprite, Graphics, Container, Text} from '@pixi/react';
import Card from './Card';

interface TradeResourceSelectionProps{
    height: number;
    width: number;
    updateMethod: Function;
    offeredResources?: any;
    requestedResources?: any;
    resources?: any // Object of resources: resource type : current amount
    y?: number;
}

export default function TradeResourceSelection(props: TradeResourceSelectionProps){
    const workingResources = props.offeredResources ? props.offeredResources : props.requestedResources;
    let xOffset = -props.width * 0.047;
    const resourcesType : any = [
        ['brick','../assets/board/archive/brick.svg', '#f55442'],
        ['wool', "../assets/board/archive/wool.svg", '#dec6c3'],
        ['ore', "../assets/board/archive/ore.svg", '#6dc0e3'],
        ['lumber', "../assets/board/archive/lumber.svg", '#93f542'],
        ['grain',"../assets/board/archive/grain.svg", 'orange']
    ]

    function handleArrowLeft(resource : string){
        if (workingResources[resource] > 0){
            props.updateMethod({...workingResources, [resource]: workingResources[resource] - 1})
        }
    }

    function handleArrowRight(resource : string){
        if (props.resources && props.offeredResources[resource] === props.resources[resource]){}
        else{
            props.updateMethod({...workingResources, [resource]: workingResources[resource] + 1})
        }
    }

    return(
        <Container y={props.y}>
            {resourcesType.map((resource : any)=>
            {
                xOffset += props.width * 0.055;
                return (
                    <Container x={xOffset} y={10}>
                        <Sprite image={'/assets/menu/panel_beige.png'} width={props.width * 0.05} height={props.height * 0.11} tint={resource[2]}/>
                        <Sprite image={resource[1]} width={props.width * 0.035} height={props.height * 0.06} x={props.width * 0.007} y={props.height * 0.03}/>
                        <Container y={props.height * 0.12}>
                            <Text x={props.width * 0.02} y={props.height * -0.005} text={workingResources[resource[0]]}/>
                            <Sprite image={'/assets/trade/arrowBlue_left.png'} eventMode='static' onclick={()=>{handleArrowLeft(resource[0])}} alpha={workingResources[resource[0]] == 0 ? 0.5 : 1}/>
                            <Sprite x={props.width * 0.036} image={'/assets/trade/arrowBlue_right.png'} eventMode='static' onclick={()=>{handleArrowRight(resource[0])}} alpha={props.resources && workingResources[resource[0]] === props.resources[resource[0]] ? 0.5 : 1}/>
                        </Container>
                    </Container>
                )
            }
            )}
        </Container>
    )
}