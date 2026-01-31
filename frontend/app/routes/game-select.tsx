import {
  Link,
  Outlet,
} from "react-router";

import { GAMES } from "../GAMES";

export default function() {
  return (
    <>
    <menu>
    {GAMES.map(game => {
      const { gameNo, name, title } = game;
      return (
        <li key={gameNo}>
        <Link to={"fe" + gameNo}>{title}</Link>
        </li>
      );
    })
    }
    </menu>
    <Outlet />
    </>
  );
}
