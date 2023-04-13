import { Container, Sprite, Text } from '@pixi/react';
import { TextStyle } from "pixi.js"

interface IntersectionComponentProps {
    x: number
    y: number
    size: number
    owner?: string
    isCity?: boolean
    direction: number | undefined
    key: string
}

function IntersectionComponent(props: IntersectionComponentProps) {
    let tile: React.ReactElement[] = [<Sprite x={0} y={0} width={props.size} height={props.size} anchor={0.5} image={"../assets/board/path/tile/grass_N.png"}/>]
    if(props.direction == 1) {
        tile.push(<Sprite x={0} y={0} width={props.size} height={props.size} anchor={0.5} image={"../assets/board/intersection/interesection1_N.png"} tint={props.owner} />)
    } else if (props.direction == 2) {
        tile.push(<Sprite x={0} y={0} width={props.size} height={props.size} anchor={0.5} image={"../assets/board/intersection/interesection2_N.png"} tint={props.owner}/>)
    }
     if (props.isCity) {
        tile.pop();
        tile.push(<Sprite x={0} y={0} width={props.size} height={props.size} anchor={0.5} image={"../assets/board/intersection/city/city_N.png"} tint={props.owner}/>)
    } else if (props.owner) {
        tile.push(<Sprite x={0} y={0} width={props.size} height={props.size} anchor={0.5} image={"../assets/board/intersection/settlement/settlement_N.png"} tint={props.owner}/>)
    }
    tile.push(
                <Text
                    text={props.key}
                    anchor={0.5}
                    x={0}
                    y={-20}
                    style={
                        new TextStyle({
                        align: 'center',
                        fontFamily: '"Source Sans Pro", Helvetica, sans-serif',
                        fontSize: 30,
                        fontWeight: '200',
                        fill: '#ffffff', // gradient
                        stroke: '#01d27e',
                        strokeThickness: 5,
                        letterSpacing: 5,
                        dropShadow: true,
                        dropShadowColor: '#ccced2',
                        dropShadowBlur: 4,
                        dropShadowAngle: Math.PI / 6,
                        dropShadowDistance: 6,
                        wordWrap: true,
                        wordWrapWidth: 440,
                    })}
                />
    )

    return (
        <Container x={props.x} y={props.y} width={props.size} height={props.size}>
            {tile.map((x) => (
                <>{x}</>
            ))}
        </Container>
    )
}

export { IntersectionComponent }