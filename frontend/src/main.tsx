import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'

import {
  createBrowserRouter,
  redirect,
} from "react-router";
import { RouterProvider } from "react-router/dom";

import './index.css'

import {
  BACKEND_URL,
} from "./lib/constants";
import {
  Root,
} from "./routes";

const router = createBrowserRouter([
  {
    path: "/",
    Component: Root,
  },
  {
    path: "/login/",
    loader: () => {
      return redirect(BACKEND_URL + "accounts/login/");
    },
  },
  {
    path: "/create-account/",
    loader: () => {
      return redirect(BACKEND_URL + "accounts/create-account");
    },
  },
]);

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>,
)
