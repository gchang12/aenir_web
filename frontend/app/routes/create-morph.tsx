import {
  Link,
  Outlet,
} from "react-router";

import type { Route } from "./+types/create-morph";

export default function({ params }: Route.ClientLoaderArgs) {
  return (
    <>
    <h1>Create Morph</h1>
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
