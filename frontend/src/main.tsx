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
                action: async ({params, request}) => {
                  // Get parameters for 'createMorph'
                  const {gameId, unitName} = params;
                  const gameNo = gameId.replace("fe", "");
                  const formData = await request.formData();
                  const morphId = formData.get("morph_id");
                  const options = {};
                  for (const [key, value] of formData) {
                    if (key !== "morph_id") {
                      options[key] = value;
                    }
                  };
                  const response = createMorph(morphId, gameNo, unitName, options)
                    .then(data => {
                      const pk = data.pk;
                      if (localStorage.getItem("morphs") === "") {
                        localStorage.setItem("morphs", '[]');
                      };
                      const morphs = JSON.parse(localStorage.getItem('morphs'));
                      morphs.push(pk);
                      localStorage.setItem("morphs", JSON.stringify(morphs));
                      return redirect("/morphs/");
                    })
                    .catch(err => {
                      console.log(err);
                      //throw redirect("/morphs/");
                    });
                  return redirect("/morphs/");
                },
                Component: UnitConfirm,
              }
            ],
          },
        ],
      },
      {
        path: "morphs/",
        Component: Root,
      },
    ],
  },
]);

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>,
)

