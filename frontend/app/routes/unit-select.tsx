import {
  Link,
  Outlet,
} from "react-router";
import type { Route } from "./+types/unit-select";

import type {
  Unit,
} from "../lib/_types";

import {
  UNITS,
} from "../lib/UNITS";
import {
  GAMES,
} from "../lib/GAMES";

function UnitSelectItem(unit : Unit) {
  return (
    <li>
      <Link to={unit.name}>
        <img width="100" src={["", "images", gameName, "characters", unit.name + imageSuffix].join('/')} />
        <table>
          <tr>
            <th><h2>{unit.name}</h2></th>
          </tr>
          <tr>
            <th>Class</th>
            <td>{unit.class}</td>
          </tr>
          <tr>
            <th>Lv</th>
            <td>{unit.lv}</td>
          </tr>
        </table>
      </Link>
    </li>
  );
}

export default function({ params }: Route.ClientLoaderArgs) {
  const { game } = params;
  const imageSuffix = game === 8 ? ".gif" : ".png";
  const unitList = UNITS.filter(unit => "fe" + unit.game === game);
  const [gameName] = GAMES.filter(someGame => "fe" + someGame.gameNo === game).map(someGame => someGame.name);
  return (
    <>
    <menu id="unit-select">
    {unitList.map(unit => {
      return (
        <UnitSelectItem key={unit.name} {...unit} />
      );
    })
    }
    </menu>
    <Outlet />
    </>
  );
}
