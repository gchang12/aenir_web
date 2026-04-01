import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'

import {
  createBrowserRouter,
  redirect,
} from "react-router";
import { RouterProvider } from "react-router/dom";

import axios from "axios";

import './index.css'

import {
  BACKEND_URL,
} from "./lib/constants";
import {
  Username,
} from "./lib/functions";
import {
  Root,
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
              return redirect(BACKEND_URL + "accounts/login/");
            },
          },
          {
            path: "login_done/",
            loader: async () => {
              const username = await Username.fetch();
              Username.set(username);
              return redirect("/");
            },
          },
          // TODO: logout/
          {
            path: "create-account/",
            loader: () => {
              return redirect(BACKEND_URL + "accounts/create-account/");
            },
          },
          {
            path: "password_reset/",
            loader: () => {
              return redirect(BACKEND_URL + "accounts/password_reset/");
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
