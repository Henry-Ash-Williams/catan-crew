import { Container, Sprite, Text } from "@pixi/react"
import { TextStyle, Graphics } from "pixi.js"
// import { Graphics } from "@pixi/react"

interface Coordinates {
    x: number,
    y: number
}

interface ResourceTile {
    resource?: string
    number_token?: number
}

interface ResourceTileProps{
    tileIndex: number
    x: number
    y: number
    size: number
    tile: ResourceTile
    interactive: boolean
    onClick: (coordinates: Coordinates, tileIndex: number) => void
}

function ResourceTileComponent(props: ResourceTileProps){
    const x = props.x
    const y = props.y
    const handleClick = () => {
        props.onClick({ x, y }, props.tileIndex)
    }
    let tile : React.ReactElement[] = []

    if (props.tile.resource == "brick") {
        tile.push(<Sprite x={0} y={0} width={props.size} height={props.size} anchor={0.5} image={"/assets/board/resource/brick/dirt_N.png"} interactive={props.interactive} onclick={handleClick} alpha={props.interactive? 0.5 : 1}/>)
    } else if (props.tile.resource == "grain") {
        tile.push(<Sprite x={0} y={0} width={props.size} height={props.size} anchor={0.5} image={"/assets/board/resource/grain/building_farm_N.png"} interactive={props.interactive} onclick={handleClick} alpha={props.interactive? 0.5 : 1}/>)
    } else if (props.tile.resource == "lumber") {
        tile.push(<Sprite x={0} y={0} width={props.size} height={props.size} anchor={0.5} image={"/assets/board/resource/lumber/grass_forest_N.png"} interactive={props.interactive} onclick={handleClick} alpha={props.interactive? 0.5 : 1}/>)
    } else if (props.tile.resource == "ore") {
        tile.push(<Sprite x={0} y={0} width={props.size} height={props.size} anchor={0.5} image={"/assets/board/resource/ore/stone_hill_N.png"} interactive={props.interactive} onclick={handleClick} alpha={props.interactive? 0.5 : 1}/>)
    } else if (props.tile.resource == "wool") {
        tile.push(<Sprite x={0} y={0} width={props.size} height={props.size} anchor={0.5} image={"/assets/board/resource/wool/building_sheep_N.png"} interactive={props.interactive} onclick={handleClick} alpha={props.interactive? 0.5 : 1}/>)
    } else if (props.tile.resource == "desert") {
        tile.push(<Sprite x={0} y={0} width={props.size} height={props.size} anchor={0.5} image={"/assets/board/resource/desert/sand_rocks_N.png"} interactive={props.interactive} onclick={handleClick} alpha={props.interactive? 0.5 : 1}/>)
    } else if (props.tile.resource == "sea") {
        tile.push(<Sprite x={0} y={0} width={props.size} height={props.size} anchor={0.5} image={"/assets/board/resource/sea/water_N.png"}/>)
    }

    if (props.tile.number_token) {
        tile.push(
            <Text
                text={props.tile.number_token.toString()}
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
    }

    return(
        <Container x={props.x} y={props.y} width={props.size} height={props.size} >
            {tile.map((x) => (
                <>{x}</>
            ))}
            
        </Container>
    )
}

export { ResourceTileComponent }