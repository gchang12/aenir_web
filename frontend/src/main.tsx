import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'

import {
  createBrowserRouter,
  redirect,
} from "react-router";
import {
  RouterProvider,
} from "react-router/dom";
import {
  Navigate,
} from "react-router-dom";

import './index.css'

const router = createBrowserRouter([
  {
    path: "/",
    element: <p>Hello world</p>
  },
  {
    path: "/login/",
    loader: () => {
    },
    element: <Navigate to="?next=http://127.0.0.1:8000/registration/login/"></Navigate>,
  }
]);

const root = document.getElementById('root');

createRoot(root).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>,
)
