
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import { getOpenGames } from "../api/requests";

const GameSearchPage = (props) => {

  let [availbleGames, setAvailbleGames] = useState([])


  // useEffect(() => {
  //   getOpenGames()
  //     .then(jsonData => console.log(jsonData))
  //     .catch(err => setAvailbleGames([]))
  // }, []);


  return (
    <div className="GameSearchPage">
      <Link to={"/"}>
        <button type="button">
          Back
        </button>
      </Link>
      <h3>Avalible Games</h3>

      <button>Add Game</button>

      {availbleGames.length > 0 &&
        availbleGames.map(() => {

        })
      } 

    </div>
  )
}

const OpenGamePotrait = (props) => {


  return (
    <div>

    </div>
  )
}

export default GameSearchPage;