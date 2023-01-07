import { useState } from "react";


const GamePage = (props) => {

  return (
    <div className="GamePage">
      <GameDisplay/>
      <GameSpace/>
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
      {/* {gameState } */}
    </div>
  )
}

const GameSpace = (props) => {

  let [currPlayerId, setCurrPlayerId] = useState(null);

  return (
    <div className="GameSpaceContainer">
      <GamePiece/>
      <div className="GameSpaceItem GameSpace">
        <div className="GameSpaceWhiteSpace" />
        <div className="GameSpaceWhiteSpace" />
        <div className="GameSpaceWhiteSpace" />
        <div className="GameSpaceWhiteSpace" />
      </div>
    </div>
  )
}

const GamePiece = (props) => {
  const pieceColorMapping = {
    0: ""
  }
  
  return (
    <div className="GameSpaceItem GamePeice">

    </div>
  );
}

export default GamePage;