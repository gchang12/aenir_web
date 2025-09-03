import {
  type RouteConfig,
  route,
  index,
  layout,
} from "@react-router/dev/routes";

export default [
  route("/", "routes/home.tsx"),
  layout("./layouts/create-morph/_root.tsx", [
    route("create/", "./routes/create-morph/_root.tsx"),
    layout("./layouts/create-morph/game.tsx", [
      route("create/:feGame/", "./routes/create-morph/game.tsx"),
      route("create/:feGame/:feUnit/", "./routes/create-morph/unit.tsx"),
    ]),
  ]),
] satisfies RouteConfig;
