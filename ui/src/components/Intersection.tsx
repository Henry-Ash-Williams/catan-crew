import { Container, Sprite } from '@pixi/react';

interface IntersectionComponentProps {
    x: number
    y: number
    size: number
    owner?: number
    isCity?: boolean
    direction: number | undefined
}

function IntersectionComponent(props: IntersectionComponentProps) {
    let tile: React.ReactElement[] = [<Sprite x={0} y={0} width={props.size} height={props.size} anchor={0.5} image={"../assets/board/path/tile/grass_N.png"}/>]
    if(props.direction == 2) {
        tile.push(<Sprite x={0} y={0} width={props.size} height={props.size} anchor={0.5} image={"../assets/board/intersection/interesection1_N.png"}/>)
    } else if (props.direction == 1) {
        tile.push(<Sprite x={0} y={0} width={props.size} height={props.size} anchor={0.5} image={"../assets/board/intersection/interesection2_N.png"}/>)
    }
    if (props.owner) {
        tile.push(<Sprite x={0} y={-12} width={props.size*4} height={props.size*4} anchor={0.5} image={"../assets/board/intersection/unit_house_E.png"} tint={props.owner}/>)
    } else if (props.isCity) {
        tile.pop();
        tile.push(<Sprite x={0} y={-12} width={props.size*4} height={props.size*4} anchor={0.5} image={"../assets/board/intersection/unit_houseLarge_E.png"} tint={props.owner}/>)
    }

    return (
        <Container x={props.x} y={props.y} width={props.size} height={props.size}>
            {tile.map((x) => (
                <>{x}</>
            ))}
        </Container>
    )
}

export { IntersectionComponent }