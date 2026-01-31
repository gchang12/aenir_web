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
    <menu id="unit-select">
    {unitList.map(unit => {
      return (
        <li key={unit.name}>
          <Link to={unit.name}>
            <figure>
              <img width="100" src={["", "images", gameName, "characters", unit.name + imageSuffix].join('/')} />
              <figcaption>{unit.name}</figcaption>
            </figure>
            <dl>
              <dt>Class</dt>
              <dd>{unit.class}</dd>
              <dt>Lv</dt>
              <dd>{unit.lv}</dd>
            </dl>
          </Link>
        </li>
      );
    })
    }
    </menu>
    <Outlet />
    </>
  );
}
