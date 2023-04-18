import { useState } from "react"

interface Players {
    red: string
    blue: string
    green: string
    yellow: string
}

interface LobbyComponentProps {
    players: string;
    onStartGame: () => void;
}

function LobbyComponent(props: LobbyComponentProps){
    const [isGameReady, setIsGameReady] = useState<boolean>(true);
    let players = JSON.parse(props.players) 


    const handleStartGame = () => {
        if (isGameReady) {
            props.onStartGame();
        }
    }
    return(
        <div>
            <h2>Lobby</h2>
            <ul>
                <li>RED: {players.red}</li>
                <li>BLUE: {players.blue}</li>
                <li>GREEN: {players.green}</li>
                <li>YELLOW: {players.yellow}</li>
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