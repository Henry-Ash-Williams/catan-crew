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

interface Players{
  red: string
  blue: string
  green: string
  yellow: string
}

const socket = io('http://localhost:3001');

function App() {
  const [menuActive, setMenuActive] = useState<boolean>(true)
  
  const [players, setPlayers] = useState<Players>(JSON.parse('{"red":"","blue":"","green":"","yellow":""}'))
  const [hasJoined, setHasJoined] = useState(false);
  // const [socket, setSocket] = useState<Socket | null>(null)
  
  const handleJoinGame = () => {
    socket.emit("join_room")
    setHasJoined(true);
  }

  useEffect(() => {
    // just a listener
    socket.on("join_room", data => {
      setPlayers(data)
      console.log("PLAYERS:")
  
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

    {!hasJoined ? 
      <Menu onShow={handleJoinGame}/>
    : <LobbyComponent players={players} onStartGame={handleStartGame}/>}
    <div style={{display: "flex", height: "100vh", justifyContent: "center", alignItems: "center"}}>

    </div>
    

    </>
  );
}

export default App;
