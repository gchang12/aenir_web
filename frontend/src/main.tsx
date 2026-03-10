import {
  StrictMode,
  useEffect,
  useContext,
} from 'react'
import { createRoot } from 'react-dom/client'
import {
  createBrowserRouter,
  RouterProvider,
  redirect,
} from 'react-router';

import './index.css'

import {
  Root,
  GameSelect,
  UnitSelect,
  UnitConfirm,
} from "./routes";
import {
  getMorph,
  createMorph,
  retrieveMorph,
  setLocalMorphs,
  getLocalMorphs,
} from "./lib/functions";

const router = createBrowserRouter([
  {
    path: "/",
    Component: Root,
    children: [
      {
        path: "create-morph",
        Component: GameSelect,
        children: [
          {
            path: ":gameId",
            Component: UnitSelect,
            children: [
              {
                path: ":unitName",
                loader: async ({params, request}) => {
                  const {gameId, unitName} = params;
                  const game_no = Number(gameId.replace("fe", ""));
                  const name = unitName;
                  const options = {};
                  console.log("UnitConfirm.loader:", request.url);
                  const queryString = new URLSearchParams(request.url.split('?')[1]);
                  for (const [key, value] of queryString.entries()) {
                    switch (value) {
                      case "on":
                        options[key] = true;
                        break;
                      case "off":
                        options[key] = false;
                        break;
                      default:
                        options[key] = value;
                    };
                  };
                  const morph = await getMorph(game_no, name, options);
                  console.log("UnitConfirm.getMorph", Object.entries(morph));
                  return {morph};
                },
                action: async ({params, request}) => {
                },
                Component: UnitConfirm,
              }
            ],
          },
        ],
      },
    ],
  },
]);

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>,
)

