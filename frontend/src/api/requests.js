


// possible endpoints for backend 
const LOCAL_ENDPOINT = "http://localhost:8000"

const chosenEndpointHead = LOCAL_ENDPOINT

async function getOpenGames() {
  const endpoint = chosenEndpointHead + "/play/games";

  const res = await fetch(endpoint, {
    headers: { "Content-Type": "application/json" }
  })

  return res.json()
} 

async function postOpenGame(gameTitle, numPlayers) {
  const endpoint = chosenEndpointHead + "/play/games";

  const postContents = {
    game_title: gameTitle,
    num_players: numPlayers,
    created_by: ""
  }

  const res = await fetch(endpoint, {
    method: "POST",
    mode: "cors",
    cache: "no-cache",
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(postContents)
  })  

  return res.json()
}

export {
  getOpenGames,
  postOpenGame
}