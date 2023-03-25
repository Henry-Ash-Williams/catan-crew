import './App.css';
import { BoardComponent } from './components/Board';
import { Container, Sprite, Stage } from '@pixi/react';
import { Texture } from 'pixi.js';
import { UiComponent } from './components/Ui';
function App() {

  return (
    <Stage width={1000} height={1000}>
      <Sprite width={1000} height={1000} texture={Texture.WHITE} ></Sprite>
        <BoardComponent size={3} width={1000} height={1000}/>
        <UiComponent></UiComponent>
    </Stage>
  );
}

export default App;
