import { Container, Sprite } from '@pixi/react';

interface Coordinates {
    x: number,
    y: number
}
interface IntersectionComponentProps {
    x: number
    y: number
    size: number
    owner?: number
    isCity?: boolean
    onClick: (coordinates: Coordinates) => void
}

function IntersectionComponent(props: IntersectionComponentProps) {
    let tile: React.ReactElement[] = [<Sprite x={0} y={0} width={props.size*4} height={props.size*4} anchor={0.5} image={"../assets/board/path/tile/grass_N.png"}/>,
            <Sprite x={0} y={-12} width={props.size*4} height={props.size*4} anchor={0.5} image={"../assets/board/path/path_intersectionF_N.png"}/>]
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