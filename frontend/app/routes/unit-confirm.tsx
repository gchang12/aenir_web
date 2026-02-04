import {
  Link,
  Outlet,
} from "react-router";
import type { Route } from "./+types/unit-confirm";

import type {
  GameID,
  Unit,
  Game,
  Stats,
} from "../lib/_types";

import {
  UNITS,
} from "../lib/UNITS";

import {
  GAMES,
} from "../lib/GAMES";

import {
  StatTable,
} from "../lib/StatTables";

export default function({ params }: Route.ClientLoaderArgs) {
  const { gameId, unitName } : {gameId: GameID, unitName: string} = params;
  const [unit]: [Unit] = UNITS.filter(someUnit => someUnit.name === unitName && "fe" + someUnit.gameNo === gameId);
  const [game]: [Game] = GAMES.filter(someGame => "fe" + someGame.no === gameId);
  const stats: Stats = [
    ["HP", 18],
    ["Pow", 5],
    ["Skl", 5],
    ["Spd", 7],
    ["Lck", 7],
    ["Def", 5],
    ["Res", 0],
    ["Con", 6],
    ["Mov", 5],
  ];
  return (
    <>
    <h1>{game.title}</h1>
    <h2>{unitName}</h2>
    <StatTable unit={unit} stats={stats} />
    </>
  );
};
