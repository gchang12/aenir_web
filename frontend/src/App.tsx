import { useState } from 'react'
import {
  useLoaderData,
  NavLink,
  useParams,
} from "react-router";
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

import {
  GAMES,
} from "./constants/GAMES";
import {
  UNITS,
} from "./constants/UNITS";

function App() {
  const [count, setCount] = useState(0)
  return (
    <>
    {/* <img src="/public/images/binding-blade/cover-art.png" /> */}
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

export { App };

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
  const {missingParams} = morph;
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
  return {morph, missingParams};
};

export {
  getMorph,
  previewMorph,
};

function ProfileHead({figureTitle, imgSrc, children}) {
  return (
    <>
    <figure>
      <img src={imgSrc} alt={imgSrc} />
      <figcaption>
        <h2>{figureTitle}</h2>
        <div className="ProfileHead-children">{children}</div>
      </figcaption>
    </figure>
    </>
  );
};

function ProfileLevelAndClass({unitClass, level}) {
  const [currentLv, maxLv] = level;
  return (
    <>
    <tr>
      <th>Class</th>
      <td>{unitClass}</td>
    </tr>
    <tr>
      <th>Lv</th>
      <td>{currentLv} / {maxLv}</td>
    </tr>
    </>
  );
};

function StatTable({stats, highlight}) {
  const className = highlight === true ? "maxed-stat" : undefined;
  return (
    <>
    {stats.map(([stat, currentValue, localMax, absMax]) => {
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

function UnitConfirm() {
  const loaderData = useLoaderData();
  const {morph, missingParams, unitName, gameId} = loaderData;
  const {stats, unitClass, level} = morph;
  const imgSuffix = gameId === "fe8" ? ".gif" : ".png";
  return (
    <>
    <form>
      <ProfileHead figureTitle={unitName} imgSrc={"/images/" + unitName + imgSuffix}>
        <table>
          <tbody>
          <ProfileLevelAndClass {...{unitClass, level}} />
          {/* OptionSelect */}
          </tbody>
        </table>
      </ProfileHead>
      <table>
        <tbody>
        <StatTable {...{stats, highlight: true}} />
        </tbody>
      </table>
      <button>Create!</button>
    </form>
    </>
  );
};

export {
  UnitConfirm,
  StatTable,
};

function GameSelect() {
  return (
    <nav>
      <menu>
      {GAMES.map(game => {
        return (
          <li key={game.no}>
            <NavLink to={["", 'create-morph', 'fe' + game.no, ''].join('/')}>
              <figure>
                <img src={["", "images", game.name, "cover-art.png"].join('/')} />
                <figcaption>
                  <table>
                    <tbody>
                      <tr>
                        <th>Game ID</th>
                        <td>{"FE" + game.no}</td>
                      </tr>
                      <tr>
                        <th>Title</th>
                        <td>{game.title}</td>
                      </tr>
                      <tr>
                        <th>Released</th>
                        <td>{game.released}</td>
                      </tr>
                    </tbody>
                  </table>
                </figcaption>
              </figure>
            </NavLink>
          </li>
        );
      })
      }
      </menu>
    </nav>
  );
};

function UnitSelect() {
  const {gameId} = useParams();
  const gameName = GAMES.find(game => gameId === "fe" + game.no)?.name;
  const unitListForGame = UNITS.filter(unit => gameId === "fe" + unit.gameNo);
  const imgSuffix = gameId === "fe8" ? ".gif" : ".png";
  return (
    <nav>
      <menu>
      {unitListForGame.map(unit => {
        const imgSrc = ["", "public/images", gameName, "characters", unit.name + imgSuffix].join('/');
        return (
          <li key={unit.name}>
            <NavLink to={["", "create-morph", gameName, unit.name, ""].join("/")}>
              <figure>
                <img src={imgSrc} alt={imgSrc} />
                <figcaption>
                  <table>
                    <tbody>
                      <tr>
                        <th>Name</th>
                        <td>{unit.name}</td>
                      </tr>
                      <tr>
                        <th>Lv</th>
                        <td>{unit.lv}</td>
                      </tr>
                      <tr>
                        <th>Class</th>
                        <td>{unit.class}</td>
                      </tr>
                    </tbody>
                  </table>
                </figcaption>
              </figure>
            </NavLink>
          </li>
        );
      })
      }
      </menu>
    </nav>
  );
};

function UnitConfirm2() {
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

function CreateMorph({section1, section2, section3}) {
  return (
    <>
    <div className="create-morph">
    {section1}
    </div>
    <div className="create-morph">
    {section2}
    </div>
    <div className="create-morph">
    {section3}
    </div>
    </>
  );
};

export {
  GameSelect,
  UnitSelect,
  //UnitConfirm,
};

