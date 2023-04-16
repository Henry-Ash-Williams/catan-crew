import './styles/App.css';

import { io, Socket } from 'socket.io-client';
import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { Container, Graphics, Sprite, Stage, useApp, useTick, InteractionEvents } from '@pixi/react';
import { Texture } from 'pixi.js';

import Menu from './components/Menu';
import Card from './components/Card';
import LeaderBoard from './components/LeaderBoard';
import ActionsBar from './components/ActionsBar';
import { DiceComponent } from './components/Dice';
import { BoardComponent } from './components/Board';
import { LobbyComponent } from './components/Lobby';
import Bank from './components/Bank';

function App() {
  const [menuActive, setMenuActive] = useState<boolean>(true)
  
  const [players, setPlayers] = useState<string[]>([])
  const [hasJoined, setHasJoined] = useState(false);
  const [socket, setSocket] = useState<Socket | null>(null)
  
  const handleJoinGame = () => {
    const newSocket = io('http://localhost:3001');
    setSocket(newSocket)
    socket?.emit("join_room")
    setHasJoined(true);
    
  }

  useEffect(() => {
    // just a listener
    socket?.on("join_room", data => {
      setPlayers(players + data)
      console.log("PLAYERS:", players)
    })

    return () => {
      socket?.off("join_room")
    }
  })
  
  const handleStartGame = () => {
      console.log('Starting the game...')
    }
  const cardContainer = useRef(null);
  const [canRoll, setCanRoll] = useState(false);
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

    {/* {!hasJoined ? 
      <Menu onShow={handleJoinGame}/>
    : <LobbyComponent players={players} onStartGame={handleStartGame}/>} */}
    <div style={{display: "flex", height: "100vh", justifyContent: "center", alignItems: "center"}}>
    <Stage width={dimensions.width} height={dimensions.height}>
        {/* Background */}
      <Sprite width={dimensions.width} height={dimensions.height} texture={Texture.WHITE} tint={0x00FFFF}></Sprite>

      {/* Board */}
      <BoardComponent size={15} width={dimensions.width} height={dimensions.height}/>
        {/* Cards */}
      <Container>
        <Card resourceType='ore' width={dimensions.width} height={dimensions.height} y={dimensions.height * 0} amount={5} fontSize={dimensions.height / 9}/>
        <Card resourceType='wool' width={dimensions.width} height={dimensions.height} y={dimensions.height * 0.16} amount={4} fontSize={dimensions.height / 9}/>
        <Card resourceType='lumber' width={dimensions.width} height={dimensions.height} y={dimensions.height * 0.32} amount={6} fontSize={dimensions.height / 9}/>
        <Card resourceType='grain' width={dimensions.width} height={dimensions.height} y={dimensions.height * 0.48} amount={3} fontSize={dimensions.height / 9}/>
        <Card resourceType='brick' width={dimensions.width} height={dimensions.height} y={dimensions.height * 0.64} amount={2} fontSize={dimensions.height / 9}/>
      </Container>

      <LeaderBoard width={dimensions.width} height={dimensions.height} fontSize={dimensions.height / 9}/>

      <DiceComponent canRoll={canRoll} numbersToDisplay={numbersToDisplay} setNumbersToDisplay={setNumbersToDisplay} x={dimensions.width*0.735} y={dimensions.height*0.86} fontSize={dimensions.height / 9}/>

      <ActionsBar width={dimensions.width} height={dimensions.height} fontSize={dimensions.height / 9}/>

      <Bank height={dimensions.height} width={dimensions.width}/>

    </Stage>
    </div>
    

    </>
  );
}

export default App;
