import { Container, PixiRef, Sprite } from "@pixi/react"
import { useState, useRef, useEffect } from "react"
import { gsap } from "gsap"

interface KnightComponentProps {
    x: number
    y: number
    size: number
}

function KnightComponent(props: KnightComponentProps) {
    const containerRef = useRef<PixiRef<typeof Container>>(null);

    useEffect(() => {
        if (containerRef.current) {
            gsap.to(containerRef.current, {
                x: props.x - 15,
                y: props.y + 10,
                duration: 0.5
            })
        }
    }, [props.x, props.y])
    return(
    <Container ref={containerRef} x={props.x} y={props.y}>
        <Sprite width={props.size/2} height={props.size/2} anchor={0.5} image={"../assets/board/knight.png"}/>
    </Container>)
}

export {KnightComponent}