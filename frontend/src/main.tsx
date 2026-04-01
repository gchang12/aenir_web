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
  LoginView,
} from "./routes";

const router = createBrowserRouter([
  {
    path: "/",
    Component: Root,
    children: [
      {
        path: "accounts",
        children: [
          {
            path: "login/",
            loader: () => {
              // TODO: Replace with a working login view
              //return redirect(BACKEND_URL + "accounts/login/");
            },
            Component: LoginView,
          },
          {
            path: "create-account/",
            loader: () => {
              return redirect(BACKEND_URL + "accounts/create-account");
            },
          },
          {
            path: "password_reset/",
            loader: () => {
              return redirect(BACKEND_URL + "accounts/password_reset");
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
