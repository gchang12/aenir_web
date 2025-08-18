import { useState } from 'react'; 

{/* import type { Route } from "./+types/team"; */}
import type { Route } from "./+types/home";

import axios from 'axios';

import "../../../app.css";
import {
  unitListLoader,
  unitListLoader2,
} from '../../../dataLoaders/morphs/new-morph.tsx';
import {
  GameUrlList,
  GameProfile,
  UnitUrlList,
} from '../../../components/morphs/new-morph.tsx';
import {
  getFireEmblemGames,
  findFireEmblemGame,
} from '../../../constants/morphs/new-morph.tsx';

export function meta({}: Route.MetaArgs) {
  return [
    { title: "Aenir: A Fire Emblem stat calculator" },
    { name: "description", content: "Calculate Fire Emblem stats here!" },
  ];
}

export {/* async */} function loader( { params }: Route.LoaderArgs) {
  const game = findFireEmblemGame({params});
  {/* const unitList = await unitListLoader({game}); */}
  const unitList = unitListLoader2({game});
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
    </>
  );
}

export default Main;
