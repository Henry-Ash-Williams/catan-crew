interface LobbyComponentProps {
    players: string[];
    onStartGame: () => void;
}

function LobbyComponent(props: LobbyComponentProps){
    const isGameReady = props.players.length === 4;

    const handleStartGame = () => {
        if (isGameReady) {
            props.onStartGame();
        }
    }
    return(
        <div>
            <h2>Lobby</h2>
            <ul>
                {props.players.map((player, index) => (
                <li key={index}>{player}</li>
                ))}
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