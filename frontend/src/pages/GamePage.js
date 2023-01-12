import { useState } from "react";
import { Outlet } from "react-router-dom";


const GamePage = (props) => {

  return (
    <div className="GamePage">
      <GameSidebar/>
      <Outlet/>
      <GameLog/>
    </div>
  );
}

const GameSidebar = (props) => {

  return (
    <div className="GameSidebar"> 
      <PlayerTag playerName="AI"/>
    </div>
  )
}

const PlayerTag = (props) => {
  // props 
  //  player name 
  //  number of captures

  // const tagElement = document.getElementById("PlayerTag");
  // tagElement.style.backgroundColor = "#00FF00"
  return (
    <div id="PlayerTag">
      <h3>{ props.playerName }</h3>
    </div>
  )
}

const GameLog = (props) => {

  let [gameLog, setGameLog] = useState([]);

  return (
    <div id="GameLog">
      <h3>Game Log</h3>
      <div id="GameLogContents">
        
        { gameLog.length > 0 ? (
          <ul>
            {
              gameLog.map(() => {
                <li>entry</li>
              })
            }
          </ul>
        ) : (
          <h4>No Moves Made</h4> 
        )
        }
      </div>
    </div>
  )
}

const GameDisplay = (props) => {
  let [gridLength, setGridLength] = useState(17);

  let [gameState, setGameState] = useState(
    new Array(gridLength).fill(new Array(gridLength).fill(0, 0, gridLength))
  )
  console.log(gameState)
  console.log(gameState.length)

  const boardMargin = 40; // how much margin is around the board 
  const offsetFromOrigin = boardMargin / 2; // how much each item within the board needs to be offset

  const gameDisplayLength = window.screen.height / 1.5;
  const boardDisplayLength = gameDisplayLength - boardMargin;
  // line X and Ys will hold all info to 
  const lineIntervalSpacing = boardDisplayLength / gridLength;
  let helperCount = Array.from({ length: gridLength + 1 }, (_, i) => i);
  const lineXs = helperCount.map(x => x * lineIntervalSpacing);
  const lineYs = helperCount.map(y => y * lineIntervalSpacing);

  // parallel to the game state, holds all x and y intersections relative to the grid
  const intersectionCoords = []
  // fill intersections
  for(let i = 0; i < lineXs.length; i++) {
    for(let j = 0; j < lineYs.length; j++) {
      intersectionCoords.push({
        "x": lineXs[i], 
        "y": lineYs[j]
      });
    }
  }




  return (
    <div className="GameDisplay">
      <svg width={ gameDisplayLength } height={ gameDisplayLength }>
        <rect width={ gameDisplayLength } height={ gameDisplayLength } fill="green" />

        <rect x={ offsetFromOrigin } y={ offsetFromOrigin } width={ boardDisplayLength } height={ boardDisplayLength } fill="white" />
        {/* place lines */}
        { lineXs.map(x =>
          <line x1={x + offsetFromOrigin} x2={x + offsetFromOrigin} y1={offsetFromOrigin} y2={ boardDisplayLength + offsetFromOrigin } stroke="black" strokeWidth={2}/>
        )}
        { lineYs.map(y =>
          <line x1={offsetFromOrigin} x2={ boardDisplayLength + offsetFromOrigin } y1={y + offsetFromOrigin} y2={y + offsetFromOrigin} stroke="black" strokeWidth={2}/>
        )}

        {/* place possible positions for playable tokens */}
        {intersectionCoords.map(coords => 
          <GameToken xCoord={ coords["x"] + offsetFromOrigin } yCoord={ coords["y"] + offsetFromOrigin } />
        )}
      </svg>
    </div>
  )
}

const GameToken = (props) => {
  // props include 
  //  xCoord: int
  //  yCoord: int
  //  currentPlayerNum 

  let [isVisible, setIsVisible] = useState(false);

  const onEmptyIntersectionClick = () => {
    console.log("intersection clicked")
    setIsVisible(true);
  }

  return (
    <>
      {isVisible ? (
        <circle id="ActiveToken" r="12" cx={props.xCoord} cy={props.yCoord}/>
      ) : (
        <circle id="InactiveToken" r="12" cx={props.xCoord} cy={props.yCoord} onClick={ onEmptyIntersectionClick }/>   
      )}
    </>
  );
}

const GameIntersection = (props) => {

}

const OnlineGameDisplay = (props) => {

}

const AiGameDisplay = (props) => {
  console.log("Ai game loaded")
  return (
    <div id="AiGameDisplay">
      <GameDisplay/>
    </div>
  )
}

export {
  GamePage,
  OnlineGameDisplay,
  AiGameDisplay
};