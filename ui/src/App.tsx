import './styles/App.css';

import { io, Socket } from 'socket.io-client';
import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { Container, Graphics, Sprite, Stage, useApp, useTick, InteractionEvents } from '@pixi/react';
import { Texture } from 'pixi.js';

import Trade from './components/Trade';
import Menu from './components/Menu';
import Card from './components/Card';
import LeaderBoard from './components/LeaderBoard';
import ActionsBar from './components/ActionsBar';
import { DiceComponent } from './components/Dice';
import { BoardComponent } from './components/Board';
import { LobbyComponent } from './components/Lobby';
import Bank from './components/Bank';

interface Players{
  red: string
  blue: string
  green: string
  yellow: string
}

interface Resources{
  ore: number
  wool: number
  grain: number
  lumber: number
  brick: number
}

const socket = io('http://localhost:3001');

function App() {
  const [menuActive, setMenuActive] = useState<boolean>(true)
  const [hasJoined, setHasJoined] = useState(false);
  const [gameStarted, setGameStarted] = useState<boolean>(false)
  const [gameID, setGameID] = useState<string>("")
  const [players, setPlayers] = useState<Players>({"red":"AI","blue":"AI","green":"AI","yellow":"AI"})
  const [socketID, setSocketID] = useState<string>("")
  const [idToPlayer, setIdToPlayer] = useState<Map<string, string>>(new Map<string, string>())
  const [boardState, setBoardState] = useState<string>("")
  const [trade, setTrade] = useState(false);
  const [canRoll, setCanRoll] = useState(false);
  const [numbersToDisplay, setNumbersToDisplay] = useState<[number, number]>([6, 6]);
  const [dimensions, setDimensions] = useState({
    height: 9 * Math.min(window.innerHeight / 9, window.innerWidth / 16),
    width: 16 * Math.min(window.innerHeight / 9, window.innerWidth / 16)
  })
  const cardContainer = useRef(null);
  const [resources, setResources] = useState<Resources>({ore: 0, wool: 0, grain: 0, lumber: 0, brick: 0})
  const [clickableTiles, setClickableTiles] = useState<string[]>([])
 
  const getClickableTiles = (gameID: string, player: string, type: string) => {
    const json = {
      game_id: gameID,
      player_colour: idToPlayer.get(player)
    }
    console.log("JSON:\n" + json.game_id + "\n" + json.player_colour)
    socket.emit("valid_location/" + type, json)
  }

  useEffect(() => {
    socket.on("valid_location/roads", data => {
      console.log("CLICKABLE TILES:\n" + data)
      setClickableTiles(data)
    })
    return () => {
      socket.off("valid_location/roads")
    }
  })

  useEffect(() => {
    socket.on("valid_location/cities", data => {
      console.log("CLICKABLE TILES:\n" + data)
      setClickableTiles(data)
    })
    return () => {
      socket.off("valid_location/cities")
    }
  })

  useEffect(() => {
    socket.on("valid_location/settlements", data => {
      console.log("CLICKABLE TILES:\n" + data)
      setClickableTiles(data)
    })
    return () => {
      socket.off("valid_location/settlements")
    }
  })



  const getPlayerResources = (gameID: string, player: string) => {
    const json = {
      game_id: gameID,
      player_colour: idToPlayer.get(player)
    }
    idToPlayer.get(player)
    socket.emit("player_resources", json)
  }

  useEffect(() => {
    socket.on("player_resources", data => {
      console.log("PLAYER RESOURCES:\n" + data)
      setResources(data)
    })
    return () => {
      socket.off("player_resources")
    }
  })


  const handleJoinGame = () => {
    socket.emit("join_room")
    
    setHasJoined(!hasJoined);
  }

  useEffect(() => {
    // just a listener
    socket.on("join_room", data => {
      console.log("Joining room...")
      const p = JSON.parse(data)
      setPlayers(p) // currently connected players socket IDs and associated colours
      setSocketID(socket.id) // This client's socket ID
      const idToPlayer = new Map<string, string>()
      idToPlayer.set(p.red, "red")
      idToPlayer.set(p.blue, "blue")
      idToPlayer.set(p.green, "green")
      idToPlayer.set(p.yellow, "yellow")  
      setIdToPlayer(idToPlayer)

    return () => {
      socket.off("join_room")
    }})
  })
  
  const handleStartGame = () => {
      console.log('Starting the game...')
      socket.emit("start_game") 
  }
  
  useEffect(() => {
    socket.on("start_game", data => {
      setBoardState(data.board_state)
      // console.log(data.game_id)
      setGameID(data.game_id)
      // console.log(typeof(data.game_id))
      // console.log(gameID)
      setGameStarted(!gameStarted)
      // const json = {
      //   game_id: data.game_id,
      //   player_colour: idToPlayer.get(socket.id)
      // }
      // console.log("JSON:\n" + json.game_id + "\n" + json.player_colour)
      // console.log(boardState)
      // getPlayerResources(data.game_id, socketID)
    })

    return () => {
      socket.off("start_game")
    }
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
    : !gameStarted ?  <LobbyComponent socketID={socketID} players={players} idToPlayer={idToPlayer} onStartGame={handleStartGame}/> :
      <div style={{display: "flex", height: "100vh", justifyContent: "center", alignItems: "center"}}>
        <Stage width={dimensions.width} height={dimensions.height}>
            {/* Background */}
          <Sprite width={dimensions.width} height={dimensions.height} texture={Texture.WHITE} tint={0x00FFFF}></Sprite>

          {/* Board */}
          <BoardComponent boardState={boardState} setBoardState={setBoardState} size={15} width={dimensions.width} height={dimensions.height}/>
            {/* Cards */}
          <Container>
            <Card resourceType='ore' width={dimensions.width} height={dimensions.height} y={dimensions.height * 0} amount={resources.ore} fontSize={dimensions.height / 9}/>
            <Card resourceType='wool' width={dimensions.width} height={dimensions.height} y={dimensions.height * 0.16} amount={resources.wool} fontSize={dimensions.height / 9}/>
            <Card resourceType='lumber' width={dimensions.width} height={dimensions.height} y={dimensions.height * 0.32} amount={resources.lumber} fontSize={dimensions.height / 9}/>
            <Card resourceType='grain' width={dimensions.width} height={dimensions.height} y={dimensions.height * 0.48} amount={resources.grain} fontSize={dimensions.height / 9}/>
            <Card resourceType='brick' width={dimensions.width} height={dimensions.height} y={dimensions.height * 0.64} amount={resources.brick} fontSize={dimensions.height / 9}/>
          </Container>

          <LeaderBoard width={dimensions.width} height={dimensions.height} fontSize={dimensions.height / 9}/>

          <DiceComponent canRoll={canRoll} numbersToDisplay={numbersToDisplay} setNumbersToDisplay={setNumbersToDisplay} x={dimensions.width*0.735} y={dimensions.height*0.86} fontSize={dimensions.height / 9}/>

      <ActionsBar width={dimensions.width} height={dimensions.height} fontSize={dimensions.height / 9} methods={[[setTrade, trade]]}/>

      <Bank height={dimensions.height} width={dimensions.width} fontSize={dimensions.height / 9}/>

      <Trade height={dimensions.height} width={dimensions.width} visible={trade} fontSize={dimensions.height / 9}/>

        </Stage>
      </div>
      
    }
    </>
  );
}

export default App;
