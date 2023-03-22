import './App.css';
import { BoardComponent } from './components/Board';
import { Container, Sprite, Stage } from '@pixi/react';
import { Texture } from 'pixi.js';

function App() {

  // const boardData = fetch('../public/board.json')
  //   .then((response) => response.json())
  //   .then((json) => console.log(json));

  return (
    <Stage width={1000} height={1000}>
      <Sprite width={1000} height={1000} texture={Texture.WHITE}></Sprite>
        <BoardComponent size={3} width={1000} height={1000}/>

    </Stage>
  );
}

export default App;
