import {
  Link,
  Outlet,
} from "react-router";
import type { Route } from "./+types/unit-select";

import { UNITS } from "../UNITS";
import { GAMES } from "../GAMES";

export default function({ params }: Route.ClientLoaderArgs) {
  const { game } = params;
  const [unitList] = UNITS.filter(game_units => "fe" + game_units.game === game).map(game_units => game_units.units);
  const imageSuffix = game === 8 ? ".gif" : ".png";
  const [gameName] = GAMES.filter(someGame => "fe" + someGame.gameNo === game).map(someGame => someGame.name);
  return (
    <>
    <menu>
    {unitList.map(unit => {
      const { name, lv } = unit;
      return (
        <li key={name}>
          <img src={["", "images", gameName, "characters", name + imageSuffix].join('/')} />
          <Link to={name}>{name}</Link>
          <h2>{unit.class}</h2>
          <h2>{lv}</h2>
        </li>
      );
    })
    }
    </menu>
    <Outlet />
    </>
  );
}
