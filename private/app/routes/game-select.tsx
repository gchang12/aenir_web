import React from "react";

import {
  NavLink,
  Outlet,
} from "react-router";
import type { Route } from "./+types/game-select";

import {
  GAMES,
} from "../lib/GAMES";
import type {
  Game,
} from "../lib/_types";

function GameSelectItem(game : Game) : React.ReactNode {
  return (
    <li>
      <NavLink to={"fe" + game.no}>
        <figure>
          <img src={["", "images", game.name, "cover-art.png"].join('/')} />
          <figcaption><h2>{game.title}</h2></figcaption>
        </figure>
      </NavLink>
    </li>
  );
}

export default function({ params }: Route.ClientLoaderArgs) : React.ReactElement {
  return (
    <>
    <h1>Create Morph</h1>
    <section id="create-morph">
      <menu id="game-select">
      {GAMES.map(game => {
        return (
          <GameSelectItem key={game.no} {...game} />
        );
      })
      }
      </menu>
      <Outlet />
    </section>
    </>
  );
}

