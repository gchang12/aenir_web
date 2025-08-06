import "./App.css";

const unit = {
  "game": {
    "name": "binding-blade",
    "title": "Sword of Seals",
    "no": 6,
  },
  "name": "Roy",
  {/* TODO: Define class for this, possibly. */}
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

function StatTable( { rawStats } ) {
  return (
    <>
      {rawStats.map(
        fieldValuePair => {
          const stat = fieldValuePair.stat;
          const value = fieldValuePair.value;
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
        <StatArray rawStats={rawStats} />
      </table>
    </>
  );
}

function App() {
  const game = unit.game;
  return (
    <>
      <h1>Choose Your Character!</h1>
      <img src={`static/${game.name}/cover-art.png`} alt={`Cover art of FE${game.no}: ${game.title}`} />
      <form>
        <label>Game</label>
        <select id="game-selector">
          <option value="4">Genealogy of the Holy War</option>
          <option value="5">Thracia 776</option>
          <option value="6">Sword of Seals</option>
          <option value="7">Blazing Sword</option>
          <option value="8">The Sacred Stones</option>
          <option value="9">Path of Radiance</option>
        </select>
        <label>Unit</label>
        <select id="unit-selector" disabled>
          <option value="Roy">Roy</option>
          <option value="Marth">Marth</option>
        </select>
        {/* NOTE: These may or may not exist. Space will be allotted for them regardless. */}
        <div id="options">
          <label>Hard Mode</label>
          <input type="checkbox" name="hard-mode" />
          <label>Chapter</label>
          <input type="checkbox" name="chapter" />
          <img src={`/static/${game.name}/characters/${unit.name}.png`} alt={`Portrait of ${unit.name} from FE${game.no}`} />
        </div>
        <button type="button" disabled>Create!</button> </form>
      <table>
        <StatTable rawStats={unit.stats} />
      </table>
    </>
  );
}

export default App;
