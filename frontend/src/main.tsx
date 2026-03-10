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
                  // prepare to make morph
                  const {gameId, unitName} = params;
                  const nowAsString = (new Date()).toISOString();
                  const morphId = gameId.toUpperCase() + "-" + unitName + "-" + nowAsString.slice(4, nowAsString.indexOf('.')).replace("T", "_").replaceAll(":", "").replaceAll("-", "");
                  const game_no = Number(gameId.replace("fe", ""));
                  const options = {};
                  const formData = await request.formData();
                  for (const [key, value] of formData.entries()) {
                    options[key] = value;
                  };
                  console.log(`createMorph(${morphId}, ${game_no}, ${unitName}, ${Object.entries(options)})`);
                  const {pk} = await createMorph(morphId, game_no, unitName, options);
                  // store morph.
                  if (!getLocalMorphs()) {
                    setLocalMorphs([]);
                  };
                  const localMorphs = getLocalMorphs();
                  localMorphs.unshift({pk, morphId, gameId, unitName});
                  while (localMorphs.length > 5) {
                    localMorphs.pop();
                  };
                  setLocalMorphs(localMorphs);
                  console.log("UnitConfirm.action:", formData);
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
        children: [
          {
            path: ":pkLoc",
            Component: EvolveMorph,
            loader: async ({params}) => {
              const {pkLoc} = params;
              const pk = getLocalMorphs()[pkLoc].pk;
              const fullMorph = await retrieveMorph(pk);
              console.log("fullMorph:", Object.entries(fullMorph));
              return {fullMorph};
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
 
