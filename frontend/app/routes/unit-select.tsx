import {
  Link,
  Outlet,
} from "react-router";
import type { Route } from "./+types/unit-select";

import type {
  Unit,
  GameID,
} from "../lib/_types";

import {
  UNITS,
} from "../lib/UNITS";
import {
  GAMES,
} from "../lib/GAMES";

function UnitSelectItem({ unit, gameId } : { unit: Unit; gameId: GameID }) {
  const [game] = GAMES.filter(someGame => "fe" + someGame.no === gameId);
  const imageSuffix = game.no === 8 ? ".gif" : ".png";
  return (
    <li>
      <Link to={unit.name}>
        <img width="100" src={["", "images", game.name, "characters", unit.name + imageSuffix].join('/')} />
        <table>
          <tbody>
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
          </tbody>
        </table>
      </Link>
    </li>
  );
}

export default function({ params }: Route.ClientLoaderArgs) {
  const { gameId } : { gameId: GameID } = params;
  const unitList = UNITS.filter(unit => "fe" + unit.gameNo === gameId);
  return (
    <>
    <menu id="unit-select">
    {unitList.map(unit => {
      return (
        <UnitSelectItem key={unit.name} {...{unit, gameId}} />
      );
    })
    }
    </menu>
    <Outlet />
    </>
  );
}

