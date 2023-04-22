import { Container, Sprite, Text } from '@pixi/react';
import { TextStyle } from 'pixi.js';

interface TileData {
    owner?: string
    isCity?: boolean
    direction?: number

}

interface IntersectionComponentProps {
    x: number
    y: number
    size: number
    tile: TileData
    tileIndex: number
    interactive: boolean
    build: (arg0: string, arg1: number) => void
    
    // onClick: (arg0: string, arg1: number) => void
}

function IntersectionComponent(props: IntersectionComponentProps) {
    const handleClick = () => {
        if(props.tile.owner != undefined) {
            console.log("Clicked on settlements", props.tileIndex)
            props.build("cities", props.tileIndex)
        } else {
            console.log("Clicked on empty intersection", props.tileIndex)
            props.build("settlements", props.tileIndex)


        }
    }

    let tile: React.ReactElement[] = [<Sprite x={0} y={0} width={props.size} height={props.size} anchor={0.5} image={"../assets/board/path/tile/grass_N.png"} interactive={props.interactive} onclick={handleClick} alpha={props.interactive? 0.5 : 1}/>]
    if(props.tile.direction == 1) {
        tile.push(<Sprite x={0} y={0} width={props.size} height={props.size} anchor={0.5} image={"../assets/board/intersection/interesection2_1.png"} tint={props.tile.owner} alpha={props.interactive? 0.5 : 1} />)
    } else if (props.tile.direction == 2) {
        tile.push(<Sprite x={0} y={0} width={props.size} height={props.size} anchor={0.5} image={"../assets/board/intersection/interesection2_2.png"} tint={props.tile.owner} alpha={props.interactive? 0.5 : 1}/>)
    }else if (props.tile.direction == 3) {
        tile.push(<Sprite x={0} y={0} width={props.size} height={props.size} anchor={0.5} image={"../assets/board/intersection/interesection2_3.png"} tint={props.tile.owner} alpha={props.interactive? 0.5 : 1}/>)
    }else if (props.tile.direction == 4) {
        tile.push(<Sprite x={0} y={0} width={props.size} height={props.size} anchor={0.5} image={"../assets/board/intersection/interesection2_N.png"} tint={props.tile.owner} alpha={props.interactive? 0.5 : 1}/>)
    }else if (props.tile.direction == 5) {
        tile.push(<Sprite x={0} y={0} width={props.size} height={props.size} anchor={0.5} image={"../assets/board/intersection/interesection1_2.png"} tint={props.tile.owner} alpha={props.interactive? 0.5 : 1}/>)
    }else if (props.tile.direction == 6) {
        tile.push(<Sprite x={0} y={0} width={props.size} height={props.size} anchor={0.5} image={"../assets/board/intersection/interesection1_3.png"} tint={props.tile.owner} alpha={props.interactive? 0.5 : 1}/>)
    }else if (props.tile.direction == 7) {
        tile.push(<Sprite x={0} y={0} width={props.size} height={props.size} anchor={0.5} image={"../assets/board/intersection/interesection1_1.png"} tint={props.tile.owner} alpha={props.interactive? 0.5 : 1}/>)
    }else if (props.tile.direction == 8) {
        tile.push(<Sprite x={0} y={0} width={props.size} height={props.size} anchor={0.5} image={"../assets/board/intersection/interesection1_N.png"} tint={props.tile.owner} alpha={props.interactive? 0.5 : 1}/>)
    }

     if (props.tile.isCity) {
        tile.pop();
        tile.push(<Sprite x={0} y={0} width={props.size} height={props.size} anchor={0.5} image={"../assets/board/intersection/city/city_N.png"} tint={props.tile.owner}/>)
    } else if (props.tile.owner) {
        tile.push(<Sprite x={0} y={0} width={props.size} height={props.size} anchor={0.5} image={"../assets/board/intersection/settlement/settlement_N.png"} tint={props.tile.owner} alpha={props.interactive? 0.5 : 1}/>)
    }
    // tile.push(
    //             <Text
    //                 text={props.tileIndex.toString()}
    //                 anchor={0.5}
    //                 x={0}
    //                 y={-20}
    //                 style={
    //                     new TextStyle({
    //                     align: 'center',
    //                     fontFamily: '"Source Sans Pro", Helvetica, sans-serif',
    //                     fontSize: 30,
    //                     fontWeight: '200',
    //                     fill: '#ffffff', // gradient
    //                     stroke: '#01d27e',
    //                     strokeThickness: 5,
    //                     letterSpacing: 5,
    //                     dropShadow: true,
    //                     dropShadowColor: '#ccced2',
    //                     dropShadowBlur: 4,
    //                     dropShadowAngle: Math.PI / 6,
    //                     dropShadowDistance: 6,
    //                     wordWrap: true,
    //                     wordWrapWidth: 440,
    //                 })}
    //             />
    // )

    return (
        <Container x={props.x} y={props.y} width={props.size} height={props.size}>
            {tile.map((x) => (
                <>{x}</>
            ))}
        </Container>
    )
}

export { IntersectionComponent }