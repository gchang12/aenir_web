import {
  StrictMode,
  useEffect,
} from 'react'
import { createRoot } from 'react-dom/client'
import {
  createBrowserRouter,
  RouterProvider,
} from 'react-router';

import './index.css'

import {
  Root,
  GameSelect,
  UnitSelect,
  UnitConfirm,
} from "./lib/routes";
import {
  previewMorph,
} from "./lib/functions";

// TODO: Add 'errorElement' prop

const router = createBrowserRouter([
  {
    path: "/",
    Component: Root,
    children: [
      {
        path: "/create-morph/",
        Component: GameSelect,
        children: [
          {
            path: ":gameId/",
            Component: UnitSelect,
            children: [
              {
                path: "/create-morph/:gameId/:unitName",
                loader: async ({params}) => {
                  const {gameId, unitName} = params;
                  const game_no = gameId.replace("fe", "");
                  const name = unitName;
                  const kwargs = {};
                  // console.log(game_no, name, kwargs);
                  const {morph, missingParams} = await previewMorph(game_no, name, kwargs);
                  return {morph, missingParams, unitName, gameId};
                },
                action: () => {
                  return;
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

