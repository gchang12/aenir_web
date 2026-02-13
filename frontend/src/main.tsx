import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { createBrowserRouter, RouterProvider } from 'react-router';
import './index.css'
import {
  // App,
  UnitConfirm,
  previewMorph,
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
  }
]);

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>,
)
