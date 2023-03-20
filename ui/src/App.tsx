import React from 'react';
import logo from './logo.svg';
import './App.css';
import { Board } from './components/Board';
import { Stage } from '@pixi/react';

function App() {
  return (
    <Stage>
      <Board size={3} width={1000} height={1000}/>
    </Stage>
  );
}

export default App;
