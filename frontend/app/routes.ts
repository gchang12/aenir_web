import {
  type RouteConfig,
  index,
  route,
  prefix,
} from "@react-router/dev/routes";

export default [
  index("./routes/index.tsx"),
  ...prefix("morphs", [
    index("./routes/morphs/index.tsx"),
    ...prefix("new-morph", [
      index("./routes/morphs/new-morph/index.tsx"),
      ...prefix(":game/", [
        index("./routes/morphs/new-morph/game.tsx"),
        route(":unit/", "./routes/morphs/new-morph/unit.tsx"),
    ]),
  ]),
])
] satisfies RouteConfig;
