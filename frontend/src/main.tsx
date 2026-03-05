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
  Morphs,
  EvolveMorph,
} from "./routes";
import {
  previewMorph,
  createMorph,
  retrieveMorph,
  // TODO: Test these functions.
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
                      // TODO: Refactor to leverage getLocalMorphs and setLocalMorphs
                      {/*
                      if (localStorage.getItem("morphs") === "") {
                        localStorage.setItem("morphs", '[]');
                      };
                      */}
                      if (!getLocalMorphs()) {
                        setLocalMorphs([]);
                      };
                      const morphs = getLocalMorphs();// JSON.parse(localStorage.getItem('morphs'));
                      morphs.push(pk);
                      // TODO: If morphs.length >= 5, then erase 'til optimal.
                      // localStorage.setItem("morphs", JSON.stringify(morphs));
                      setLocalMorphs(morphs);
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
        path: "morphs",
        Component: Morphs,
        loader: async () => {
          if (!getLocalMorphs()) {
            setLocalMorphs([]);
          };
          const localMorphs = getLocalMorphs();
          //console.log(localMorphs, typeof localMorphs);
          const fetchTasks = localMorphs.map(pk => retrieveMorph(pk));
          const morphs = await Promise.all(fetchTasks);
          return {morphs};
        },
        children: [
          {
            path: ":pkLoc",
            Component: EvolveMorph,
            loader: async ({params}) => {
              const {pkLoc} = params;
              return {};
            },
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

