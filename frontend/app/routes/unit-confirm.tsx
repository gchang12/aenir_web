import {
  Link,
  Outlet,
} from "react-router";
import type { Route } from "./+types/unit-confirm";

export default function({ params }: Route.ClientLoaderArgs) {
  console.log(params);
  return (
    <>
    <h1>Unit Confirm</h1>
    <Outlet />
    </>
  );
};
