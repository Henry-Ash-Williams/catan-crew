import { Container, Sprite, Text } from "@pixi/react";

export default function LeaderBoard(){
    return(
        <Container x={1000} y={470} width={50} height={500}>
            <Container>
            <Sprite image={'/assets/leaderboard-icons/card.png'} width={50} height={50}/>
            <Text text={'1'} x={60} y={10}/>
            </Container>
            <Container>
            <Sprite image={'/assets/leaderboard-icons/path.png'} width={50} height={50} y={80}/>
            <Text text={'1'} x={60} y={85}/>
            </Container>
            <Container>
            <Sprite image={'/assets/leaderboard-icons/player.png'} width={50} height={50} y={160}/>
            <Text text={'1'} x={60} y={170}/>
            </Container>
            <Container>
            <Sprite image={'/assets/leaderboard-icons/resource.png'} width={50} height={50} y={240}/>
            <Text text={'1'} x={60} y={245}/>
            </Container>
            <Container>
            <Sprite image={'/assets/leaderboard-icons/shield.png'} width={50} height={50} y={320}/>
            <Text text={'1'} x={60} y={325}/>
            </Container>
            <Container>
            <Sprite image={'/assets/leaderboard-icons/victory-points.png'} width={50} height={50} y={400}/>
            <Text text={'1'} x={60} y={405}/>
            </Container>
        </Container>
    )
}