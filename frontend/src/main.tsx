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
          {
            path: "logout/",
            loader: async () => {
              //return redirect(BACKEND_URL + "accounts/logout/");
              // TODO: This keeps getting interpreted as an unauthenticated request.
              await axios.post(BACKEND_URL + "accounts/api/logout/", {withCredentials: true});
              //await axios.post(BACKEND_URL + "accounts/api-auth/logout/", {withCredentials: true});
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
