import { useState } from "react"

interface Players {
    red: string
    blue: string
    green: string
    yellow: string
}

interface LobbyComponentProps {
    players: Players;
    onStartGame: () => void;
}

function LobbyComponent(props: LobbyComponentProps){
    const [isGameReady, setIsGameReady] = useState<boolean>(false);


    // const props.players = JSON.parse(props.players)//'{"red":"f2_1V6EL4Fb_XBOzAAAT","blue":"f2_1V6EL4Fb_XBOzAAAT","green":"f2_1V6EL4Fb_XBOzAAAT","yellow":"nYR9cALCEeKLHH9QAAAh","undefined":"VJf7IPDa7WD0AsaZAAAt"}');
    console.log(typeof(props.players))
    console.log(props.players.blue)
    var playerList: JSX.Element[] = []
    for(const player in props.players){
        playerList.push(<li key={player}>{player}: {props.players[player]}</li>)
    }

    const handleStartGame = () => {
        if (isGameReady) {
            props.onStartGame();
        }
    }
    return(
        <div>
            <h2>Lobby</h2>
            <ul>
                {/* {Object.keys(props.players).map((player: string) => (
                <li key={player}>{props.players[player]}</li>
                ))}
                
                <li>{props.players.red}</li> */}
                {playerList}
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