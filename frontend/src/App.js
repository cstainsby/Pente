import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter, Routes, Route, Outlet, Link, useNavigate, useLocation } from "react-router-dom";

import SplashPage from "./pages/SplashPage.js";
import GameSearchPage from './pages/GameSearchPage.js';
import GamePage from "./pages/GamePage.js";
import AnalyticsPage from './pages/AnalyticsPage.js';
import ErrorPage from "./pages/ErrorPage.js";

import 'bootstrap/dist/css/bootstrap.css';
// Put any other imports below so that CSS from your
// components takes precedence over default styles.

import './App.css';

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<SplashPage/>} />
          <Route path="gameSearch" element={<GameSearchPage/>} />
          <Route page="/game">
            <Route path=":gameId" element={<GamePage/>} />
          </Route>
          <Route path="analytics" element={ <AnalyticsPage/> }/>
          <Route path="*" element={<ErrorPage/>} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
