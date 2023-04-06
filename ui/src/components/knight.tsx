import { Container, Sprite } from "@pixi/react"
import { useState } from "react"

interface KnightComponentProps {
    x: number
    y: number
    size: number
}

function KnightComponent(props: KnightComponentProps) {
    return(
    <Container x={props.x} y={props.y + 30}>
        <Sprite width={props.size} height={props.size} anchor={0.5} image={"../assets/board/knight.png"}/>
    </Container>)
}

export {KnightComponent}