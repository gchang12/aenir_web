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
} from "./lib/routes";
import {
  previewMorph,
  createMorph,
} from "./lib/functions";

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
                action: ({params, request}) => {
                  const {gameId, unitName} = params;
                  const gameNo = gameId.replace("fe", "");
                  const options = {};
                  let morph;
                  let morph_id;
                  request.formData()
                    .then(data => {
                      morph_id = data['morph_id'];
                      for (const [key, value] of data) {
                        options[key] = value;
                      };
                    })
                    .catch(err => console.log(err));
                  createMorph(morph_id, gameNo, unitName, options)
                    .then(data => {
                      morph = data;
                    })
                    .catch(err => console.log(err));
                  if (morph != undefined) {
                    throw redirect("/morphs/");
                  }
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

