import type { Route } from "./+types/home";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "Aenir - A Fire Emblem stat calculator" },
    { name: "description", content: "Calculate Fire Emblem stats" },
  ];
}

export default function Home() {
  return (
    <>
    </>
  );
}
