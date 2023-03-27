import { Container } from "@pixi/react";
import { TileComponent } from './Tile';
import { PathComponent } from './Path';
import { IntersectionComponent } from "./Intersection";
import board from  "./new_board.json";

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
    owner?: number | null
    isCity?: boolean | undefined
    direction?: number | undefined
}

interface TileData {
    tile: Tile,
    x: number,
    y: number,
}
// interface Path {
//     location: number,
//     endpoints: Array<number>,
//     road: number | null
// }

// interface Intersection {
//     location: number,
//     settlement: number | null
// }

function initTiles(props: BoardComponentProps, tiles: Tile[]) {
    let x = props.width/2; // centre of board ( current position when initialising)
    let y = props.height/2;
    let ctx = 0; // position on board when initialising 
    let east = board.directions[0];
    let northEast = board.directions[1];
    let northWest = board.directions[2];
    let radius = 50;
    let radiusToFace = Math.sqrt(radius**2 - (radius/2)**2);
    let n = 1 + 3 * props.size * (props.size + 1); // number of tiles
    let tile_map = new Map();
    let tileDatas: TileData[] = [];

    // set first tile and move southeast
    tileDatas.push({tile: tiles[ctx], x: x, y: y});
    x += (radiusToFace*2);
    ctx += east; 
    
    for(let i = 1; i <= props.size; i++) {
        console.log(`RUN: ${i}/${props.size}`);
        for(let j = 0; j < i-1; j++){ // south
            console.log(`CTX: ${ctx} | X: ${x} Y: ${y} | South East`);
            tileDatas.push({tile: tiles[ctx], x: x, y: y});
            ctx = (n + ctx - northWest) % n;
            x += radiusToFace;
            y += radius*.8;
        }
        for(let j = 0; j < i; j++){ // southwest
            console.log(`CTX: ${ctx} | X: ${x} Y: ${y} | South West`);
            tileDatas.push({tile: tiles[ctx], x: x, y: y});
            ctx = (n + ctx - northEast) % n; 
            x -= radiusToFace;
            y += radius*.8;

        };
        for(let j = 0; j < i; j++){ // west
            console.log(`CTX: ${ctx} | X: ${x} Y: ${y} | West`);
            tileDatas.push({tile: tiles[ctx], x: x, y: y});
            ctx = (n + ctx - east) % n;
            x -= (radiusToFace*2);

        };
        for(let j = 0; j < i; j++){ // northwest
            console.log(`CTX: ${ctx} | X: ${x} Y: ${y} | North West`);
            tileDatas.push({tile: tiles[ctx], x: x, y: y});
            ctx = (n + ctx + northWest) % n;
            x -= radiusToFace;
            y -= radius*.8;
 
        };
        for(let j = 0; j < i; j++){ // northeast
            console.log(`CTX: ${ctx} | X: ${x} Y: ${y} | North East`);
            tileDatas.push({tile: tiles[ctx], x: x, y: y});
            ctx = (n + ctx + northEast) % n;
            x += radiusToFace;
            y -= radius*.8;
 
        };
        for(let j = 0; j < i+1; j++){ // east
            console.log(`CTX: ${ctx} | X: ${x} Y: ${y} | East`);
            tileDatas.push({tile: tiles[ctx], x: x, y: y});
            ctx = (n + ctx + east) % n;
            x += radiusToFace*2;

        };
    }

    tileDatas.sort(compare)

    for(let i = 0; i < tileDatas.length; i++){
        tile_map.set(
            tileDatas[i].tile.location, <TileComponent 
                key={tileDatas[i].tile.location} 
                x={tileDatas[i].x} 
                y={tileDatas[i].y} 
                width={radius} 
                height={radius} 
                t={tileDatas[i].tile}/>);
    }

    return tile_map
} 

function compare(a: TileData, b: TileData) {
    if (a.y === b.y) {
      return b.x - a.x;
    }
    return a.y - b.y;
  }

function BoardComponent(props: BoardComponentProps){
    let tiles: Tile[] = (board.tiles as Array<
                { type: string
                location: number
                resource?: string | undefined
                harbor?: boolean | null
                number_token?: number | undefined
                owner?: number | null | undefined
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

    let tileComponents = initTiles(props, tiles)

    return (
        <Container>
            {(Array.from(tileComponents.keys())).map((key) => (
                <>{tileComponents.get(key)}</>
             ))}
        </Container>
    )
} 

export { BoardComponent }
