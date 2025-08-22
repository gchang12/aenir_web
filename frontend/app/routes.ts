import {
  type RouteConfig,
  index,
  route,
  layout,
  prefix,
} from "@react-router/dev/routes";

export default [
  index("./routes/index.tsx"),
  ...prefix("morphs", [
    index("./routes/morphs/index.tsx"),
    ...prefix("new-morph", [
      layout("./routes/morphs/new-morph/layout.tsx", [
        index("./routes/morphs/new-morph/index.tsx"),
        ...prefix(":game/", [
          index("./routes/morphs/new-morph/UnitSelect.tsx"),
          route(":unit/", "./routes/morphs/new-morph/UnitConfirm.tsx"),
      ]),
    ]),
  ]),
])
] satisfies RouteConfig;
