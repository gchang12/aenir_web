import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <div>
        <a href="https://vite.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <p>
          Edit <code>src/App.tsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
    </>
  )
}

export default App

// MY CODE

import axios from 'axios';

function getMorph(game_no, name, kwargs) {
  const RESOURCE_URL: string = "http://localhost:8000/dracogate/api/morphs/";
  const params = {
    game_no,
    name,
    ...kwargs,
  };
  const fetchTask = axios
    .get(RESOURCE_URL, {params})
    .then(resp => resp.data)
    .catch(err => console.log(err));
  return fetchTask;
};

async function previewMorph(game_no, name, kwargs) {
  let morph = await getMorph(game_no, name, {});
  const { missingParams } = morph;
  if (typeof missingParams === 'object') {
    const newKwargs = {};
    Object.entries(missingParams).forEach(([key, values]) => {
      // const [key, values] = entry;
      const [defaultVal] = values;
      newKwargs[key] = defaultVal;
    });
    Object.entries(kwargs).forEach(([key, value]) => {
      // const [key, value] = entry;
      newKwargs[key] = value;
    });
    morph = await getMorph(game_no, name, newKwargs);
  };
  return { morph, missingParams };
};

export {
  getMorph,
  previewMorph,
};

function StatTable({stats, highlight}) {
  return (
    <>
    {stats.map(([stat, currentValue, localMax, absMax]) => {
      const className = highlight === true ? "maxed-stat" : undefined;
      return (
        <tr key={stat} className={currentValue === localMax ? className : undefined}>
          <td>{currentValue}</td>
          <td>
            <meter min="0" value={currentValue} max={absMax} high={localMax}></meter>
          </td>
        </tr>
      );
    })
    }
    </>
  );
};

function GameSelect() {
  return (
    <nav>
      <menu>
        <li>
          <Link>
            <figure>
              <figcaption>Game Name</figcaption>
              <img src="" />
              gameId
              title
              releaseDate
            </figure>
          </Link>
        </li>
      </menu>
    </nav>
  );
};

function UnitSelect() {
  return (
    <nav>
      <menu>
        <li>
          <Link>
            <figure>
              <img src="" />
              <figcaption>Unit Name</figcaption>
            </figure>
            <table>
              <tbody>
                <tr>
                  <th>Lv</th>
                  <td>0</td>
                </tr>
                <tr>
                  <th>Class</th>
                  <td></td>
                </tr>
              </tbody>
            </table>
          </Link>
        </li>
      </menu>
    </nav>
  );
};

function UnitConfirm() {
  return (
    <form>
      <div>
        <h1>Game Name</h1>
        <figure>
          <img src="" />
          <figcaption>Unit Name</figcaption>
        </figure>
        <table>
          <tbody>
            <tr>
              <th>Lv</th>
              <td>0</td>
            </tr>
            <tr>
              <th>Class</th>
              <td></td>
            </tr>
            <tr>
              <th>Option</th>
              <td>Widget</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div>
        <table>
          <tbody>
            <tr>Stat-Name</tr>
            <td>Stat-Value</td>
          </tbody>
        </table>
      </div>
      <button>Create</button>
    </form>
  );
};

export {
  GameSelect,
  UnitSelect,
  UnitConfirm,
};

