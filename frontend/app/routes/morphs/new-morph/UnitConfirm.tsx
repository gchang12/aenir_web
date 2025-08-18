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
    if (initParams.name === "Gonzales") {
      if (!Object.keys(initParams).includes("hard_mode")) {
        initParams["hard_mode"] = false;
      } else if (!Object.keys(initParams).includes("route")) {
        initParams["route"] = "Lalum";
      } else {
        alert("Unknown error.");
      }
    };
    [metaStats, currentStats, missingParams] = await unitStatsLoader(initParams);
  }
  return [game, initParams, metaStats, currentStats, missingParams];
};

{/*
function Main_(
  {loaderData,
}: Route.ComponentProps) {
  const [defaultInitParams, metaStats, currentStats, missingParams] = loaderData;
  const [initParams, setInitParams] = useState(defaultInitParams);
  async function retryCreateMorph(e) {
    const inputWidget = e.currentTarget;
    const field = inputWidget.dataset.fieldname;
    let value = inputWidget.value;
    if (inputWidget.type === "checkbox") {
      value = inputWidget.checked;
    };
    const currentInitParams = {};
    Object.entries(initParams).forEach(
      entry => {
        const [key, value] = entry;
        currentInitParams[key] = value;
      }
    );
    currentInitParams[field] = value;
    if (currentInitParams.name === "Gonzales") {
      if (!Object.keys(currentInitParams).includes("hard_mode")) {
        currentInitParams["hard_mode"] = false;
      } else if (!Object.keys(currentInitParams).includes("route")) {
        currentInitParams["route"] = "Lalum";
      } else {
        console.log("Unknown error.");
      }
    }
    await unitStatsLoader({initParams});
    axios
      .post("http://127.0.0.1:8000/dracogate/api/initialization_view/",
        {data: currentInitParams},
      )
      .then(res => {
        const data = res.data;
        const [_, clsLv, value] = data;
        const [currentCls, currentLv] = clsLv;
        setMorph({ ...currentInitParams, currentCls: currentCls, currentLv: currentLv, currentStats: value, missingParams: morph.missingParams});
      });
  }
  const imgSuffix = selectedGame.no === 8 ? "gif" : "png";
  const imgFile = `${morph.name}.${imgSuffix}`;
  const fireEmblemGames = getFireEmblemGames();
  return (
    <>
      <nav>
        <menu>
          <GameUrlList gameList={fireEmblemGames} />
        </menu>
      </nav>
      <h1>Initialization</h1>
        {selectedGame && (
          <figure>
          <img src={`/static/${selectedGame.name}/cover-art.png`} alt={`Cover art of FE${selectedGame.no}: ${selectedGame.title}`} />
          <figcaption>
            {`FE${selectedGame.no}: ${selectedGame.title}`}
          </figcaption>
        </figure>
        )
        }
      <article>
        <figure>
          <img src={`/static/${selectedGame.name}/characters/${imgFile}`} alt={`Portrait of ${morph.name}, ${imgFile}`} />
          <figcaption>
            {morph.name}
          </figcaption>
        </figure>
        <table>
          <tbody>
            <StatTable rawStats={[["Class", morph.currentCls], ["Lv", morph.currentLv]].concat(morph.currentStats)} />
          </tbody>
        </table>
      <form>
        {morph.missingParams !== null && (
          <div id="options">
            <ShowOptions optionalParams={morph.missingParams} options={options} onClick={retryCreateMorph} />
          </div>
          )
        }
        <button type="button" disabled>Create!</button>
      </form>
    </article>
    </>
  );
};
const sourceUrl = "http://127.0.0.1:8000/dracogate/api/initialization_view/";
*/}

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
    if (currentInitParams.name === "Gonzales") {
      if (!Object.keys(currentInitParams).includes("hard_mode")) {
        tempInitParams["hard_mode"] = false;
      } else if (!Object.keys(currentInitParams).includes("route")) {
        tempInitParams["route"] = "Lalum";
      } else {
        console.log("Unknown error.");
      }
    };
    setInitParams(tempInitParams);
    [metaStats, currentStats, missingParams] = await unitStatsLoader({initParams});
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
          getOptionList({missingParams, retryCreateMorph).map(option => option)
        )}
        <button>
          Create!
        </button>
      </form>
    </>
  );
};

export default Main;
