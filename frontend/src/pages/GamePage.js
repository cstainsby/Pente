import { useState } from "react";
import { Outlet } from "react-router-dom";


const GamePage = (props) => {

  return (
    <div className="GamePage">
      In Game
      <Outlet/>
    </div>
  );
}

const GameSidebar = (props) => {

  return (
    <div className="GameSidebar"> 

    </div>
  )
}

const GameDisplay = (props) => {
  let [gridLength, setGridLength] = useState(19);

  let [gameState, setGameState] = useState(
    new Array(gridLength).fill(new Array(gridLength).fill(0, 0, gridLength))
  )
  console.log(gameState)
  console.log(gameState.length)

  return (
    <div className="GameDisplay">
      <svg width="400" height="100">
        <rect width="400" height="100" />
      </svg>
    </div>
  )
}

const OnlineGameDisplay = (props) => {

}

const AiGameDisplay = (props) => {
  console.log("Ai game loaded")
  return (
    <div>
      AI Game
      <GameDisplay/>
    </div>
  )
}

export {
  GamePage,
  OnlineGameDisplay,
  AiGameDisplay
};