import {
  Link,
  Outlet,
} from "react-router";
import type { Route } from "./+types/unit-select";

import { UNITS } from "../UNITS";

export default function({ params }: Route.ClientLoaderArgs) {
  const { game } = params;
  const [unitList] = UNITS.filter(game_units => "fe" + game_units.game === game).map(game_units => game_units.units);
  return (
    <>
    <menu>
    {unitList.map(unit => {
      const { name, lv } = unit;
      return (
        <li key={name}>
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
