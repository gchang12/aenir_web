import logo from './logo.svg';
import './App.css';

function App() {
  return (
    <>
      <img src="./box-art.png" alt="box art of FE#: Subtitle here" />
      <select id='game-selector'>
        <option value="4">Genealogy of the Holy War</option>
        <option value="5">Thracia 776</option>
        <option value="6">Sword of Seals</option>
        <option value="7">Blazing Sword</option>
        <option value="8">The Sacred Stones</option>
        <option value="9">Path of Radiance</option>
      </select>
      <select id='unit-selector'>
        <option value='Roy'>Roy</option>
        <option value='Marth'>Marth</option>
      </select>
      <input type='checkbox' />
      <input type='checkbox' />
      <img src="./portrait.png" />
      <button type="button">Create!</button>
      <table>
        <tr>
          <th>HP</th>
          <td>30</td>
        </tr>
      </table>
    </>
  );
}

export default App;
