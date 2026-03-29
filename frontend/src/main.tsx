import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'

import {
  createBrowserRouter,
} from "react-router";
import {
  RouterProvider,
} from "react-router/dom";

import './index.css'

const router = createBrowserRouter([
  {
    path: "/",
    element: <p>Hello world</p>
  },
]);

const root = document.getElementById('root');

createRoot(root).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>,
)
