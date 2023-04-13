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

    let x = props.width/2; // centre of board ( current position when initialising)
    let y = -50 + props.height/2;
    let ctx = 0; // position on board when initialising 
    let east = board.directions[0];
    let northEast = board.directions[1];
    let northWest = board.directions[2];
    let radius = 50;
    let radiusToFace = Math.sqrt(radius**2 - (radius/2)**2);
    let n = tiles.length; // number of tiles
    let tile_map = new Map();
    let tileDatas: Map<number, TileData> = new Map();

    // set first tile and move southeast
    tileDatas.set(ctx, {tile: tiles[ctx], x: x, y: y});
    x += (radiusToFace);
    ctx += east; 
    
    
    for(let i = 1; i <= props.size; i++) {
        console.log(`RUN: ${i}/${props.size}`);
        for(let j = 0; j < i-1; j++){ // south
            console.log(`CTX: ${ctx} | X: ${x} Y: ${y} | South East`);
            tileDatas.set(ctx, {tile: tiles[ctx], x: x, y: y});
            ctx = (n + ctx - northWest) % n;
            x += radiusToFace/2;
            y += radius/2.4;
        }
        for(let j = 0; j < i; j++){ // southwest
            console.log(`CTX: ${ctx} | X: ${x} Y: ${y} | South West`);
            tileDatas.set(ctx, {tile: tiles[ctx], x: x, y: y});
            ctx = (n + ctx - northEast) % n; 
            x -= radiusToFace/2;
            y += radius/2.4;

        };
        for(let j = 0; j < i; j++){ // west
            console.log(`CTX: ${ctx} | X: ${x} Y: ${y} | West`);
            tileDatas.set(ctx, {tile: tiles[ctx], x: x, y: y});
            ctx = (n + ctx - east) % n;
            x -= (radiusToFace);

        };
        for(let j = 0; j < i; j++){ // northwest
            console.log(`CTX: ${ctx} | X: ${x} Y: ${y} | North West`);
            tileDatas.set(ctx, {tile: tiles[ctx], x: x, y: y});
            ctx = (n + ctx + northWest) % n;
            x -= radiusToFace/2;
            y -= radius/2.4;
 
        };
        for(let j = 0; j < i; j++){ // northeast
            console.log(`CTX: ${ctx} | X: ${x} Y: ${y} | North East`);
            tileDatas.set(ctx, {tile: tiles[ctx], x: x, y: y});
            ctx = (n + ctx + northEast) % n;
            x += radiusToFace/2;
            y -= radius/2.4;
 
        };
        for(let j = 0; j < i+1; j++){ // east
            console.log(`CTX: ${ctx} | X: ${x} Y: ${y} | East`);
            tileDatas.set(ctx, {tile: tiles[ctx], x: x, y: y});
            ctx = (n + ctx + east) % n;
            x += radiusToFace;

        };
    }

    console.log(tileDatas)
    tileDatas.forEach(function(value, key) {
        if (value.tile.type == "Resource") {
            for (let i = 0; i < 6; i++) {
                console.log((n + key + board.directions[i]) % n)
                var temp = tileDatas.get((n + key + board.directions[i]) % n)!
                console.log(temp)
                temp.tile.type = "ChildResource"
                temp.tile.resource = value.tile.resource
            }
        }
    })

    tileDatas = sortMap(tileDatas)
    let knight = {x, y}
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
