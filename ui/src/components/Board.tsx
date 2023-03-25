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
    width: number,
    height: number
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
    tile_map.set(ctx, <TileComponent key={ctx} x={x} y={y} width={radius} height={radius} t={tiles[ctx]} />);
    tileDatas.push({tile: tiles[ctx], x: x, y: y, width: radius, height: radius})
    x += (radiusToFace*2);
    ctx += east; 
    for(let i = 1; i <= props.size; i++) {
        console.log(`RUN: ${i}/${props.size}`);
        for(let j = 0; j < i-1; j++){ // south
            console.log(`CTX: ${ctx} | X: ${x} Y: ${y} | South East`);
            tile_map.set(ctx, <TileComponent key={ctx} x={x} y={y}  width={radius} height={radius} t={tiles[ctx]}/>);
            ctx = (n + ctx - northWest) % n;
            x += radiusToFace;
            y += radius;
        }
        for(let j = 0; j < i; j++){ // southwest
            console.log(`CTX: ${ctx} | X: ${x} Y: ${y} | South West`);
            tile_map.set(ctx, <TileComponent key={ctx} x={x} y={y} width={radius} height={radius} t={tiles[ctx]}/>);
            ctx = (n + ctx - northEast) % n; 
            x -= radiusToFace;
            y += radius;

        };
        for(let j = 0; j < i; j++){ // west
            console.log(`CTX: ${ctx} | X: ${x} Y: ${y} | West`);
            tile_map.set(ctx, <TileComponent key={ctx} x={x} y={y}  width={radius} height={radius} t={tiles[ctx]}/>);
            ctx = (n + ctx - east) % n;
            //console.log((n + ctx - east) % n);
            x -= (radiusToFace*2);

        };
        for(let j = 0; j < i; j++){ // northwest
            console.log(`CTX: ${ctx} | X: ${x} Y: ${y} | North West`);
            tile_map.set(ctx, <TileComponent key={ctx} x={x} y={y}  width={radius} height={radius} t={tiles[ctx]}/>);
            ctx = (n + ctx + northWest) % n;
            x -= radiusToFace;
            y -= radius;
 
        };
        for(let j = 0; j < i; j++){ // northeast
            console.log(`CTX: ${ctx} | X: ${x} Y: ${y} | North East`);
            tile_map.set(ctx, <TileComponent key={ctx} x={x} y={y}  width={radius} height={radius} t={tiles[ctx]}/>);
            ctx = (n + ctx + northEast) % n;
            x += radiusToFace;
            y -= radius;
 
        };
        for(let j = 0; j < i+1; j++){ // east
            console.log(`CTX: ${ctx} | X: ${x} Y: ${y} | East`);
            tile_map.set(ctx, <TileComponent key={ctx} x={x} y={y}  width={radius} height={radius} t={tiles[ctx]}/>);
            ctx = (n + ctx + east) % n;
            x += radiusToFace*2;

        };
    }
    
    return tile_map
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

    // let intersections: Intersection[] = board.intersections.map(intersection => {
    //     return {
    //         location: intersection.location,
    //         settlement: intersection.settlement
    //     }
    // })

    // let paths: Path[] = board.paths.map(path => {
    //     return {
    //         location: path.location,
    //         endpoints: path.endpoints,
    //         road: path.road
    //     }
    // })

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


// type BoardObject = {
//     "size": number,
//     "directions": Array<number>,
//     "tiles": Array<TileComponentObject>

// }

// interface props {
//     board: object,
//     size: number,
//     width: number,
//     height: number,
// }

// function Board(props: props) {

//     console.log(`${props.width}   ${props.height}`)
//     let size = props.size;
//     let x = props.width/2;
//     let y = props.height/2;
//     let radius = 50;
//     let radiusToFace = Math.sqrt(radius**2 - (radius/2)**2);
//     let northEast = 11;
//     let northWest = 10;
//     let east = 1;
//     let ctx = 0;
//     let n = 1 + 3 * size * (size + 1);
//     let tile_map = new Map();
//     console.log(`CTX: ${ctx} | X: ${x} Y: ${y}`)
//     tile_map.set(ctx, <TileComponent> key={ctx} x={x} y={y} width={radius} height={radius} t={props.board.tiles[ctx]} />);
//     x += (radiusToFace*2);
//     ctx += east; 
//     console.log(`n: ${n} | size: ${size}`);
//     let side = 3;

//     for(let i = 1; i <= side; i++) {
//         console.log(`RUN: ${i}/${side}`);
//         for(let j = 0; j < i-1; j++){ // southeast
//             console.log(`CTX: ${ctx} | X: ${x} Y: ${y} | South East`);
//             tile_map.set(ctx, <TileComponent> key={ctx} x={x} y={y}  width={radius} height={radius} t={props.board.tiles[ctx]}/>);
//             ctx = (n + ctx - northWest) % n;
//             x += radiusToFace;
//             y += radius*1.5;
//         }
//         for(let j = 0; j < i; j++){ // southwest
//             console.log(`CTX: ${ctx} | X: ${x} Y: ${y} | South West`);
//             tile_map.set(ctx, <TileComponent> key={ctx} x={x} y={y} width={radius} height={radius} t={props.board.tiles[ctx]}/>);
//             ctx = (n + ctx - northEast) % n; 
//             x -= radiusToFace;
//             y += radius*1.5;

//         };
//         for(let j = 0; j < i; j++){ // west
//             console.log(`CTX: ${ctx} | X: ${x} Y: ${y} | West`);
//             tile_map.set(ctx, <TileComponent> key={ctx} x={x} y={y}  width={radius} height={radius} t={props.board.tiles[ctx]}/>);
//             ctx = (n + ctx - east) % n;
//             //console.log((n + ctx - east) % n);
//             x -= (radiusToFace*2);

//         };
//         for(let j = 0; j < i; j++){ // northwest
//             console.log(`CTX: ${ctx} | X: ${x} Y: ${y} | North West`);
//             tile_map.set(ctx, <TileComponent> key={ctx} x={x} y={y}  width={radius} height={radius} t={props.board.tiles[ctx]}/>);
//             ctx = (n + ctx + northWest) % n;
//             x -= radiusToFace;
//             y -= radius*1.5
 
//         };
//         for(let j = 0; j < i; j++){ // northeast
//             console.log(`CTX: ${ctx} | X: ${x} Y: ${y} | North East`);
//             tile_map.set(ctx, <TileComponent> key={ctx} x={x} y={y}  width={radius} height={radius} t={props.board.tiles[ctx]}/>);
//             ctx = (n + ctx + northEast) % n;
//             x += radiusToFace;
//             y -= radius*1.5;
 
//         };
//         for(let j = 0; j < i+1; j++){ // east
//             console.log(`CTX: ${ctx} | X: ${x} Y: ${y} | East`);
//             tile_map.set(ctx, <TileComponent> key={ctx} x={x} y={y}  width={radius} height={radius} t={props.board.tiles[ctx]}/>);
//             ctx = (n + ctx + east) % n;
//             x += radiusToFace*2;

//         };
//     }

//     const keys = Array.from(tile_map.keys());
//     console.log(keys);
//     console.log("YEET");
//     console.log(tile_map);
//     return (
    
//       <Container x={0} y={0} width={props.width} height={props.height}>
//         {keys.map((key) => (
//             <>{tile_map.get(key)}</>
//         ))}

//       </Container>
    
//     )
// }

// export { Board };