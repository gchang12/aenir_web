import { useState, Fragment } from 'react'; 
import {
  redirect,
} from 'react-router';
{/* import { */}
  {/* useNavigate, */}
  {/* } from 'react-router-dom'; */}
import type { Route } from "./+types/home";

import axios from 'axios';

import "../../../app.css";
import {
  unitStatsLoader,
  newUnitSaver,
} from '../../../_dataLoaders/morphs/new.tsx';
import {
  GameUrlList,
  GameProfile,
  UnitProfile,
  UnitUrlList,
  StatTable,
  MorphOption1,
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

export async function loader( { params }: Route.LoaderArgs) {
  const game = findFireEmblemGame({params});
  const unit = params.unit;
  const initParams = {
    game: game.no,
    name: unit,
  };
  let [metaStats, currentStats, missingParams] = await unitStatsLoader({initParams});
  if (missingParams !== null) {
    const [field, choices] = missingParams;
    const defaultVal = choices[0];
    initParams[field] = defaultVal;
    let _;
    [metaStats, currentStats, _] = await unitStatsLoader({initParams});
  };
  return [game, initParams, metaStats, currentStats, missingParams];
};

function Main(
  {loaderData,
}: Route.ComponentProps) {
  const [game, defaultInitParams, defaultMetaStats, defaultCurrentStats, missingParams] = loaderData;
  const [initParams, setInitParams] = useState(defaultInitParams);
  const [metaStats, setMetaStats] = useState(defaultMetaStats);
  const [currentStats, setCurrentStats] = useState(defaultCurrentStats);
  const fireEmblemGames = getFireEmblemGames();
  async function retryCreateMorph(e) {
    const inputWidget = e.currentTarget;
    const field = inputWidget.dataset.fieldname;
    let value = inputWidget.value;
    if (inputWidget.type === "checkbox") {
      value = inputWidget.checked;
    } else if (field === "father") {
      const fatherName = inputWidget.value;
      const fatherPreview = document.getElementById("father-preview");
      const fatherImgSrc = `/static/genealogy-of-the-holy-war/characters/${fatherName}.png`;
      fatherPreview.src = fatherImgSrc;
      fatherPreview.alt = fatherImgSrc;
    };
    let tempInitParams = {...initParams};
    tempInitParams[field] = value;
    let tempMetaStats;
    let tempCurrentStats;
    let _;
    unitStatsLoader({initParams: tempInitParams})
      .then(res => {
          [tempMetaStats, tempCurrentStats, _] = res;
          setInitParams(tempInitParams);
          setMetaStats(tempMetaStats);
          setCurrentStats(tempCurrentStats);
        }
      )
      .catch(err => console.log(err));
  };
  function decideWhetherOrNotToActivateButton(e) {
    const morphSubmitButton = document.getElementById("morph-name-input");
    const newMorphName = e.currentTarget.value;
    morphSubmitButton.disabled = newMorphName === "";
    {/* setMorphName(newMorphName); */}
  };
  {/* const navigate = useNavigate(); */}
  async function saveMorph(e) {
    // send init-data to server
    {/* async function newUnitSaver( {initParams, showError} ) { */}
    alert("saveMorph");
    {/* navigate('/morph/'); */}
    function showError(e) {
      const initErrors = document.getElementById("init-errors");
      initErrors.textContent = e;
    };
    return await newUnitSaver({initParams, showError});
  };
  return (
    <>
      <nav id="game-select">
        <menu>
          <GameUrlList gameList={fireEmblemGames} />
        </menu>
      </nav>
      <UnitProfile game={game} unit={initParams.name} />
      <StatTable stats={[["Class", metaStats.currentCls], ["Lv", metaStats.currentLv]].concat(currentStats)} />
      {/* NOTE: This form.action is just a placeholder. */}
      <form action="/morphs">
        {missingParams !== null && <MorphOption1 params={missingParams} onClick={retryCreateMorph} />}
        {/* <input id="morph-name-input" type="text" required onClick={decideWhetherOrNotToActivateButton} /> */}
        <button id="morph-submit-button" type="button" onClick={saveMorph}>
          Create!
        </button>
        <a href="/morphs" onClick={saveMorph}>
          Create via Link!
        </a>
        <div id="init-errors">
        </div>
      </form>
    </>
  );
};

export default Main;
