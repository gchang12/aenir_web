import type {
  Unit,
  Game,
  GameID,
} from "../lib/_types";

import {
  GAMES,
} from "../lib/GAMES";

// TODO: Declare image-width by games

export function UnitImage({ unit } : {unit: Unit}) {
  const [game] = GAMES.filter(someGame => someGame.no === unit.gameNo);
  const imageSuffix = game.no === 8 ? ".gif" : ".png";
  const src = ["", "images", game.name, "characters", unit.name + imageSuffix].join('/');
  return (
    <img width="100" src={src} alt={src} />
  );
}

export function UnitPortrait({ unit }: { Unit }) {
  return (
    <figure>
    <UnitImage unit={unit} />
      <figcaption><h2>{unit.name}</h2></figcaption>
    </figure>
  );
};
