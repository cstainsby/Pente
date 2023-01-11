
import { Link } from "react-router-dom";

import OnlineButtonIcon from "../icons/internet.png";

const SplashPage = (props) => {
  
  return (
    <div className="SplashPage">
      <h1 className="PageTitle">Pente</h1> 
      <ul>
        <li>
          <Link to={"/gameSearch"}>
            <button type="button" className="NavigationButton">
              {/* <img src={OnlineButtonIcon} height="24" className="ButtonIcon"/> */}
              <span className="ButtonText">Online</span>
            </button>
          </Link>
        </li>
        <li>
          <Link to={"/game/ai"} >
            <button type="button" className="NavigationButton">
              <span className="ButtonText">Play AI</span>
            </button>
          </Link>
        </li>
        <li>
          <Link to={"/analytics"}>
            <button type="button" className="NavigationButton">
              <span className="ButtonText">Info</span>
            </button>
          </Link>
        </li>
      </ul>
    </div>
  );
}

export default SplashPage;