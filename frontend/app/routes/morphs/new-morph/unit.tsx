import { useState, Fragment } from 'react'; 
import { unitListLoader } from './game.tsx';
import axios from 'axios';
import "../../../app.css";

import type { Route } from "./+types/home";
{/* import { Welcome } from "../welcome/welcome"; */}

import UnitSelectMenu from './game.tsx';

export function meta({}: Route.MetaArgs) {
  return [
    { title: "Aenir: A Fire Emblem stat calculator" },
    { name: "description", content: "Calculate Fire Emblem stats here!" },
  ];
}

function StatTable( { rawStats } ) {
  console.log("Hello from 'StatTable'!");
  return (
    <>
    {Object.values(rawStats).map(fieldValuePair => {
      const [stat, value] = fieldValuePair;
      return (
        <tr key={stat}>
          <th>{stat}</th>
          <td>{value}</td>
        </tr>
      );
    })
    }
    </>
  );
}

const options = {
  father: ["Father", "select"],
  hard_mode: ["Hard Mode", "checkbox"],
  lyn_mode: ["Lyn Mode", "checkbox"],
  route: ["Route", "radio"],
  number_of_declines: ["Number of Declines", "number"],
};

export async function statLoader( {initParams} ) {
  let missingParams = null;
  const tempInitParams = { ...initParams};
  let currentCls, currentLv;
  let currentStats;
  await axios
    .post("http://127.0.0.1:8000/dracogate/api/initialization_view/",
      {data: initParams},
    )
    .then(res => {
      const data = res.data;
      const [success, clsLv, value] = data;
      if (success) {
        currentStats = value;
        [currentCls, currentLv] = clsLv;
      } else {
        missingParams = value;
      }
    })
    .catch(err => console.log(err));
  if (missingParams !== null) {
    for (const item of Object.entries(missingParams)) {
      const [field, choices] = item;
      const defaultVal = choices[0];
      tempInitParams[field] = defaultVal;
    };
    await axios
      .post("http://127.0.0.1:8000/dracogate/api/initialization_view/",
        {data: tempInitParams},
      )
      .then(res => {
        const data = res.data;
        const [_, clsLv, value] = data;
        [currentCls, currentLv] = clsLv;
        currentStats = value;
      })
      .catch(err => console.log(err));
  }
  return [tempInitParams, missingParams, currentCls, currentLv, currentStats];
}

function ShowOptions({optionalParams, options, onClick}) {
  const optionsToBeShown = [];
  let key = 0;
  Object.entries(optionalParams).forEach(params => {
    const [field, choices] = params;
    const [title, inputType] = options[field];
    const inputWidget = {
      "select": (
        <>
          <label htmlFor={field}>{title}</label>
          <select id={field}>
            {choices.map(choice => {
              return (
                <option key={choice} data-fieldname={field} value={choice} onClick={onClick}>{choice}</option>
              );}
            )
            }
          </select>
        </>
      ),
      "radio": (
          <fieldset>
          <legend>Route</legend>
          {choices.map(choice => {
            return (
              <>
                <label htmlFor={field}>{choice}</label>
                <input type={inputType} id={choice} value={choice} name={field} data-fieldname={field} onClick={onClick} />
              </>
            );
          })}
        </fieldset>
      ),
      "number": (
        <>
          <label htmlFor={field}>{title}</label>
          <input type={inputType} id={field} name={field} min="0" max={choices.length - 1} data-fieldname={field} onClick={onClick} />
        </>
      ),
      "checkbox": (
        <>
          <label htmlFor={field}>{title}</label>
          <input type={inputType} id={field} name={field} data-fieldname={field} onClick={onClick} />
        </>
      ),
    }[inputType]
    optionsToBeShown.push(
      <Fragment key={key}>
        {inputWidget}
      </Fragment>
    );
    key += 1;
  });
  return optionsToBeShown;
};

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
