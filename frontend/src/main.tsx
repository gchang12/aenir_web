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
                loader: async ({params}) => {
                  const {gameId, unitName} = params;
                  const game_no = Number(gameId.replace("fe", ""));
                  const name = unitName;
                  const kwargs = {};
                  const morph = await getMorph(game_no, name, kwargs);
                  return {data: morph, gameId, unitName};
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

