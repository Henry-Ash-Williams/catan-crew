import './styles/App.css';
import { BoardComponent } from './components/Board';
import { Container, Graphics, Sprite, Stage, useApp, useTick, InteractionEvents } from '@pixi/react';
import { Texture } from 'pixi.js';
import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import Menu from './components/Menu';
import Card from './components/Card';
import LeaderBoard from './components/LeaderBoard';
import ActionsBar from './components/ActionsBar';
import { DiceComponent } from './components/Dice';

function App() {

  const [menuActive, setMenuActive] = useState<boolean>(true)
  const cardContainer = useRef(null);
  const [canRoll, setCanRoll] = useState(true);
  const [numbersToDisplay, setNumbersToDisplay] = useState<[number, number]>([6, 6]);
  const [dimensions, setDimensions] = useState({
    height: 9 * Math.min(window.innerHeight / 9, window.innerWidth / 16),
    width: 16 * Math.min(window.innerHeight / 9, window.innerWidth / 16)
  })
  // const [boardPosition, setBoardPosition] = useState({ x: 0, y:0});
    
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
      <Sprite width={dimensions.width} height={dimensions.height} texture={Texture.WHITE} tint={0x00FFFF}></Sprite>

      {/* Board */}
      <BoardComponent size={13} width={dimensions.width} height={dimensions.height}/>
        {/* Cards */}
      <Container>
        <Card resourceType='ore' width={dimensions.width} height={dimensions.height} y={dimensions.height * 0} amount={5}/>
        <Card resourceType='wool' width={dimensions.width} height={dimensions.height} y={dimensions.height * 0.16} amount={4}/>
        <Card resourceType='lumber' width={dimensions.width} height={dimensions.height} y={dimensions.height * 0.32} amount={6}/>
        <Card resourceType='grain' width={dimensions.width} height={dimensions.height} y={dimensions.height * 0.48} amount={3}/>
        <Card resourceType='brick' width={dimensions.width} height={dimensions.height} y={dimensions.height * 0.64} amount={2}/>
      </Container>

      <LeaderBoard width={dimensions.width} height={dimensions.height}/>

      <DiceComponent canRoll={canRoll} numbersToDisplay={numbersToDisplay} setNumbersToDisplay={setNumbersToDisplay} x={dimensions.width*0.735} y={dimensions.height*0.86}/>

      <ActionsBar width={dimensions.width} height={dimensions.height}/>

    </Stage>
    </div>
}
    </>
  );
}

export default App;
