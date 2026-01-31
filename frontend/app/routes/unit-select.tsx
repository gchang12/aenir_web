import {
  Link,
  Outlet,
} from "react-router";
import type { Route } from "./+types/unit-select";

import { UNITS } from "../UNITS";

export default function({ params }: Route.ClientLoaderArgs) {
  console.log(params);
  return (
    <>
    <h1>Unit Select</h1>
    <Outlet />
    </>
  );
}
