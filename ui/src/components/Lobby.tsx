import { useState } from "react"

interface Players {
    red: string
    blue: string
    green: string
    yellow: string
}

interface LobbyComponentProps {
    players: Players
    socketID: string
    idToPlayer: Map<string, string>
    onStartGame: () => void;
}

function LobbyComponent(props: LobbyComponentProps){
    const [isGameReady, setIsGameReady] = useState<boolean>(true);
    const handleStartGame = () => {
        if (isGameReady) {
            props.onStartGame();
        }
    }
    return(
        <div>
            <h2>Lobby</h2>
            <h5>u r {props.idToPlayer.get(props.socketID)}</h5>
            <ul>
                <li>RED: {props.players.red}</li>
                <li>BLUE: {props.players.blue}</li>
                <li>GREEN: {props.players.green}</li>
                <li>YELLOW: {props.players.yellow}</li>
            </ul>
    
            <button
                style={{ opacity: isGameReady ? 1 : 0.5 }}
                onClick={handleStartGame}
                disabled={!isGameReady}
            >
                Start Game
            </button>
        </div>
  
    )
}

export {LobbyComponent}