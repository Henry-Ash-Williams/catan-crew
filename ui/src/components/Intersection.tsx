import { Container, Sprite } from '@pixi/react';

interface IntersectionComponentProps {
    location: number,
    settlement: number | null
}

function IntersectionComponent(props: IntersectionComponentProps) {


    return (
        <Container>
            <Sprite>
                
            </Sprite>
        </Container>
    )
}

export { IntersectionComponent }