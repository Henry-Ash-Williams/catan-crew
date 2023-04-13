import { useState } from "react";
import '../styles/Menu.css'

interface MenuProps{
    onShow: () => void
}

export default function Menu(props: MenuProps){
    const [settingsView, setSettingsView] = useState(true)

    return(
        <div id="menu">
            {settingsView ?
            <div className="mainMenu">
                <button className="btns" onClick={() => {props.onShow()}}>New Game</button>
                <button className="btns" onClick={() => {props.onShow()}}>Join Game</button>
            </div>
            :
            <div className="gameMenu">
            </div>}
        </div>
    )
}