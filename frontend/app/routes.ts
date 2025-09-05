import {
  type RouteConfig,
  route,
  index,
  layout,
} from "@react-router/dev/routes";

export default [
  route("/", "routes/home.tsx"),
  layout("./layouts/create-morph/_root.tsx", [
    route("create-morph/", "./routes/create-morph/_root.tsx"),
    layout("./layouts/create-morph/game.tsx", [
      route("create-morph/:feGame/", "./routes/create-morph/game.tsx"),
      route("create-morph/:feGame/:feUnit/", "./routes/create-morph/unit.tsx"),
    ]),
  ]),
] satisfies RouteConfig;
