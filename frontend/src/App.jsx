import { useState } from 'react'; 
import axios from 'axios';
import "./App.css";

{/* TODO: Define class for this, possibly. */}
{/* TODO: Use state for this. */}
const unit = {
  "game": {
    "name": "binding-blade",
    "title": "Sword of Seals",
    "no": 6,
  },
  "name": "Roy",
  "stats": [
    {
      "stat": "HP",
      "value": "18",
    },
    {
      "stat": "Pow",
      "value": "5",
    },
    {
      "stat": "Skl",
      "value": "5",
    },
    {
      "stat": "Spd",
      "value": "7",
    },
    {
      "stat": "Lck",
      "value": "6",
    },
    {
      "stat": "Def",
      "value": "5",
    },
    {
      "stat": "Res",
      "value": "2",
    },
  ]
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
  const [initParams, setInitParams] = useState({});
  const [missingParams, setMissingParams] = useState({});
  const [game, setGame] = useState("4");
  {/* const game = unit.game; */}
  const gameName = "genealogy-of-the-holy-war";
  const [unitList, setUnitList] = useState([]);
  const [unit, setUnit] = useState("");
  const [unitStats, setUnitStats] = useState([]);
  const [unitOptions, setUnitOptions] = useState({});
  function tryCreateMorph(e) {
    const selectedUnit = e.currentTarget.id;
    setUnit(selectedUnit);
    console.log("game: " + game);
    console.log("name: " + selectedUnit);
    axios
      .post("http://127.0.0.1:8000/dracogate/api/initialization_view/",
        {data: {game: game, name: selectedUnit}},
      )
      .then(res => {
        const data = res.data;
        if (typeof data === "object") {
          setMissingParams(data);
        } else if (typeof data === "array") {
          setUnitStats(data);
        } else {
          console.log(`data is of type: ${typeof data}`);
        }
      }
      )
      .catch(err => console.log(err));
  }
  function refreshUnitList(e) {
    {/* Set game, then load unit list */}
    const selectedGame = e.currentTarget.value;
    setGame(selectedGame);
    axios
      .get("http://127.0.0.1:8000/dracogate/api/initialization_view/",
        {params: {game: selectedGame}},
      )
      .then(res => setUnitList(res.data))
      .catch(err => console.log(err));
  }
  {/* console.log("game: " + game); */}
  {/* console.log("unit: " + unit); */}
  {/* console.log(unitList.length); */}
  return (
    <>
      <h1>Choose Your Character!</h1>
      <img src={`static/${game.name}/cover-art.png`} alt={`Cover art of FE${game.no}: ${game.title}`} />
      <form>
        <label>Game</label>
        <select id="game-selector">
          <option value="4" onClick={refreshUnitList}>Genealogy of the Holy War</option>
          <option value="5" onClick={refreshUnitList}>Thracia 776</option>
          <option value="6" onClick={refreshUnitList}>Sword of Seals</option>
          <option value="7" onClick={refreshUnitList}>Blazing Sword</option>
          <option value="8" onClick={refreshUnitList}>The Sacred Stones</option>
          <option value="9" onClick={refreshUnitList}>Path of Radiance</option>
        </select>
        <label>Unit</label>
        <menu id="unit-selector">
          {/* TODO: Gotta retrieve from Django. */}
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
        {/* NOTE: These may or may not exist. Space will be allotted for them regardless. */}
        <div id="options">
          {/* TODO: Something to do with 'unitParams' */}
          <label>Hard Mode</label>
          <input type="checkbox" name="hard-mode" />
          <label>Chapter</label>
          <input type="checkbox" name="chapter" />
          <img src={`/static/${game.name}/characters/${unit.name}.png`} alt={`Portrait of ${unit.name} from FE${game.no}`} />
        </div>
        <button type="button" disabled>Create!</button> </form>
      <table>
        <StatTable rawStats={unitStats} />
      </table>
    </>
  );
}

export default App;
