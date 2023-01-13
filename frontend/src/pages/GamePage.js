import { useEffect, useState } from "react";
import { Outlet, useOutletContext } from "react-router-dom";


const GamePage = (props) => {
  

  let [gridLength, setGridLength] = useState(17);

  let [gameState, setGameState] = useState(
    new Array(gridLength).fill(new Array(gridLength).fill(0, 0, gridLength))
  );

  // How each of the log types should be shaped 
  // placement log shape: (log_id, player_id_who_placed, x, y)
  // capture log shape: (log_id, player_id_who_captured,  [ordered (x, y) of all stones involved])
  // win log shape: (log_id, player_id)
  let [gameLog, setGameLog] = useState([]);
  console.log("on game page render" + gameLog.length)

  let [currentPlayer, setCurrentPlayer] = useState("placeholder")

  return (
    <div className="GamePage">
      <GameSidebar/>
      <Outlet context={[gameState, setGameState, gameLog, setGameLog]}/>
      <GameLog gameLog={ gameLog }/>
    </div>
  );
}

const OnlineGameDisplay = (props) => {

}

const AiGameDisplay = (props) => {
  // in the Ai version of the game, websockets will not be used
  // we wont need to wait on other players to make on a descision rather we only need to query the backend 
  // model for a response

  // 
  const [gameState, setGameState, gameLog, setGameLog] = useOutletContext();

  const notifyBoardStateChange = (changeInfo) => {
    const changeX = changeInfo["x"];
    const changeY = changeInfo["y"];
    const newValue = changeInfo["newValue"];

    console.log("notified of state change" + changeX + " " + changeY)
    
    const newLog = {
      log_type: "PLACEMENT",
      x: changeX, 
      y: changeY,
      player_id: newValue
    }
    console.log("old log: " + gameLog)
    let updatedGameLog = [...gameLog]
    updatedGameLog.push(newLog)
    console.log("new log: " + updatedGameLog)
    setGameLog(updatedGameLog)

    // push this change to the backend, allow it to take care of the logic 
    // get the new 
  }

  console.log("Ai game loaded")
  return (
    <div id="AiGameDisplay">
      <GameDisplay gridLength={gameState.length} notifyBoardStateChange={ notifyBoardStateChange }/>
    </div>
  )
}

const GameSidebar = (props) => {

  return (
    <div id="GameSidebar"> 
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
  // props include 
  // gameLog: list of json
  console.log("on log render" + props.gameLog)

  return (
    <div id="GameLog">
      <h3>Game Log</h3>
      Items in log: {props.gameLog.length}
      
      <div id="GameLogContents">
        { props.gameLog.length > 0 ? (
          <ul>
            {
              props.gameLog.map((logContents) => {
                return (
                  <li id="GameLogContentListItem" className="">{
                    <p>Player {logContents.player_id} {logContents.log_type}: ({logContents.x}, {logContents.y})</p>
                  }</li>
                )
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
  // props include 
  // gridLength: int 
  // gameState: list of list of int
  // notifyBoardStateChange: func

  const boardMargin = 40; // how much margin is around the board 
  const offsetFromOrigin = boardMargin / 2; // how much each item within the board needs to be offset

  const gameDisplayLength = window.screen.height / 1.5;
  const boardDisplayLength = gameDisplayLength - boardMargin;
  // line X and Ys will hold all info to 
  const lineIntervalSpacing = boardDisplayLength / props.gridLength;
  let helperCount = Array.from({ length: props.gridLength + 1 }, (_, i) => i);
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
          <GameToken 
            xCoord={ coords["x"] + offsetFromOrigin } 
            yCoord={ coords["y"] + offsetFromOrigin } 
            currentPlayerNum={1}
            notifyBoardStateChange={ props.notifyBoardStateChange }
          />
        )}
      </svg>
    </div>
  )
}

const GameToken = (props) => {
  // props include 
  //  xCoord: int
  //  yCoord: int
  //  currentPlayerNum: int
  //  notifyBoardStateChange: func

  let [isVisible, setIsVisible] = useState(false);

  const onEmptyIntersectionClick = () => {
    setIsVisible(true);

    // notify the log that a change has happened
    const changes = {
      "x": props.xCoord,
      "y": props.yCoord,
      "newValue": true
    }
    console.log("changes being accepted " + changes)
    console.log(props.notifyBoardStateChange)
    props.notifyBoardStateChange(changes);
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

export {
  GamePage,
  OnlineGameDisplay,
  AiGameDisplay
};