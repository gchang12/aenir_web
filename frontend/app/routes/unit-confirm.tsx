import {
  Link,
  Outlet,
} from "react-router";
import type { Route } from "./+types/unit-confirm";

export default function({ params }: Route.ClientLoaderArgs) {
  console.log(params);
  const { game, unit } = params;
  return (
    <>
    <h1>{unit}</h1>
    <h2>{game}</h2>
    </>
  );
};
