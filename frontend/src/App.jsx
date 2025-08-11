import { useState, Fragment } from 'react'; 
import axios from 'axios';
import "./App.css";

const fireEmblemGames = {
  4: {
    no: 4,
    name: "genealogy-of-the-holy-war",
    title: "Genealogy of the Holy War",
  },
  5: {
    no: 5,
    name: "thracia-776",
    title: "Thracia 776",
  },
  6: {
    no: 6,
    name: "binding-blade",
    title: "The Sword of Seals",
  },
  7: {
    no: 7,
    name: "blazing-sword",
    title: "The Blazing Blade",
  },
  8: {
    no: 8,
    name: "the-sacred-stones",
    title: "The Sacred Stones",
  },
  9: {
    no: 9,
    name: "path-of-radiance",
    title: "Path of Radiance",
  },
};
const options = {
  father: ["Father", "select", "Arden"],
  hard_mode: ["Hard Mode", "checkbox", false],
  lyn_mode: ["Lyn Mode", "checkbox", true],
  route: ["Route", "radio", "Lalum"],
  number_of_declines: ["Number of Declines", "number", 0],
};
const fe4Units = [
  'Sigurd',
  'Noish',
  'Alec',
  'Arden',
  'Cuan',
  'Ethlin',
  'Fin',
  'Lex',
  'Azel',
  'Midayle',
  'Adean',
  'Dew',
  'Ira',
  'Diadora',
  'Jamka',
  'Holyn',
  'Lachesis',
  'Levin',
  'Sylvia',
  'Fury',
  'Beowolf',
  'Briggid',
  'Claude',
  'Tiltyu',
  'Mana',
  'Radney',
  'Roddlevan',
  'Oifey',
  'Tristan',
  'Dimna',
  'Yuria',
  'Femina',
  'Amid',
  'Johan',
  'Johalva',
  'Shanan',
  'Daisy',
  'Janne',
  'Aless',
  'Laylea',
  'Linda',
  'Asaello',
  'Hawk',
  'Hannibal',
  'Sharlow',
  'Celice',
  'Leaf',
  'Altenna',
  'Rana',
  'Lakche',
  'Skasaher',
  'Delmud',
  'Lester',
  'Fee',
  'Arthur',
  'Patty',
  'Nanna',
  'Leen',
  'Tinny',
  'Faval',
  'Sety',
  'Corpul',
];

function ShowOptions({optionalParams, options, onClick}) {
  const optionsToBeShown = [];
  let key = 0;
  {/* alert("optionalParams: " + optionalParams); */}
  {/* alert("options: " + options); */}
  {/* alert("onClick: " + onClick); */}
  Object.entries(optionalParams).forEach(params => {
    const [field, choices] = params;
    const [title, inputType, _] = options[field];
    let inputWidget;
    {/* alert(choices[0]); */}
    switch (inputType) {
      case "select":
        inputWidget = (
          <select id={field}>
            {choices.map(choice => {
              return (
                <option key={choice} data-fieldname={field} value={choice} onClick={onClick}>{choice}</option>
              );}
            )
            }
          </select>
        );
        break;
      case "radio":
        inputWidget = choices.map(choice => {
          return (
            <>
              <label htmlFor={field}>{choice}</label>
              <input type={inputType} id={choice} value={choice} name={field} data-fieldname={field} onClick={onClick} />
            </>
          );
          }
        )
        ;
        break;
      case "number":
        inputWidget = (
          <input type={inputType} id={field} name={field} min="0" max={choices.length - 1} data-fieldname={field} onClick={onClick} />
        );
        break;
      case "checkbox":
        inputWidget = (
          <input type={inputType} id={field} name={field} data-fieldname={field} onClick={onClick} />
        );
        break;
      default:
        console.log("???");
        {/* alert("???"); */}
        break;
    }
    optionsToBeShown.push(
      <Fragment key={key}>
        <label htmlFor={field}>{title}</label>
        {inputWidget}
      </Fragment>
    );
    key += 1;
  });
  return optionsToBeShown;
};

function Portrait() {
  return (
    <figure>
    <img />
    <figcaption>
    </figcaption>
    </figure>
  );
}

function StatTable( { rawStats } ) {
  console.log("Hello from 'StatTable'!");
  {/* alert(rawStats); */}
  return (
    <>
    {Object.values(rawStats).map(
      fieldValuePair => {
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

function StatProfile( { profileBlock, detailsBlock, rawStats } ) {
  return (
    <>
      <div className="personal">
        {profileBlock}
        {detailsBlock}
      </div>
      <table>
        <tbody>
          <StatTable rawStats={rawStats} />
        </tbody>
      </table>
    </>
  );
}

function App() {
  const [unitList, setUnitList] = useState(fe4Units);
  const [initParams, setInitParams] = useState(
    {
      game: 4,
      name: null,
    }
  );
  const [morph, setMorph] = useState(
    {
      game: null,
      name: null,
      currentCls: null,
      currentLv: null,
      currentStats: null,
      missingParams: null,
    }
  );
  function refreshUnitList(e) {
    {/* Set game, then load unit list */}
    const selectedGame = e.currentTarget.value;
    setInitParams( { ...initParams, game: selectedGame, });
    axios
      .get("http://127.0.0.1:8000/dracogate/api/initialization_view/",
        {params: {game: selectedGame}},
      )
      .then(res => setUnitList(res.data))
      .catch(err => console.log(err));
    setMorph({...morph, missingParams: null, currentStats: null});
  };
  function tryCreateMorph(e) {
    const selectedUnit = e.currentTarget.id;
    setInitParams( { ...initParams, name: selectedUnit, });
    axios
      .post("http://127.0.0.1:8000/dracogate/api/initialization_view/",
        {data: {game: initParams.game, name: selectedUnit}},
      )
      .then(res => {
        const data = res.data;
        const [success, clsLv, value] = data;
        if (success) {
          const [currentCls, currentLv] = clsLv;
          setMorph({ ...initParams, currentCls: currentCls, currentLv: currentLv, currentStats: value, missingParams: null});
        } else {
          const missingParams = value;
          const tempInitParams = { ...initParams, name: selectedUnit};
          for (const field of Object.keys(missingParams)) {
            const [_, __, defaultVal] = options[field];
            tempInitParams[field] = defaultVal;
          };
          axios
            .post("http://127.0.0.1:8000/dracogate/api/initialization_view/",
              {data: tempInitParams},
            )
            .then(res => {
              const data = res.data;
              const [_, clsLv, value] = data;
              const [currentCls, currentLv] = clsLv;
              setMorph({ ...tempInitParams, currentStats: value, currentCls: currentCls, currentLv: currentLv, missingParams: missingParams});
            })
            .catch(err => console.log(err));
        }
      }
      )
      .catch(err => console.log(err));
  };
  function retryCreateMorph(e) {
    const inputWidget = e.currentTarget;
    const field = inputWidget.dataset.fieldname;
    let value = inputWidget.value;
    {/* alert(inputWidget.type); */}
    {/* alert(value); */}
    if (inputWidget.type === "checkbox") {
      value = inputWidget.checked;
    };
    {/* alert(field); */}
    {/* alert(value); */}
    const currentInitParams = {};
    Object.entries(initParams).forEach(
      entry => {
        const [key, value] = entry;
        currentInitParams[key] = value;
      }
    );
    currentInitParams[field] = value;
    {/* alert("aftetr copying"); */}
    if (currentInitParams.name === "Gonzales") {
      if (!Object.keys(currentInitParams).includes("hard_mode")) {
        currentInitParams["hard_mode"] = false;
      } else if (!Object.keys(currentInitParams).includes("route")) {
        currentInitParams["route"] = "Lalum";
      } else {
        console.log("Unknown error.");
      }
    }
    {/* alert("after gonzy exceptions"); */}
    axios
      .post("http://127.0.0.1:8000/dracogate/api/initialization_view/",
        {data: currentInitParams},
      )
      .then(res => {
        const data = res.data;
        const [success, clsLv, value] = data;
        const [currentCls, currentLv] = clsLv;
        setMorph({ ...currentInitParams, currentCls: currentCls, currentLv: currentLv, currentStats: value, missingParams: morph.missingParams});
      });
    {/* alert("after data retrieval"); */}
  }
  const selectedGame = fireEmblemGames[initParams.game];
  return (
    <>
      <h1>Choose Your Character!</h1>
        {selectedGame && (
          <figure>
          <img src={`static/${selectedGame.name}/cover-art.png`} alt={`Cover art of FE${selectedGame.no}: ${selectedGame.title}`} />
          <figcaption>
            {`Official cover-art for FE${selectedGame.no}: ${selectedGame.title}`}
          </figcaption>
        </figure>
        )
        }
      <form>
        <label>Game</label>
        <select id="game-selector">
          {Object.entries(fireEmblemGames).map(fireEmblemGame => {
            const [gameNo, game] = fireEmblemGame;
            const title = game.title;
            const name = game.name;
            return (
              <option key={name} value={gameNo} onClick={refreshUnitList}>{title}</option>
            );
          })
          }
        </select>
        <label>Unit</label>
        <menu id="unit-selector">
          {unitList.map(unit => {
            return (
              <li key={unit}>
                <button type="button" id={unit} onClick={tryCreateMorph}>
                  {unit}
                </button>
              </li>
            );
          })
          }
        </menu>
      {morph.missingParams !== null && (
        <div id="options">
          <ShowOptions optionalParams={morph.missingParams} options={options} onClick={retryCreateMorph} />
        </div>
        )
      }
      <button type="button" disabled>Create!</button>
      </form>
      {morph.currentStats !== null && (
        <table>
          <tbody>
            <StatTable rawStats={[["Class", morph.currentCls], ["Lv", morph.currentLv]].concat(morph.currentStats)} />
          </tbody>
        </table>
        )
      }
    </>
  );
};

export default App;
