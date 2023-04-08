import { Container, Sprite } from '@pixi/react';

interface Coordinates {
    x: number,
    y: number
}

interface PathComponentProps {
    x: number,
    y: number,
    size: number
    direction?: number,
    owner?: number
    onClick: (coordinates: Coordinates) => void
}

function PathComponent(props: PathComponentProps) {
    let tile: React.ReactElement[] = [<Sprite x={0} y={0} width={props.size} height={props.size} anchor={0.5} image={"../assets/board/path/tile/grass_N.png"}/>]

    if(props.direction == 1) {
        tile.push(<Sprite x={0} y={0} width={props.size} height={props.size} anchor={0.5} image={"../assets/board/path/path_straight_N.png"} tint={props.owner} rotation={0}/>)
    } else if(props.direction == 2) {
        tile.push(<Sprite x={0} y={0} width={props.size} height={props.size} anchor={0.5} image={"../assets/board/path/path_NE.png"} tint={props.owner} rotation={0}/>)
    } else if(props.direction == 3) {
        tile.push(<Sprite x={0} y={0} width={props.size} height={props.size} anchor={0.5} image={"../assets/board/path/path_NW.png"} tint={props.owner} rotation={0}/>)
    }
    return (
        <Container x={props.x} y={props.y} width={props.size} height={props.size}>
            {tile.map((x) => (
                <>{x}</>
            ))}
        </Container>
        )
}

export { PathComponent }

