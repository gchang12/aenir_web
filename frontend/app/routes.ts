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
    ...prefix("new", [
      layout("./routes/morphs/new/layout.tsx", [
        index("./routes/morphs/new/index.tsx"),
        ...prefix(":game/", [
          index("./routes/morphs/new/UnitSelect.tsx"),
          route(":unit/", "./routes/morphs/new/UnitConfirm.tsx"),
      ]),
    ]),
  ]),
])
] satisfies RouteConfig;
