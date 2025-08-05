import "./App.css";

const game = {
  "name": "binding-blade",
  "title": "Sword of Seals",
  "no": 6,
};
const unit = {
  "name": "Roy",
};

function App() {
  return (
    <div id="init">
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
      {/* TODO: Loop over the thing and display. values in unit, fields in game */}
        <tr>
          <th>HP</th>
          <td>18</td>
        </tr>
        <tr>
          <th>Pow</th>
          <td>5</td>
        </tr>
        <tr>
          <th>Skl</th>
          <td>5</td>
        </tr>
        <tr>
          <th>Spd</th>
          <td>7</td>
        </tr>
        <tr>
          <th>Lck</th>
          <td>8</td>
        </tr>
        <tr>
          <th>Def</th>
          <td>6</td>
        </tr>
        <tr>
          <th>Res</th>
          <td>3</td>
        </tr>
        <tr>
          <th>Con</th>
          <td>7</td>
        </tr>
        <tr>
          <th>Mov</th>
          <td>5</td>
        </tr>
      </table>
    </div>
  );
}

export default App;
