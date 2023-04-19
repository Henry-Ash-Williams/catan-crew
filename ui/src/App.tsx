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
  const game_idR = useRef('');
  const [menuActive, setMenuActive] = useState<boolean>(true)
  const [hasJoined, setHasJoined] = useState(false);
  const [gameStarted, setGameStarted] = useState<boolean>(false)
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
  const [resources, setResources] = useState<Resources>({ore: 0, wool: 0, grain: 0, lumber: 0, brick: 0})
  const [devcards, setDevCards] = useState()
  const [clickableTiles, setClickableTiles] = useState<string[]>([])
  // Type can be "roads", "cities", "settlements"
  const getClickableTiles = (type: string) => {
    const json = {
      game_id: game_idR.current,
      player_colour: idToPlayer.get(socketID)
    }
    console.log("JSON:\n" + json.game_id + "\n" + json.player_colour)
    
    socket.emit("valid_location/" + type, json)
  }

  const getCurrentPlayer = () => {
    console.log("GETTING CURRENT PLAYER")
    const json = {
      game_id: game_idR.current,
    }
    socket.emit("current_player", json)
  }

  const getAvailableActions = () => {
    const json = {
      game_id: game_idR.current,
      player_colour: idToPlayer.get(socketID)
    }
    socket.emit("available_actions", json)
  }

  const endTurn = () => {
    const json = {
      game_id: game_idR.current,
      player_colour: idToPlayer.get(socketID)
    }
    socket.emit("end_turn", json)
  }

  useEffect(() => {
    socket.on("end_turn", data => {
      console.log("END TURN:\n" + data)
      // todo: add logic to check end turn is valid
      // todo: on confirmation, make all actions unavailable
      getCurrentPlayer()
    })

    socket.on("current_player", data => {
      console.log("CURRENT PLAYER:\n" + data)
      if(data === idToPlayer.get(socketID)){
        getAvailableActions()
      }
    })

    socket.on("available_actions", data => {
      console.log("AVAILABLE ACTIONS:\n" + data)
    })
    
    socket.on("valid_location/roads", data => {
      console.log("CLICKABLE TILES:\n" + data.toString())
      setClickableTiles(data)
    })

    socket.on("valid_location/cities", data => {
      console.log("CLICKABLE TILES:\n" + data)
      setClickableTiles(data)
    })

    socket.on("valid_location/settlements", data => {
      console.log("CLICKABLE TILES:\n" + data)
      setClickableTiles(data)
    })

    socket.on("player_resources", data => {
      console.log("PLAYER RESOURCES:\n" + data)
      setResources(data)
    })

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
    })

    socket.on("start_game", data => {
      game_idR.current = data.game_id;
      setBoardState(data.board_state)
      setGameStarted(!gameStarted);
      // console.log(game_idR.current)
      // console.log(boardState)
      // console.log(data.game_id)
      // console.log(gameID);
      // getClickableTiles("settlements")
      getCurrentPlayer()
    })

    return () => {
      socket.off("current_player");
      socket.off("available_actions")
      socket.off("valid_location/roads");
      socket.off("valid_location/cities");
      socket.off("valid_location/settlements");
      socket.off("player_resources");
      socket.off('start_game')
    }
  })

  const getPlayerResources = () => {
    const json = {
      game_id: game_idR.current,
      player_colour: idToPlayer.get(socketID)
    }
    socket.emit("player_resources", json)
  }

  const handleJoinGame = () => {
    socket.emit("join_room")
    setHasJoined(!hasJoined);
  }

  const handleStartGame = () => {
      console.log('Starting the game...')
      socket.emit("start_game") 
  }
  

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
  },[])

  

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
