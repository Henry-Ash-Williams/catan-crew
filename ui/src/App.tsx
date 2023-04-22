import './styles/App.css';

import { io } from 'socket.io-client';
import { useEffect, useRef, useState } from 'react';
import { Container, Sprite, Stage } from '@pixi/react';
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

interface AvailableActions{
  buildRoad: boolean
  buildSettlement: boolean
  buildCity: boolean
  buyDevCard: boolean
  trade: false
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
  const [trade, setTrade] = useState(false);
  const [canRoll, setCanRoll] = useState(true);
  const [numbersToDisplay, setNumbersToDisplay] = useState<[number, number]>([6, 6]);
  const [dimensions, setDimensions] = useState({
    height: 9 * Math.min(window.innerHeight / 9, window.innerWidth / 16),
    width: 16 * Math.min(window.innerHeight / 9, window.innerWidth / 16)
  })
  const [resources, setResources] = useState<Resources>({ore: 0, wool: 0, grain: 0, lumber: 0, brick: 0})
  const [devcards, setDevCards] = useState()
  const [availableActions, setAvailableActions] = useState<string[]>([])
  const [clickableTiles, setClickableTiles] = useState<string[]>([])
  const [leaderBoardState, setLeaderBoardState] = useState([])
  const [boardState, setBoardState] = useState<string>("")

  function action (type: string) {
    const json = {
      game_id : game_idR.current,
      player_colour: idToPlayer.get(socketID)
    }
    console.log('API CALLED', type)
    socket.emit(type, json)
  }

  function validLocationsFor (type: string, reachable: boolean) {
    const json = {
      game_id : game_idR.current,
      player_colour: idToPlayer.get(socketID),
      reachable: reachable
    }
    console.log('API CALLED', type, 'REACHABLE?', reachable)
    socket.emit('valid_location/' + type, json)
  }

  const getCurrentPlayer = () => {
    console.log("API CALLED current_player")
    const json = {
      game_id: game_idR.current,
    }
    socket.emit("current_player", json)
  }

  const handleJoinGame = () => {
    socket.emit("join_room")
    setHasJoined(!hasJoined);
  }

  const handleStartGame = () => {
      console.log('Starting the game...')
      socket.emit("start_game") 
  }

  useEffect(() => {
    socket.on("end_turn", data => {
      console.log("END TURN:\n", data)
      // todo: add logic to check end turn is valid
      // todo: on confirmation, make all actions unavailable
      getCurrentPlayer()
    })

    socket.on("roll_dice", data => {
      console.log("ROLL DICE:\n", data)
      const d1 = Math.floor(data.dice_val/2)
      setNumbersToDisplay([d1, data.dice_val - d1])
      setCanRoll(false)
      if(data.dice_val == 7){
        action("discard_resource_card")
        action("valid_robber_locations")
      action("updated_player_resources")
    }
  })

    socket.on("valid_robber_locations", data => {
      console.log("VALID ROBBER LOCATIONS:\n", data)
      setClickableTiles(data)
    })

    socket.on("robber_location", data => {
      console.log("ROBBER LOCATION:\n", data)
    })


    socket.on("board_state", data => {
      console.log("BOARD STATE:\n", data)
      setBoardState(data)
    })

    socket.on("current_player", data => {
      // console.log("CURRENT PLAYER:\n", data)
      if(data.player_colour == idToPlayer.get(socketID)){
        action('available_actions')
        setCanRoll(true)
      }
      action("player_resources");
      action("board_state");
      action("updated_player_resources");
      action("valid_location/roads");
      action("valid_location/settlements");
      action("valid_location/cities");
    })

    socket.on("available_actions", data => {
      console.log("AVAILABLE ACTIONS:\n", data)
      setAvailableActions(data)
    })
    
    socket.on("valid_location/roads", data => {
      console.log("CLICKABLE TILES:\n", data.toString())
      setClickableTiles(data)
    })

    socket.on("valid_location/cities", data => {
      console.log("CLICKABLE TILES:\n", data)
      setClickableTiles(data)
    })

    socket.on("valid_location/settlements", data => {
      console.log("CLICKABLE TILES:\n", data)
      setClickableTiles(data)
    })

    socket.on("player_resources", data => {
      console.log("PLAYER RESOURCES:\n", data['0'], data['1'], data['2'], data['3'], data['4'])
      const resources: Resources = {
        ore: data['2'],
        wool: data['4'],
        grain: data['3'],
        lumber: data['1'],
        brick: data['0'],
      }

      setResources(resources)
    })

    socket.on("updated_player_resources", data => {
      console.log("UPDATED PLAYER RESOURCES:\n", data)
      const resources: Resources = {
        ore: data['2'],
        wool: data['4'],
        grain: data['3'],
        lumber: data['1'],
        brick: data['0'],
      }
      setResources(resources)
    })

    socket.on("join_room", data => {
      console.log("Joining room...")
      console.log("Players: ", data)
      const p = JSON.parse(data)
      setPlayers(p) // currently connected players socket IDs and associated colours
      setSocketID(socket.id) // This client's socket ID
      const idTo = new Map<string, string>()
      idTo.set(p.red, "red")
      idTo.set(p.blue, "blue")
      idTo.set(p.green, "green")
      idTo.set(p.yellow, "yellow")  
      console.log(idTo)
      setIdToPlayer(idTo)
    })

    socket.on("start_game", data => {
      game_idR.current = data.game_id;
      setBoardState(data.board_state)
      setGameStarted(!gameStarted);
      console.log('Started game with these players' ,players)
      action("leaderboard")
      getCurrentPlayer()
    })

    socket.on('leaderboard', data => {
      console.log("LEADERBOARD",data)
      setLeaderBoardState(data)
    })

    return () => {
      socket.off('start_game');
      socket.off('leaderboard');
      socket.off('join_room');
      socket.off('player_resources');
      socket.off('valid_location/roads');
      socket.off('valid_location/cities');
      socket.off('valid_location/settlements');
      socket.off('available_actions');
      socket.off('current_player');
      socket.off('board_state');
      socket.off('end_turn');
      socket.off('roll_dice');
    }
  },[idToPlayer, resources])



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
          <BoardComponent boardState={boardState} setBoardState={setBoardState} size={15} width={dimensions.width} height={dimensions.height} clickable={clickableTiles}/>
            {/* Cards */}
          <Container>
            <Card resourceType='ore' width={dimensions.width} height={dimensions.height} y={dimensions.height * 0} amount={resources.ore} fontSize={dimensions.height / 9}/>
            <Card resourceType='wool' width={dimensions.width} height={dimensions.height} y={dimensions.height * 0.16} amount={resources.wool} fontSize={dimensions.height / 9}/>
            <Card resourceType='lumber' width={dimensions.width} height={dimensions.height} y={dimensions.height * 0.32} amount={resources.lumber} fontSize={dimensions.height / 9}/>
            <Card resourceType='grain' width={dimensions.width} height={dimensions.height} y={dimensions.height * 0.48} amount={resources.grain} fontSize={dimensions.height / 9}/>
            <Card resourceType='brick' width={dimensions.width} height={dimensions.height} y={dimensions.height * 0.64} amount={resources.brick} fontSize={dimensions.height / 9}/>
          </Container>

          <LeaderBoard width={dimensions.width} height={dimensions.height} fontSize={dimensions.height / 9} state={leaderBoardState}/>

          <DiceComponent canRoll={canRoll} numbersToDisplay={numbersToDisplay} setNumbersToDisplay={setNumbersToDisplay} onClick={() => {action('roll_dice')}} x={dimensions.width*0.735} y={dimensions.height*0.86} fontSize={dimensions.height / 9}/>

      <ActionsBar action={action} getLocationsFor={validLocationsFor} width={dimensions.width} height={dimensions.height} fontSize={dimensions.height / 9} availableActions={availableActions} tradeFunction={[setTrade, trade]}/>

      <Bank height={dimensions.height} width={dimensions.width} fontSize={dimensions.height / 9}/>

      <Trade height={dimensions.height} width={dimensions.width} visible={trade} fontSize={dimensions.height / 9}/>

        </Stage>
      </div>
      
    }
    </>
  );
}

export default App;
