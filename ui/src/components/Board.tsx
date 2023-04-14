import { Container } from "@pixi/react";
import board from  "./end_board.json";
import { IntersectionComponent } from "./Intersection";
import { PathComponent } from "./Path";
import { ResourceTileComponent } from "./Resource";
import { KnightComponent } from "./knight";
import { useState } from "react";

interface BoardComponentProps {
    height: number,
    width: number,
    size: number
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
    x: number,
    y: number,
}

interface Coordinates {
    x: number,
    y: number
}


function initTiles(props: BoardComponentProps, handleClick: (coordinates: Coordinates) => void) {
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
    console.log(tiles.length)

    // x and y values for center tile
    let x0 = props.width/2;
    let y0 = -50 + props.height/2;

    let east = board.directions[0];
    let northEast = board.directions[1];

    let radius = 50;
    let radiusToFace = (radius * Math.sqrt(3) / 2)*1.05; // Better way to calculate radiusToFace

    let n = tiles.length; // number of tiles

    let tile_map = new Map();
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
            tileDatas.set(ctx, {tile: tiles[ctx], x: x, y: y});
        }
    }

    console.log(tileDatas)
    tileDatas.forEach(function(value, key) {
        if (value.tile.type == "Resource") {
            for (let i = 0; i < 6; i++) {
                console.log((n + key + board.directions[i]) % n)
                // if the index for the child node can't be found in tileDatas, skip it
                if(!tileDatas.has((n + key + board.directions[i]) % n)){continue;}
                var temp = tileDatas.get((n + key + board.directions[i]) % n)!
                console.log(temp)
                temp.tile.type = "ChildResource"
                temp.tile.resource = value.tile.resource
            }
        }
    })

    let knight = {x: x0, y: y0}
    tileDatas.forEach(function(value, key) {
        if(value.tile.type == "Intersection") {
            tile_map.set(key, <IntersectionComponent
                key={key.toString()}
                x={value.x}
                y={value.y}
                size={radius}
                direction={value.tile.direction? value.tile.direction : undefined}
                owner={value.tile.owner}
                isCity={value.tile.isCity}
                />)
        } else if(value.tile.type == "PathTile") {
            tile_map.set(key, <PathComponent
                key={key}
                x={value.x}
                y={value.y}
                size={radius}
                direction={value.tile.direction}
                text={key.toString()}
                onClick={handleClick}
                owner={value.tile.owner}
                />)
        } else if(value.tile.type == "Resource") {
            tile_map.set(key, <ResourceTileComponent
                key={key}
                x={value.x}
                y={value.y}
                size={radius}
                number_token={value.tile.number_token}
                resource={value.tile.resource}
                onClick={handleClick}
                />)
            if(value.tile.resource == "desert") {
                knight = {x: value.x, y: value.y}
            }
        } else if(value.tile.type == "ChildResource") {
            tile_map.set(key, <ResourceTileComponent
                key={key}
                x={value.x}
                y={value.y}
                size={radius}
                resource={value.tile.resource}
                onClick={handleClick}
                />)
        }
    })

    return {tiles: tile_map, knight}
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
        let boardInit = initTiles(props, handleResourceClick)
        return boardInit
    }
    const handleResourceClick = (coordinates: Coordinates) => {
        console.log(coordinates)
        setKnightPosition(coordinates)
    }

    const [boardState, setBoardState] = useState<{ tiles: Map<Number, JSX.Element>, knight: Coordinates }>(initBoard)
    const [knightPosition, setKnightPosition] = useState<Coordinates>(boardState.knight)

    return (
        <Container>
            {(Array.from(boardState.tiles.keys())).map((key) => (
                <>{boardState.tiles.get(key)}</>
             ))}
            <KnightComponent x={knightPosition.x} y={knightPosition.y} size={50}/>
        </Container>
    )
} 

export { BoardComponent }
