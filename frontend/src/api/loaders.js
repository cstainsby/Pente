// functions which wrap all requests needed to load a given page

import { getOpenGames } from "./requests.js"

async function gameSearchPageLoader() {
  const openGames = await getOpenGames();
  
  return { openGames };
} 

export {
  gameSearchPageLoader,
}