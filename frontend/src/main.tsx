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
  MorphHub,
  MorphMethodExecute,
  //EvolveMorph2,
} from "./routes";
import {
  getMorph,
  createMorph,
  retrieveMorph,
  simulateMorphMethod,
  setLocalMorphs,
  getLocalMorphs,
  getNullArgs,
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
                  const morphId = gameId.toUpperCase() + "-" + unitName + "_" + nowAsString.slice(4, nowAsString.indexOf('.')).replaceAll("-", "").replace("T", "-").replaceAll(":", "");
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
            Component: MorphHub,
            loader: async ({params}) => {
              const {pkLoc} = params;
              const pk = getLocalMorphs()[pkLoc].pk;
              const fullMorph = await retrieveMorph(pk);
              console.log("loader.fullMorph:", Object.entries(fullMorph));
              return {pk, fullMorph};
            },
          },
          {
            path: ":pkLoc/:methodName",
            Component: MorphMethodExecute,
            loader: async ({params}) => {
              const {pkLoc, methodName} = params;
              const nullArgs = getNullArgs(methodName);
              const morphRecord = getLocalMorphs()[pkLoc];
              const {pk, gameId, unitName} = morphRecord;
              const {morph, paramBounds} = await simulateMorphMethod(pk, methodName, nullArgs);
              console.log("MorphMethodExecute.loader.paramBounds:", Object.entries(paramBounds));
              console.log("MorphMethodExecute.loader.morph:", Object.entries(morph));
              const fullMorph = {
                initArgs: {
                  gameNo: Number(gameId.replace("fe", "")),
                  unitName,
                },
                morph,
              };
              return {pk, fullMorph, paramBounds};
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
 
