import { Container } from "@pixi/react";
import board from  "./new_board.json";
import { IntersectionComponent } from "./Intersection";
import { PathComponent } from "./Path";
import { ResourceTileComponent } from "./Resource";

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
    owner?: number | undefined
    isCity?: boolean | undefined
    direction?: number | undefined
}

interface TileData {
    tile: Tile,
    x: number,
    y: number,
}


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
    let tileDatas: Map<number, TileData> = new Map();

    // set first tile and move southeast
    tileDatas.set(ctx, {tile: tiles[ctx], x: x, y: y});
    x += (radiusToFace*2);
    ctx += east; 
    
    
    for(let i = 1; i <= props.size; i++) {
        console.log(`RUN: ${i}/${props.size}`);
        for(let j = 0; j < i-1; j++){ // south
            console.log(`CTX: ${ctx} | X: ${x} Y: ${y} | South East`);
            tileDatas.set(ctx, {tile: tiles[ctx], x: x, y: y});
            ctx = (n + ctx - northWest) % n;
            x += radiusToFace;
            y += radius*.8;
        }
        for(let j = 0; j < i; j++){ // southwest
            console.log(`CTX: ${ctx} | X: ${x} Y: ${y} | South West`);
            tileDatas.set(ctx, {tile: tiles[ctx], x: x, y: y});
            ctx = (n + ctx - northEast) % n; 
            x -= radiusToFace;
            y += radius*.8;

        };
        for(let j = 0; j < i; j++){ // west
            console.log(`CTX: ${ctx} | X: ${x} Y: ${y} | West`);
            tileDatas.set(ctx, {tile: tiles[ctx], x: x, y: y});
            ctx = (n + ctx - east) % n;
            x -= (radiusToFace*2);

        };
        for(let j = 0; j < i; j++){ // northwest
            console.log(`CTX: ${ctx} | X: ${x} Y: ${y} | North West`);
            tileDatas.set(ctx, {tile: tiles[ctx], x: x, y: y});
            ctx = (n + ctx + northWest) % n;
            x -= radiusToFace;
            y -= radius*.8;
 
        };
        for(let j = 0; j < i; j++){ // northeast
            console.log(`CTX: ${ctx} | X: ${x} Y: ${y} | North East`);
            tileDatas.set(ctx, {tile: tiles[ctx], x: x, y: y});
            ctx = (n + ctx + northEast) % n;
            x += radiusToFace;
            y -= radius*.8;
 
        };
        for(let j = 0; j < i+1; j++){ // east
            console.log(`CTX: ${ctx} | X: ${x} Y: ${y} | East`);
            tileDatas.set(ctx, {tile: tiles[ctx], x: x, y: y});
            ctx = (n + ctx + east) % n;
            x += radiusToFace*2;

        };
    }

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

    tileDatas.forEach(function(value, key) {
        if(value.tile.type == "Intersection") {
            tile_map.set(key, <IntersectionComponent
                key={key}
                x={value.x}
                y={value.y}
                size={radius*4}
                />)
        } else if(value.tile.type == "PathTile") {
            tile_map.set(key, <PathComponent
                key={key}
                x={value.x}
                y={value.y}
                size={radius*4}
                direction={value.tile.direction}
                />)
        } else if(value.tile.type == "Resource") {
            tile_map.set(key, <ResourceTileComponent
                key={key}
                x={value.x}
                y={value.y}
                size={radius*4}
                number_token={value.tile.number_token}
                resource={value.tile.resource}
                />)
        } else if(value.tile.type == "ChildResource") {
            tile_map.set(key, <ResourceTileComponent
                key={key}
                x={value.x}
                y={value.y}
                size={radius*4}
                resource={value.tile.resource}
                />)
        }
    })
    return tile_map
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

// function compare(a: TileData, b: TileData) {
//     if (a.y === b.y) {
//       return b.x - a.x;
//     }
//     return a.y - b.y;
//   }

function BoardComponent(props: BoardComponentProps){
    let tiles: Tile[] = (board.tiles as Array<
                { type: string
                location: number
                resource?: string | undefined
                harbor?: boolean | null
                number_token?: number | undefined
                owner?: number | undefined
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
