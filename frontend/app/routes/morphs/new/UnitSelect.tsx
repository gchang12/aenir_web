import { useState } from 'react'; 

{/* import type { Route } from "./+types/team"; */}
import type { Route } from "./+types/home";

import axios from 'axios';

import "../../../app.css";
import {
  unitListLoader,
} from '../../../_dataLoaders/morphs/new.tsx';
import {
  GameUrlList,
  GameProfile,
  UnitUrlList,
} from '../../../_components/morphs/new.tsx';
import {
  getFireEmblemGames,
  findFireEmblemGame,
} from '../../../_constants/morphs/new.tsx';

export function meta({}: Route.MetaArgs) {
  return [
    { title: "Aenir: A Fire Emblem stat calculator" },
    { name: "description", content: "Calculate Fire Emblem stats here!" },
  ];
}

export function loader( { params }: Route.LoaderArgs) {
  const game = findFireEmblemGame({params});
  {/* const unitList = await unitListLoader({game}); */}
  const unitList = unitListLoader({game});
  return [game, unitList];
}

function Main(
  {loaderData,
}: Route.ComponentProps) {
  const [game, unitList, gameUrl, gameTitle] = loaderData;
  const gameRank = `fe${game}`;
  const fireEmblemGames = getFireEmblemGames();
  return (
    <>
      <article>
        <h1>Game Select</h1>
        <nav>
          <menu>
            <GameUrlList gameList={fireEmblemGames} />
          </menu>
        </nav>
        <nav>
          <h2>{gameTitle}</h2>
          <GameProfile game={game} />
          <menu>
            <UnitUrlList game={game} unitList={unitList} />
          </menu>
        </nav>
      </article>
    </>
  );
}

export default Main;
