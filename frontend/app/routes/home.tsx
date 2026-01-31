import {
  Link,
} from "react-router";
import type { Route } from "./+types/home";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "New React Router App" },
    { name: "description", content: "Welcome to React Router!" },
  ];
}

export default function Home() {
  const urlPrefix = "create-morph";
  return (
    <>
    <h1>Home</h1>
    <Link to={urlPrefix}>Create Morph</Link>
    </>
  );
}
