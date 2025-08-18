import { useState, Fragment } from 'react'; 
import { unitListLoader } from './GameSelect.tsx';
import axios from 'axios';
import "../../../app.css";

import type { Route } from "./+types/home";
{/* import { Welcome } from "../welcome/welcome"; */}

import UnitSelectMenu from './GameSelect.tsx';

export function meta({}: Route.MetaArgs) {
  return [
    { title: "Aenir: A Fire Emblem stat calculator" },
    { name: "description", content: "Calculate Fire Emblem stats here!" },
  ];
}


export async function loader( { params }: Route.LoaderArgs) {
  const rawGame = params.game;
  const gameNo = {
    "fe4": 4,
    "fe5": 5,
    "fe6": 6,
    "fe7": 7,
    "fe8": 8,
    "fe9": 9,
  }[rawGame];
  const unitList = await unitListLoader({rawGame, gameNo});
  const unit = params.unit;
  const initParams = {
    game: gameNo,
    name: unit,
  };
  const [tempInitParams, missingParams, currentCls, currentLv, currentStats] = await statLoader({initParams});
  return [tempInitParams, missingParams, currentCls, currentLv, currentStats, rawGame];
};

function UnitConfirmMenu(
  {loaderData,
}: Route.ComponentProps) {
  const [tempInitParams, missingParams, currentCls, currentLv, currentStats, rawGame] = loaderData;
  const [morph, setMorph] = useState(
    {
      game: tempInitParams.game,
      name: tempInitParams.name,
      currentCls: currentCls,
      currentLv: currentLv,
      currentStats: currentStats,
      missingParams: missingParams,
    }
  );
  const [initParams, setInitParams] = useState(tempInitParams);
  function tryCreateMorph(e) {
    setInitParams({...initParams});
  };
  function retryCreateMorph(e) {
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
  const selectedGame = {
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
  }[rawGame];
  const imgSuffix = selectedGame.no === 8 ? "gif" : "png";
  const imgFile = `${morph.name}.${imgSuffix}`;
  return (
    <>
    {/* <UnitSelectMenu /> */}
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

export default UnitConfirmMenu;

  const sourceUrl = "http://127.0.0.1:8000/dracogate/api/initialization_view/";
  await function retryCreateMorph(e) {
    const inputWidget = e.currentTarget;
    const field = inputWidget.dataset.fieldname;
    let value = inputWidget.value;
    if (inputWidget.type === "checkbox") {
      value = inputWidget.checked;
    };
    initParams[field] = value;
    if (currentInitParams.name === "Gonzales") {
      if (!Object.keys(currentInitParams).includes("hard_mode")) {
        currentInitParams["hard_mode"] = false;
      } else if (!Object.keys(currentInitParams).includes("route")) {
        currentInitParams["route"] = "Lalum";
      } else {
        console.log("Unknown error.");
      }
    };
    const [metaStats, currentStats, missingParams] = unitStatsLoader({initParams});
    await axios
      .post(sourceUrl,
        {data: initParams},
      )
      .then(res => {
        const data = res.data;
        const [_, clsLv, value] = data;
        const [currentCls, currentLv] = clsLv;
      })
      .catch(err => console.log(err));
  }
