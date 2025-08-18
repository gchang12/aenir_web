import { useState } from 'react'; 
import type { Route } from "./+types/team";
import axios from 'axios';
import "../../../app.css";

import type { Route } from "./+types/home";

import GameSelectMenu from './index.tsx';

export function meta({}: Route.MetaArgs) {
  return [
    { title: "Aenir: A Fire Emblem stat calculator" },
    { name: "description", content: "Calculate Fire Emblem stats here!" },
  ];
}

export async function unitListLoader( {rawGame, gameNo} ) {
  const unitList = [];
  await axios
    .get("http://127.0.0.1:8000/dracogate/api/initialization_view/",
      {params: {game: gameNo}},
    )
    .then(res => unitList.push(...res.data))
    .catch(err => console.log(err));
  return unitList;
}

export async function loader( { params }: Route.LoaderArgs) {
  const game = {
    "fe4": {
      no: 4,
      name: "genealogy-of-the-holy-war",
      title: "Genealogy of the Holy War",
    },
    "fe5": {
      no: 5,
      name: "thracia-776",
      title: "Thracia 776",
    },
    "fe6": {
      no: 6,
      name: "binding-blade",
      title: "The Sword of Seals",
    },
    "fe7": {
      no: 7,
      name: "blazing-sword",
      title: "The Blazing Blade",
    },
    "fe8": {
      no: 8,
      name: "the-sacred-stones",
      title: "The Sacred Stones",
    },
    "fe9": {
      no: 9,
      name: "path-of-radiance",
      title: "Path of Radiance",
    },
  }[params.game];
  const gameNo = game.no;
  game.urlName = params.game;
  const unitList = await unitListLoader( {game, gameNo} );
  return [game, unitList];
}

function UnitSelectMenu(
  {loaderData,
}: Route.ComponentProps) {
  const [game, unitList] = loaderData;
  const gameUrlName = game.urlName;
  return (
    <>
      <GameSelectMenu />
      <h1>Unit Select</h1>
      <h2>{game.title}</h2>
      <menu>
        {unitList.map(unit => {
          const imgSuffix = game.no === 8 ? "gif" : "png";
          const imgFile = `${unit}.${imgSuffix}`;
          const unitHref = `/morphs/new-morph/${game.urlName}/${unit}`
          return (
            <li key={unit}>
              <a href={unitHref}>
                <figure>
                  <img src={`/static/${game.name}/characters/${imgFile}`} alt={`Portrait of ${unit}, ${imgFile}`} />
                  <figcaption>
                    {unit}
                  </figcaption>
                </figure>
              </a>
            </li>
          );
        })
        }
      </menu>
    </>
  );
}

export default UnitSelectMenu;
