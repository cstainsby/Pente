
import { useEffect, useState } from "react";
import { Link, useLoaderData } from "react-router-dom";

import { getOpenGames } from "../api/requests";

const GameSearchPage = (props) => {

  const { openGames } = useLoaderData();


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
      <h3>Open Games</h3>

      <button>Add Game</button>

      {openGames.length ? (
        openGames.map(() => {

        })
      ) : (
        <p>
          <i>No open games</i>
        </p>
      )
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