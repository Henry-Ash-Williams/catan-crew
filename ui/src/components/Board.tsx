import { Container } from "@pixi/react";
// import board from  "./end_board.json";
import { IntersectionComponent } from "./Intersection";
import { PathComponent } from "./Path";
import { ResourceTileComponent } from "./Resource";
import { KnightComponent } from "./Knight";
import { useEffect, useState } from "react";

interface BoardComponentProps {
    height: number,
    width: number,
    size: number,
    boardStateJson: Object
    setBoardState: (boardState: string) => void,
    clickable: number[]
    build: (args0: string, args1: number) => void
    setTileData: Function
    robber: (args0: number) => void
}

export interface Board {
    board_size: number
    directions: number[]
    tiles: Tile[]
}

interface Tile {
    type: string
    location: number
    harbor?: boolean //not implemented
    resource?: string | undefined
    number_token?: number | undefined 
    owner?: string | undefined
    isCity?: boolean | undefined
    direction?: number | undefined
}

interface TileData {
    tile: Tile,
    key: number,
    x: number,
    y: number,
    interactive: boolean
    build: (args0: string, args1: number) => void
}

interface Coordinates {
    x: number,
    y: number
}


function initTiles(props: BoardComponentProps) {
    // console.log(typeof(props.boardState))
    // console.log("BOARD STATE:\n", props.boardState + "\n")
    const board = props.boardStateJson as Board
    // console.log("SERIALISED:\n", board)
    // console.log(typeof(board))
    
    let tiles: Tile[] = (board.tiles as Array<
        { type: string
        location: number
        resource?: string | undefined
        harbor?: boolean | null
        number_token?: number | undefined
        owner?: string | undefined
        isCity?: boolean | undefined
        direction?: number | undefined}>).map(tile => {
        return{
            type: tile.type,
            location: tile.location,
            resource: tile.resource ? tile.resource : undefined,
            harbour: tile.harbor ? tile.harbor : false,
            number_token: tile.number_token ? tile.number_token : undefined,
            owner: tile.owner ? tile.owner : undefined,
            isCity: tile.isCity ? tile.isCity : undefined,
            direction: tile.direction ? tile.direction : undefined
        }
        });
    // console.log(tiles.length)

    // x and y values for center tile
    let x0 = props.width/2;
    let y0 = -50 + props.height/2;

    let east = board.directions[0];
    let northEast = board.directions[1];

    let radius = 50;
    let radiusToFace = (radius * Math.sqrt(3) / 2)*1.05; // Better way to calculate radiusToFace

    let n = tiles.length; // number of tiles

    // let tile_map = new Map();
    let tileDatas: Map<number, TileData> = new Map();

    // q will be the number of layers of tiles around the center tile
    // setting q to 1 will wrap the center tile in only one layer
    let q = props.size-3;

    // j is the index for the row of tiles whose locations are being calculated
    // j =  q corresponds to the topmost row of tiles
    // j = -q corresponds to the bottom-most
    for(let j = q; j >= -q; j--){
        // i will be the index for the horizontal axis
        // the lower i is the more the tile is to the left and vice versa
        for(let i = -q; i <= q; i++){
            // some combinations of (i,j) will fall outside the hexagon, ignore these
            if (!(-q<=i+j && i+j<=q)){continue;}
            // calculate the x and y coordinates and the ctx for the current tile
            let x = x0 + i*radiusToFace + j*(radiusToFace/2);
            let y = y0 - j*(radius/2.6);  // This used to be radius/2.4 , but I think 2.6 works better
            let ctx = (i*east + j*northEast + n) % n;
            // add them to tileDatas
            console.log(ctx)
            tileDatas.set(ctx, {tile: tiles[ctx], key: structuredClone(ctx), x: x, y: y, interactive: false, build: props.build});
        }
    }

    // console.log(tileDatas)

    // if tile is a resource tile, set its surrounding tiles type to ChildResource
    tileDatas.forEach(function(value, key) {
        if (value.tile.type == "Resource") {
            for (let i = 0; i < 6; i++) {
                // console.log((n + key + board.directions[i]) % n)
                // if the index for the child node can't be found in tileDatas, skip it
                if(!tileDatas.has((n + key + board.directions[i]) % n)){continue;}
                var temp = tileDatas.get((n + key + board.directions[i]) % n)!
                // console.log(temp)
                temp.tile.type = "ChildResource"
                temp.tile.resource = value.tile.resource
            }
        }
    })

    // let knight = {x: x0, y: y0}
    // tileDatas.forEach(function(value, key) {
    //     if(value.tile.type == "Intersection") {
    //         tile_map.set(key, <IntersectionComponent
    //             key={key}
    //             x={value.x}
    //             y={value.y}
    //             size={radius}
    //             direction={value.tile.direction? value.tile.direction : undefined}
    //             owner={value.tile.owner}
    //             isCity={value.tile.isCity}
    //             interactive={props.clickable.includes(key)? true : false}
    //             />)
    //     } else if(value.tile.type == "PathTile") {
    //         tile_map.set(key, <PathComponent
    //             key={key}
    //             x={value.x}
    //             y={value.y}
    //             size={radius}
    //             direction={value.tile.direction}
    //             text={key.toString()}
    //             interactive={props.clickable.includes(key)? true : false}
    //             onClick={props.build}
    //             owner={value.tile.owner}
    //             />)
    //     } else if(value.tile.type == "Resource") {
    //         tile_map.set(key, <ResourceTileComponent
    //             key={key}
    //             x={value.x}
    //             y={value.y}
    //             size={radius}
    //             number_token={value.tile.number_token}
    //             resource={value.tile.resource}
    //             onClick={handleClick}
    //             />)
    //         if(value.tile.resource == "desert") {
    //             knight = {x: value.x, y: value.y}
    //         }
    //     } else if(value.tile.type == "ChildResource") {
    //         tile_map.set(key, <ResourceTileComponent
    //             key={key}
    //             x={value.x}
    //             y={value.y}
    //             size={radius}
    //             resource={value.tile.resource}
    //             onClick={handleClick}
    //             />)
    //     }
    // })
   

    return tileDatas
} 

function sortMap(map: Map<number, TileData>): Map<number, TileData> {
    const entries = Array.from(map.entries());
    entries.sort(([a, aVal], [b, bVal]) => {
    if (aVal.y === bVal.y) {
      return bVal.x - aVal.x;
    } else {
      return aVal.y - bVal.y;
    }
  });
  return new Map(entries);
}

function getCoordinatesFromKey(key: number, components: JSX.Element[]): {x: number, y: number} {
    const component = components.find((c) => c.key === key)

    if(!component) {
        throw Error("No component found with key");
    }
    const {x, y} = component.props
    return {x, y}
}

function BoardComponent(props: BoardComponentProps){
    const initBoard = () => {
        // console.log(props.boardState)
        let boardInit = initTiles(props)
        return boardInit
    }
    const handleResourceClick = (coordinates: Coordinates, tileIndex: number) => {
        console.log(coordinates)
        props.robber(tileIndex)
        // setKnightPosition(coordinates)
    }

    let clickable = structuredClone(props.clickable)

    useEffect (() => {
        if(clickable != props.clickable) {
            console.log("clickable changed")
            props.clickable.map((c: number) => {
                console.log(c)
                // boardState.set(c, {...boardState.get(c)!, tile.interactive: true})
                let a = boardState.get(c)!
                a.interactive = true
                boardState.set(c, a)
            })
            clickable = structuredClone(props.clickable)
            return
        }
    })

    const [boardState, setBoardState] = useState<Map<number, TileData>>(initBoard)

    // const [knightPosition, setKnightPosition] = useState<Coordinates>(boardState.knight)

    // props.setTileData(boardState.tiles)
    
    return (
        <Container>
            {Array.from(boardState).map((t) => {
                switch (t[1].tile.type){
                    case 'Intersection':
                        return <IntersectionComponent
                            tileIndex={t[1].key}
                            x={t[1].x}
                            y={t[1].y}
                            tile={t[1].tile}
                            size = {50}
                            interactive={t[1].interactive}
                            build={t[1].build}/>
                        break;
                    case 'PathTile':
                        return <PathComponent
                            tileIndex={t[1].key}
                            x={t[1].x}
                            y={t[1].y}
                            tile={t[1].tile}
                            size = {50}
                            interactive={t[1].interactive}
                            build={t[1].build}/>
                        break;
                    case 'Resource':
                        return <ResourceTileComponent
                            tileIndex={t[1].key}
                            x={t[1].x}
                            y={t[1].y}
                            tile={t[1].tile}
                            size = {50}
                            interactive={t[1].interactive}
                            onClick = {handleResourceClick}
                            />
                        break;
                    case 'ChildResource':
                        return <ResourceTileComponent
                            tileIndex={t[1].key}
                            x={t[1].x}
                            y={t[1].y}
                            tile={t[1].tile}
                            size = {50}
                            interactive={t[1].interactive}
                            onClick = {handleResourceClick}
                            />
                        break;
                    default:
                        return <></>
                }
            }
             )}
            {/* <KnightComponent x={knightPosition.x} y={knightPosition.y} size={50}/> */}
        </Container>
    )
} 

export { BoardComponent }
