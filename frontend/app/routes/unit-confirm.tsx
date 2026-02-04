import React from "react";

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
  Morph,
} from "../lib/_types";
import {
  UNITS,
} from "../lib/UNITS";
import {
  GAMES,
} from "../lib/GAMES";
import {
  UnitPortrait,
} from "../lib/UnitPortrait";
import {
  StatTable,
} from "../lib/StatTables";
import {
  createMorph,
} from "../lib/quintessence";

export default function({ params }: Route.ClientLoaderArgs) : React.ReactElement {
  const { gameId, unitName } : {gameId: GameID, unitName: string} = params;
  const unit: Unit = UNITS.find(someUnit => someUnit.name === unitName && "fe" + someUnit.gameNo === gameId);
  const game: Game = GAMES.find(someGame => "fe" + someGame.no === gameId);
  const [morph, setMorph] = React.useState<Morph>(createMorph({game_no: game.no, name: unitName}));
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
    <UnitPortrait {...{unit}} />
    <StatTable {...{unit, stats}} />
    </>
  );
};

