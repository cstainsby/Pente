
import { useRouteError } from "react-router-dom";

export default function ErrorPage() {
  const error = useRouteError();
  console.error(error);

  return (
    <div id="ErrorPage">
      <h1>Error has occurred</h1>
      <p>
        <i>{error.statusText || error.message}</i>
      </p>
    </div>
  );
}