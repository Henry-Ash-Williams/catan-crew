import './styles/App.css';
import { BoardComponent } from './components/Board';
import { Container, Graphics, Sprite, Stage, useApp, useTick } from '@pixi/react';
import { Texture } from 'pixi.js';
import { UiComponent } from './components/Ui';
import { useCallback, useRef, useState } from 'react';
import Menu from './components/Menu';
import Card from './components/Card';
import LeaderBoard from './components/LeaderBoard';
import { IntersectionComponent } from './components/Intersection';
import { PathComponent } from './components/Path';
import { ResourceTileComponent } from './components/Resource';
import { KnightComponent } from './components/knight';
import { DiceComponent } from './components/Dice';

function App() {

  const [menuActive, setMenuActive] = useState<boolean>(true)
  const cardContainer = useRef(null);
  const [canRoll, setCanRoll] = useState(false);
  const [numbersToDisplay, setNumbersToDisplay] = useState<[number, number]>([6, 6]);
  // function handleRef(){
  //   cardContainer.current.addChild()
  // }


  return (
    <>
    {menuActive ? <Menu onShow={() => setMenuActive(!menuActive)}/>
    :
    <Stage width={1000} height={1000}>
      <Sprite width={2000} height={1000} texture={Texture.WHITE} ></Sprite>
      <BoardComponent size={3} width={1000} height={1000}/>
      <DiceComponent canRoll={canRoll} numbersToDisplay={numbersToDisplay} setNumbersToDisplay={setNumbersToDisplay} x={100} y={100}/>
      {/* <Container ref={cardContainer} interactive={true} onclick={()=>{handleRef()}}>
        <Card resourceType='ore' xPos={25} yPos={50}/>
        <Card resourceType='wool' xPos={145} yPos={50}/>
        <Card resourceType='lumber' xPos={265} yPos={50}/>
        <Card resourceType='grain' xPos={385} yPos={50}/>
        <Card resourceType='brick' xPos={505} yPos={50}/>
      </Container> */}
      {/* <UiComponent></UiComponent> */}

      {/* <KnightComponent x={100} y={100} size={50}/> */}


      {/* <IntersectionComponent x={100} y={100} isCity={false} size={200}/>
      <IntersectionComponent x={300} y={200} owner={0xFF22AB} size={200} isCity={false}/>
      <IntersectionComponent x={500} y={300} owner={0xAB22FF} size={200} isCity={true}/>
      <PathComponent x={200} y={400} direction={1} size={200}/>
      <PathComponent x={300} y={500} direction={1} owner={0xAB22FF} size={200}/>
      <PathComponent x={500} y={600} direction={1} owner={0xFF22AB} size={200}/>
      <ResourceTileComponent x={700} y={200} number_token={2} resource={"brick"} size={200}/>
      <ResourceTileComponent x={900} y={200} number_token={3} resource={"grain"} size={200}/>
      <ResourceTileComponent x={1200} y={300} number_token={4} resource={"ore"} size={200}/>
      <ResourceTileComponent x={700} y={300} number_token={5} resource={"wool"} size={200}/>
      <ResourceTileComponent x={900} y={400} number_token={6} resource={"lumber"} size={200}/>
      <ResourceTileComponent x={1200} y={500} size={200}/> */}
    </Stage>
}
    </>
  );
}

export default App;
