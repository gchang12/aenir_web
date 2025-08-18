import { useState, Fragment } from 'react'; 
import type { Route } from "./+types/home";

import axios from 'axios';

import "../../../app.css";
import {
  unitStatsLoader,
} from '../../../dataLoaders/morphs/new-morph.tsx';
import {
  GameUrlList,
  GameProfile,
  UnitProfile,
  UnitUrlList,
  StatTable,
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

export async function loader( { params }: Route.LoaderArgs) {
  const game = findFireEmblemGame({params});
  const unit = params.unit;
  const initParams = {
    game: game.no,
    name: unit,
  };
  let [metaStats, currentStats, missingParams] = await unitStatsLoader(initParams);
  if (missingParams !== null) {
    const [field, choices] = missingParams;
    const defaultVal = choices[0];
    initParams[field] = defaultVal;
    [metaStats, currentStats, missingParams] = await unitStatsLoader(initParams);
  }
  return [game, initParams, metaStats, currentStats, missingParams];
};

function Main(
  {loaderData,
}: Route.ComponentProps) {
  const [game, defaultInitParams, metaStats, currentStats, missingParams] = loaderData;
  const [initParams, setInitParams] = useState(defaultInitParams);
  const fireEmblemGames = getFireEmblemGames();
  async function retryCreateMorph(e) {
    const inputWidget = e.currentTarget;
    const field = inputWidget.dataset.fieldname;
    let value = inputWidget.value;
    if (inputWidget.type === "checkbox") {
      value = inputWidget.checked;
    };
    const tempInitParams = {...initParams};
    tempInitParams[field] = value;
    setInitParams(tempInitParams);
  }
  return (
    <>
      <nav id="game-select">
        <menu>
          <GameUrlList gameList={fireEmblemGames} />
        </menu>
      </nav>
      <UnitProfile game={game} unit={initParams.name} />
      <StatTable stats={[["Class", metaStats.currentCls], ["Lv", metaStats.currentLv]].concat(currentStats)} />
      <form>
        {missingParams && (
          getOptionList({missingParams, retryCreateMorph}).map(option => option)
        )}
        <button>
          Create!
        </button>
      </form>
    </>
  );
};

export default Main;
