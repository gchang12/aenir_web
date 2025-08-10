import { useState } from 'react'; 
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
  father: ["Father", "select"],
  hard_mode: ["Hard Mode", "checkbox"],
  lyn_mode: ["Lyn Mode", "checkbox"],
  route: ["Route", "radio"],
  number_of_declines: ["Number of Declines", "number"],
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
  return (
    <>
      {rawStats.map(
        fieldValuePair => {
          const [stat, value] = fieldValuePair;
          return (
            <tr>
              <th>{stat}</th>
              <td>{value}</td>
            </tr>
          );
        }
      )}
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
        <StatTable rawStats={rawStats} />
      </table>
    </>
  );
}

function App() {
  const [unitList, setUnitList] = useState([]);
  const [initParams, setInitParams] = useState(
    {
      game: null,
      name: null,
    }
  );
  const [missingParams, setMissingParams] = useState(
    {
      game: null,
      name: null,
      father: null,
      hard_mode: null,
      lyn_mode: null,
      route: null,
      number_of_declines: null,
    }
  );
  const [morph, setMorph] = useState(
    {
      game: null,
      name: null,
      currentStats: null,
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
        const [success, value] = data;
        if (success) {
          setMorph({ ...initParams, currentStats: value, });
          setMissingParams(null);
        } else {
          setMissingParams(value);
        };
      }
      )
      .catch(err => console.log(err));
  };
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
            return (
              <option value={gameNo} onClick={refreshUnitList}>{title}</option>
            );
          })
          }
        </select>
        <label>Unit</label>
        <menu id="unit-selector">
          {unitList.map(unit => {
            return (
              <li>
                <button type="button" id={unit} onClick={tryCreateMorph}>
                  {unit}
                </button>
              </li>
            );
          })
          }
        </menu>
      {morph.currentStats === null ? (
        <div id="options">
        {Object.entries(missingParams).map(params => {
          const [field, choices] = params;
          const [title, inputType] = options[field];
          let inputWidget;
          switch (inputType) {
            case "select":
              inputWidget = (
                <select id={field}>
                  {choices.map(choice => {
                    <option value={choice}>choice</option>
                  })
                  }
                </select>
              );
            case "radio":
              console.log("something");
              inputWidget = {choices.map(choice => {
                  <input type={inputType} id={choice} value={choice} name={field} />
                })
              }
            case "number":
              inputWidget = (
                <input type={inputType} id={field} name={field} min="0" max={choices.length - 1} />
              );
            case "checkbox":
              inputWidget = (
                <input type={inputType} id={field} name={field} />
              );
            default:
              console.log("???");
          }
          return (
            <>
              {inputWidget}
              <label htmlFor={field}>{title}</label>
            </>
          );
        })
        }
        </div>
        ) : (
        <table>
          <StatTable rawStats={morph.currentStats} />
        </table>
        )
      }
      <button type="button" disabled>Create!</button>
      </form>
    </>
  );
};

export default App;
