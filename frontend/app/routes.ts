import type {
  RouteConfig,
} from "@react-router/dev/routes";

import {
  index,
  route,
} from "@react-router/dev/routes";

export default [
  index("routes/home.tsx"),
  route("create-morph/", "routes/game-select.tsx", [
    route(":gameId", "routes/unit-select.tsx", [
      route(":unitName", "routes/unit-confirm.tsx"),
    ]),
  ]),
] satisfies RouteConfig;
