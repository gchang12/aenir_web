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
      return (
        <li key={unit}>
          <Link to={unit}>{unit}</Link>
        </li>
      );
    })
    }
    </menu>
    <Outlet />
    </>
  );
}
