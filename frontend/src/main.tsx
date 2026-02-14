import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { createBrowserRouter, RouterProvider } from 'react-router';
import './index.css'
import {
  App,
  UnitConfirm,
  previewMorph,
  UnitSelect,
  GameSelect,
} from './App.tsx'

const router = createBrowserRouter([
  {
    path: "/create-morph/:gameId/:unitName",
    loader: async ({params}) => {
      const {gameId, unitName} = params;
      const game_no = gameId.replace("fe", "");
      const name = unitName;
      const kwargs = {};
      console.log(game_no, name, kwargs);
      const {morph, missingParams} = await previewMorph(game_no, name, kwargs);
      return {morph, missingParams, unitName, gameId};
    },
    Component: UnitConfirm,
  },
  {
    path: "/create-morph/",
    Component: GameSelect,
  },
  {
    path: "/create-morph/:gameId/",
    Component: UnitSelect,
  },
  {
    path: "/",
    Component: App,
  },
]);

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>,
)
