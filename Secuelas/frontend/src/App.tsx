import React, { useState } from 'react';
import './App.css';
import GameTerminal from './components/GameTerminal';
import LandingPage from './components/LandingPage';

function App() {
  const [gameStarted, setGameStarted] = useState(false);

  return (
    <div className="App">
      {gameStarted ? (
        <GameTerminal />
      ) : (
        <LandingPage onStart={() => setGameStarted(true)} />
      )}
    </div>
  );
}

export default App;
