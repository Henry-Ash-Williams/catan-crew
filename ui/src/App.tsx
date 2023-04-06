import './styles/App.css';
import { BoardComponent } from './components/Board';
import { Container, Sprite, Stage, useApp } from '@pixi/react';
import { Texture } from 'pixi.js';
import { UiComponent } from './components/Ui';
import { useRef, useState } from 'react';
import Menu from './components/Menu';
import Card from './components/Card';



function App() {

  const [menuActive, setMenuActive] = useState<boolean>(true)
  const cardContainer = useRef(null);

  function handleRef(){
    cardContainer.current.addChild()
  }

  return (
    <>
    {menuActive ? <Menu onShow={() => setMenuActive(!menuActive)}/>
    :
    <Stage width={1000} height={1000}>
      <Sprite width={2000} height={1000} texture={Texture.WHITE} ></Sprite>
      <BoardComponent size={3} width={1000} height={1000}/>
      <Container ref={cardContainer} interactive={true} onclick={()=>{handleRef()}}>
        <Card resourceType='ore' xPos={25} yPos={50}/>
        <Card resourceType='wool' xPos={145} yPos={50}/>
        <Card resourceType='lumber' xPos={265} yPos={50}/>
        <Card resourceType='grain' xPos={385} yPos={50}/>
        <Card resourceType='brick' xPos={505} yPos={50}/>
      </Container>
      {/* <UiComponent></UiComponent> */}


      {/* <IntersectionComponent x={100} y={100} isCity={false}/>
      <IntersectionComponent x={300} y={200} owner={0xFF22AB} isCity={false}/>
      <IntersectionComponent x={500} y={300} owner={0xAB22FF} isCity={true}/>
      <PathComponent x={100} y={400} direction={1}/>
      <PathComponent x={300} y={500} direction={1} owner={0xAB22FF}/>
      <PathComponent x={500} y={600} direction={1} owner={0xFF22AB}/>
      <ResourceTileComponent x={700} y={100} number_token={2} resource={"brick"}/>
      <ResourceTileComponent x={900} y={200} number_token={3} resource={"grain"}/>
      <ResourceTileComponent x={1100} y={300} number_token={4} resource={"ore"}/>
      <ResourceTileComponent x={700} y={300} number_token={5} resource={"wool"}/>
      <ResourceTileComponent x={900} y={400} number_token={6} resource={"lumber"}/>
      <ResourceTileComponent x={1100} y={500}/> */}
    </Stage>
}
    </>
  );
}

export default App;
