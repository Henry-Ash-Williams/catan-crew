import { Container } from "@pixi/react";
import { Tile } from './Tile';

interface props {
    size: number,
    width: number,
    height: number,
}

function Board(props: props) {


    console.log(`${props.width}   ${props.height}`)
    let size = props.size;
    let x = props.width/2;
    let y = props.height/2;
    let radius = 50;
    let radiusToFace = Math.sqrt(radius**2 - (radius/2)**2);
    let northEast = 11;
    let northWest = 10;
    let east = 1;
    let ctx = 0;
    let n = 1 + 3 * size * (size + 1);
    let tile_map = new Map();
    console.log(`CTX: ${ctx} | X: ${x} Y: ${y}`)
    tile_map.set(ctx, <Tile x={x} y={y} radius={radius} tileID={ctx} />);
    x += (radiusToFace*2);
    ctx += east; 
    console.log(`n: ${n} | size: ${size}`);
    let side = 3;

    for(let i = 1; i <= side; i++) {
        console.log(`RUN: ${i}/${side}`);
        for(let j = 0; j < i-1; j++){ // southeast
            console.log(`CTX: ${ctx} | X: ${x} Y: ${y} | South East`);
            tile_map.set(ctx, <Tile x={x} y={y} tileID={ctx} radius={radius}/>);
            ctx = (n + ctx - northWest) % n;
            x += radiusToFace;
            y += radius*1.5;
        }
        for(let j = 0; j < i; j++){ // southwest
            console.log(`CTX: ${ctx} | X: ${x} Y: ${y} | South West`);
            tile_map.set(ctx, <Tile x={x} y={y} tileID={ctx}  radius={radius}/>);
            ctx = (n + ctx - northEast) % n; 
            x -= radiusToFace;
            y += radius*1.5;

        };
        for(let j = 0; j < i; j++){ // west
            console.log(`CTX: ${ctx} | X: ${x} Y: ${y} | West`);
            tile_map.set(ctx, <Tile x={x} y={y} tileID={ctx}  radius={radius}/>);
            ctx = (n + ctx - east) % n;
            //console.log((n + ctx - east) % n);
            x -= (radiusToFace*2);

        };
        for(let j = 0; j < i; j++){ // northwest
            console.log(`CTX: ${ctx} | X: ${x} Y: ${y} | North West`);
            tile_map.set(ctx, <Tile x={x} y={y} tileID={ctx}  radius={radius}/>);
            ctx = (n + ctx + northWest) % n;
            x -= radiusToFace;
            y -= radius*1.5
 
        };
        for(let j = 0; j < i; j++){ // northeast
            console.log(`CTX: ${ctx} | X: ${x} Y: ${y} | North East`);
            tile_map.set(ctx, <Tile x={x} y={y} tileID={ctx}  radius={radius}/>);
            ctx = (n + ctx + northEast) % n;
            x += radiusToFace;
            y -= radius*1.5;
 
        };
        for(let j = 0; j < i+1; j++){ // east
            console.log(`CTX: ${ctx} | X: ${x} Y: ${y} | East`);
            tile_map.set(ctx, <Tile x={x} y={y} tileID={ctx}  radius={radius}/>);
            ctx = (n + ctx + east) % n;
            x += radiusToFace*2;

        };
    }

    const keys = Array.from(tile_map.keys());
    console.log(keys);
    console.log("YEET");
    console.log(tile_map);
    return (
    
      <Container x={0} y={0} width={props.width} height={props.height}>
        {keys.map((key) => (
            <>{tile_map.get(key)}</>
        ))}

      </Container>
    
    )
}

export { Board };