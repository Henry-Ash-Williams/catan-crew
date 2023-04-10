import './styles/App.css';
import { BoardComponent } from './components/Board';
import { Container, Graphics, Sprite, Stage, useApp, useTick } from '@pixi/react';
import { Texture } from 'pixi.js';
import { UiComponent } from './components/Ui';
import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import Menu from './components/Menu';
import Card from './components/Card';
import LeaderBoard from './components/LeaderBoard';
import { IntersectionComponent } from './components/Intersection';
import { PathComponent } from './components/Path';
import { ResourceTileComponent } from './components/Resource';
import { KnightComponent } from './components/knight';
import ActionsBar from './components/ActionsBar';
import PlayerInfo from './components/PlayerInfo';
import { DiceComponent } from './components/Dice';

function App() {

  const [menuActive, setMenuActive] = useState<boolean>(true)
  const cardContainer = useRef(null);
  const [canRoll, setCanRoll] = useState(true);
  const [numbersToDisplay, setNumbersToDisplay] = useState<[number, number]>([6, 6]);
  const [dimensions, setDimensions] = useState({
    height: 9 * Math.min(window.innerHeight / 9, window.innerWidth / 16),
    width: 16 * Math.min(window.innerHeight / 9, window.innerWidth / 16)
  }
    )
  useEffect(()=>{
    function handleResize(){
      setDimensions({
        width: 16 * Math.min(window.innerHeight / 9, window.innerWidth / 16),
        height: 9 * Math.min(window.innerHeight / 9, window.innerWidth / 16),
      })
    }
   window.addEventListener('resize', handleResize) 
   return () => {
    window.removeEventListener('resize', handleResize)
   }
  })

  return (
    <>
    {menuActive ? <Menu onShow={() => setMenuActive(!menuActive)}/>
    :
    <div style={{display: "flex", height: "100vh", justifyContent: "center", alignItems: "center"}}>
    <Stage width={dimensions.width} height={dimensions.height}>
        {/* Background */}
      {/* 
      */}
      {/* 
      <Sprite width={dimensions.width} height={dimensions.height} texture={Texture.WHITE} ></Sprite>
        Board
      */}
      <BoardComponent size={3} width={dimensions.width} height={dimensions.height}/>
      {/* 
      */}
        {/* Cards */}
      <Container>
        <Card resourceType='ore' width={dimensions.width} height={dimensions.height} y={dimensions.height * 0} amount={5}/>
        <Card resourceType='wool' width={dimensions.width} height={dimensions.height} y={dimensions.height * 0.16} amount={4}/>
        <Card resourceType='lumber' width={dimensions.width} height={dimensions.height} y={dimensions.height * 0.32} amount={6}/>
        <Card resourceType='grain' width={dimensions.width} height={dimensions.height} y={dimensions.height * 0.48} amount={3}/>
        <Card resourceType='brick' width={dimensions.width} height={dimensions.height} y={dimensions.height * 0.64} amount={2}/>
      </Container>
      {/* 
        Leaderboard
      */}
      <LeaderBoard width={dimensions.width} height={dimensions.height}/>
      {/* 
        Player
      */}
      {/* <PlayerInfo score={0} fontSize={"4.5em"} width={dimensions.width * 1/13} height={dimensions.height * 0.13} y={dimensions.height * 0.80} x={dimensions.width * 0.75}/> */}
      {/* 
        Action bar
      */}
      <ActionsBar width={dimensions.width} height={dimensions.height}/>

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
    </div>
}
    </>
  );
}

export default App;
