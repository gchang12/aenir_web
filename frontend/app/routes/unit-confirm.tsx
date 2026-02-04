import {
  Link,
  Outlet,
} from "react-router";
import type { Route } from "./+types/unit-confirm";

import type {
  GameID,
} from "../lib/_types";

import {
  StatTable,
} from "../lib/StatTables";

export default function({ params }: Route.ClientLoaderArgs) {
  const { gameId, unitName } : {gameId: GameID, unit: string} = params;
  return (
    <>
    <h1>{unitName}</h1>
    <h2>{gameId}</h2>
    </>
  );
};
