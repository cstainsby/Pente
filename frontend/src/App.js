import React, { Children } from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter, Routes, Route, Outlet, Link, useNavigate, useLocation, createBrowserRouter, RouterProvider } from "react-router-dom";

import SplashPage from "./pages/SplashPage.js";
import GameSearchPage from './pages/GameSearchPage.js';
import { GamePage, OnlineGameDisplay, AiGameDisplay } from "./pages/GamePage.js";
import AnalyticsPage from './pages/AnalyticsPage.js';
import ErrorPage from "./pages/ErrorPage.js";

import { gameSearchPageLoader } from "./api/loaders.js"

import 'bootstrap/dist/css/bootstrap.css';
// Put any other imports below so that CSS from your
// components takes precedence over default styles.

import './App.css';

function App() {
  return (
    <div className="App">
      <RouterProvider router={router} />
      {/* <BrowserRouter>
        <Routes>
          <Route path="/" element={<SplashPage/>} />
          <Route path="gameSearch" element={<GameSearchPage/>} />

          <Route page="game" element={<GamePage/>}>
            <Route page="ai" element={<AiGameDisplay/>}/>

            <Route page="online" element={<GamePage/>}>
              <Route path=":gameId" element={<GamePage/>}/>
            </Route>
          </Route>

          <Route path="analytics" element={ <AnalyticsPage/> }/>
          <Route path="*" element={<ErrorPage/>} />
        </Routes>
      </BrowserRouter> */}
    </div>
  );
}

const router = createBrowserRouter([
  {
    path: "/",
    element: <SplashPage/>,
    errorElement: <ErrorPage/>
  },
  {
    path: "gameSearch",
    element: <GameSearchPage/>,
    loader: gameSearchPageLoader,
    errorElement: <ErrorPage/>
  },
  {
    path: "game",
    element: <GamePage/>,
    children: [
      {
        path: "online/:gameId",
        element: <OnlineGameDisplay/>,
        errorElement: <ErrorPage/>
      },
      {
        path: "ai",
        element: <AiGameDisplay/>,
        errorElement: <ErrorPage/>
      }
    ]
  },
  {
    path: "analytics",
    element: <AnalyticsPage/>,
    errorElement: <ErrorPage/>
  }
])

export default App;
