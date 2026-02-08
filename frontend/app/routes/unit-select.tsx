import React from "react";

import {
  NavLink,
  Outlet,
} from "react-router";
import type { Route } from "./+types/unit-select";

import type {
  Unit,
  Game,
  GameID,
} from "../lib/_types";
import {
  UnitImage,
} from "../lib/UnitPortrait";
import {
  UNITS,
} from "../lib/UNITS";
import {
  GAMES,
} from "../lib/GAMES";

function UnitSelectItem({ unit, gameId } : { unit: Unit; gameId: GameID }) : React.ReactNode {
  const game: Game = GAMES.find(someGame => "fe" + someGame.no === gameId);
  return (
    <li>
      <NavLink to={unit.name}>
        <UnitImage unit={unit} />
        <table>
          <tbody>
            <tr>
              <th colSpan="2"><h2>{unit.name}</h2></th>
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
      </NavLink>
    </li>
  );
}

export default function({ params }: Route.ClientLoaderArgs) : React.ReactElement {
  const { gameId } = params;
  const unitList: Unit[] = UNITS.filter(unit => "fe" + unit.gameNo === gameId);
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

