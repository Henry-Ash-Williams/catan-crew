import { Container, Sprite, Text } from '@pixi/react';
import { TextStyle } from 'pixi.js';

interface TileData {
    owner?: string
    direction?: number
}

interface PathComponentProps {
    tileIndex: number
    x: number,
    y: number,
    size: number
    tile: TileData
    build: (args0: string, args1: number) => void
    interactive: boolean

}

function PathComponent(props: PathComponentProps) {
    const handleClick = () => {
        props.build("path", props.tileIndex)
    }
    
    let tile: React.ReactElement[] = [<Sprite x={0} y={0} width={props.size} height={props.size} anchor={0.5} image={"../assets/board/path/tile/grass_N.png"} interactive={props.interactive} onclick={handleClick} alpha={props.interactive? 0.5 : 1}/>]

    if(props.tile.direction == 3) {
        tile.push(<Sprite x={0} y={0} width={props.size} height={props.size} anchor={0.5} image={"../assets/board/path/path_straight_N.png"} tint={props.tile.owner} rotation={0} alpha={props.interactive? 0.5 : 1}/>)
    } else if(props.tile.direction == 1) {
        tile.push(<Sprite x={0} y={0} width={props.size} height={props.size} anchor={0.5} image={"../assets/board/path/path_NE.png"} tint={props.tile.owner} rotation={0} alpha={props.interactive? 0.5 : 1}/>)
    } else if(props.tile.direction == 2) {
        tile.push(<Sprite x={0} y={0} width={props.size} height={props.size} anchor={0.5} image={"../assets/board/path/path_NW.png"} tint={props.tile.owner} rotation={0} alpha={props.interactive? 0.5 : 1}/>)
    }
    // tile.push(
    //     <Text
    //         text={props.text}
    //         anchor={0.5}
    //         x={0}
    //         y={-20}
    //         style={
    //             new TextStyle({
    //             align: 'center',
    //             fontFamily: '"Source Sans Pro", Helvetica, sans-serif',
    //             fontSize: 30,
    //             fontWeight: '200',
    //             fill: '#ffffff', // gradient
    //             stroke: '#01d27e',
    //             strokeThickness: 5,
    //             letterSpacing: 5,
    //             dropShadow: true,
    //             dropShadowColor: '#ccced2',
    //             dropShadowBlur: 4,
    //             dropShadowAngle: Math.PI / 6,
    //             dropShadowDistance: 6,
    //             wordWrap: true,
    //             wordWrapWidth: 440,
    //         })}
    //     />
    // )
    return (
        <Container x={props.x} y={props.y} width={props.size} height={props.size}>
            {tile.map((x) => (
                <>{x}</>
            ))}
        </Container>
        )
}

export { PathComponent }

