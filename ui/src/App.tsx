import './styles/App.css';
import { BoardComponent } from './components/Board';
import { Container, Graphics, Sprite, Stage, useApp, useTick } from '@pixi/react';
import { Texture } from 'pixi.js';
import { UiComponent } from './components/Ui';
import { useCallback, useRef, useState } from 'react';
import Menu from './components/Menu';
import Card from './components/Card';
import LeaderBoard from './components/LeaderBoard';



function App() {

  const [menuActive, setMenuActive] = useState<boolean>(true)
  const cardContainer = useRef(null);
  const draw = useCallback((g:any)=> {
    g.clear();
    g.lineStyle(2, 'red');
    g.drawRect(0, 0, 1300, 1000);
  }, [])

  // function handleRef(){
  //   cardContainer.current.addChild()
  // }


  return (
    <>
    {menuActive ? <Menu onShow={() => setMenuActive(!menuActive)}/>
    :
    <Stage width={1300} height={1000}>
      <Sprite width={1300} height={1000} texture={Texture.WHITE} ></Sprite>
      <BoardComponent size={3} width={1000} height={1000}/>
      <Container ref={cardContainer} interactive={true} x={30} y={0}>
        <Card resourceType='ore' xPos={0} yPos={50} amount={1}/>
        <Card resourceType='wool' xPos={0} yPos={200} amount={1}/>
        <Card resourceType='lumber' xPos={0} yPos={350} amount={1}/>
        <Card resourceType='grain' xPos={0} yPos={500} amount={1}/>
        <Card resourceType='brick' xPos={0} yPos={650} amount={1}/>
      </Container>
      <LeaderBoard/>
      <Graphics draw={draw}/>
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
