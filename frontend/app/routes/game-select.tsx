import {
  Link,
  Outlet,
} from "react-router";
import type { Route } from "./+types/game-select";

import { GAMES } from "../GAMES";

export default function({ params }: Route.ClientLoaderArgs) {
  return (
    <>
    <h1>Create Morph</h1>
    <section id="create-morph">
    <menu id="game-select">
    {GAMES.map(game => {
      const { gameNo, name, title } = game;
      return (
        <li key={gameNo}>
          <Link to={"fe" + gameNo}>
            <figure>
              <img src={["", "images", name, "cover-art.png"].join('/')} />
              <figcaption><h2>{title}</h2></figcaption>
            </figure>
          </Link>
        </li>
      );
    })
    }
    </menu>
    <Outlet />
    </section>
    </>
  );
}
