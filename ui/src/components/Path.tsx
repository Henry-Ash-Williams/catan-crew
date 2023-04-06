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
    let tile: React.ReactElement[] = [<Sprite x={0} y={0} width={props.size*4} height={props.size*4} anchor={0.5} image={"../assets/board/path/tile/grass_N.png"}/>,
            <Sprite x={0} y={-12} width={props.size*4} height={props.size*4} anchor={0.5} image={"../assets/board/path/path_straight_N.png"} tint={props.owner}/>]
    return (
        <Container x={props.x} y={props.y} width={props.size} height={props.size}>
            {tile.map((x) => (
                <>{x}</>
            ))}
        </Container>
        )
}

export { PathComponent }

