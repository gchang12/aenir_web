import {
  type RouteConfig,
  index,
  route,
} from "@react-router/dev/routes";

export default [
  index("routes/home.tsx"),
  route("create-morph/", "routes/game-select.tsx", [
    route(":game", "routes/unit-select.tsx", [
      route(":unit", "routes/unit-confirm.tsx"),
    ]),
  ]),
] satisfies RouteConfig;
