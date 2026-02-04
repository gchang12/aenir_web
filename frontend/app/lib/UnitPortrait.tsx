import React from "react";

import type {
  Unit,
  Game,
  GameID,
} from "../lib/_types";

import {
  GAMES,
} from "../lib/GAMES";

const IMAGE_WIDTH_BY_GAME: Array<[GameID, number]> = [
  ["fe4", 100],
  ["fe5", 100],
  ["fe6", 100],
  ["fe7", 100],
  ["fe8", 100],
  ["fe9", 100],
];

// TODO: Declare image-width by games

export function UnitImage({ unit } : {unit: Unit}) : React.ReactNode {
  const game: Game = GAMES.find(someGame => someGame.no === unit.gameNo);
  const imageSuffix: string = game.no === 8 ? ".gif" : ".png";
  const src: string = ["", "images", game.name, "characters", unit.name + imageSuffix].join('/');
  const width: number = IMAGE_WIDTH_BY_GAME.find(gameWidth => gameWidth[0] === "fe" + game.no)[1];
  return (
    <img {...{width, src}} alt={src} />
  );
}

export function UnitPortrait({ unit }: { unit: Unit }) : React.ReactNode {
  return (
    <figure>
    <UnitImage {...{unit}} />
      <figcaption><h2>{unit.name}</h2></figcaption>
    </figure>
  );
};
