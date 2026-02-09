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
  GlowingStatTable,
} from "../lib/StatTables";
import {
  previewMorph,
} from "../lib/quintessence";

export async function loader({ params }: Route.LoaderArgs) : { game: Game; unit: Unit; defaultMorph: Morph } {
  const { gameId, unitName } : {gameId: GameID, unitName: string} = params;
  const unit: Unit = UNITS.find(someUnit => someUnit.name === unitName && "fe" + someUnit.gameNo === gameId);
  const game: Game = GAMES.find(someGame => "fe" + someGame.no === gameId);
  const defaultMorph = await previewMorph({game_no: game.no, name: unitName});
  return { game, unit, defaultMorph };
};

export default function UnitConfirm({
  loaderData,
}: Route.ComponentProps) : React.ReactElement {
  const { game, unit, defaultMorph } = loaderData;
  // const [morph, setMorph] = React.useState<Morph>(defaultMorph);
  const { currentStats, maxStats } = defaultMorph;
  return (
    <div id="unit-confirm">
      <h1>{game.title}</h1>
      <UnitPortrait {...{unit}} />
      <GlowingStatTable {...{currentStats, maxStats, unit}} />
    </div>
  );
};

