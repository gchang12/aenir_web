import {
  useState,
  useEffect,
  useContext,
} from 'react'
import {
  useLoaderData,
  useFetcher,
  useParams,
  NavLink,
  Outlet,
  Form,
  Link,
} from "react-router";

import {
  GAMES,
  UNITS,
} from "./constants";
import {
  OptionSelect,
} from "./lib/Components";
import {
  retrieveMorph,
} from "./lib/functions";

export function Root() {
  return (
    <>
    <header id="top-banner">
      <figure>
        <Link to="/">
          <img src="/logo.png" />
        </Link>
        <figcaption>
          <h1>aenir</h1>
          <h2>A Fire Emblem stats calculator and comparison tool</h2>
        </figcaption>
      </figure>
      <nav>
        <menu>
          <li><NavLink to="/create-morph/">Create</NavLink></li>
          <li><NavLink to="/morphs/">Morphs</NavLink></li>
          <li><NavLink to="/compare/">Compare</NavLink></li>
        </menu>
      </nav>
    </header>
    <main>
    <Outlet />
    </main>
    </>
  );
};

export function GameSelect() {
  return (
    <>
    <div id="create-morph">
    <nav className="create-morph">
      <menu>
      {GAMES.map(game => {
        const imgSrc = ["", "images", game.name, "cover-art.png"].join('/');
        return (
          <li key={game.no}>
            <NavLink to={["", 'create-morph', 'fe' + game.no, ''].join('/')}>
              <figure>
                <img src={imgSrc} alt={imgSrc} />
                <figcaption>
                    <h2>{"FE" + game.no}</h2>
                    <h3>{game.title}</h3>
                </figcaption>
              </figure>
            </NavLink>
          </li>
        );
      })
      }
      </menu>
    </nav>
    <Outlet />
    </div>
    </>
  );
};

export function UnitSelect() {
  const {gameId} = useParams();
  const gameName = GAMES.find(game => gameId === "fe" + game.no)?.name;
  const unitListForGame = UNITS.filter(unit => gameId === "fe" + unit.gameNo);
  const imgSuffix = gameId === "fe8" ? ".gif" : ".png";
  return (
    <>
    <nav className="create-morph">
      <menu>
      {unitListForGame.map(unit => {
        const imgSrc = ["", "images", gameName, "characters", unit.name + imgSuffix].join('/');
        return (
          <li key={unit.name}>
            <NavLink to={["", "create-morph", gameId, unit.name, ""].join("/")}>
              <figure>
                <img src={imgSrc} alt={imgSrc} />
                <figcaption>
                  <h2>{unit.name}</h2>
                  <table>
                    <tbody>
                      <tr>
                        <th>Class</th>
                        <td>{unit.class}</td>
                      </tr>
                      <tr>
                        <th>Lv</th>
                        <td>{unit.lv}</td>
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
    <Outlet />
    </>
  );
};

export function UnitConfirm() {
  // TODO: Two routes: Need extra info, and no extra info needed.
  const {data, gameId, unitName} = useLoaderData();
  const {preview, missingParams} = data;
  const imgSuffix = gameId === "fe8" ? ".gif" :".png";
  const gameName = GAMES.find(game => "fe" + game.no === gameId).name;
  const [isUpdated, setIsUpdated] = useState(true);
  const [morph, setMorph] = useState(preview);
  useEffect(() => {
    setIsUpdated(false);
    setMorph
  }, [unitName]);
  return (
    <>
    <figure>
      <img src={["", "images", gameName, "characters", unitName + imgSuffix].join("/")} />
      <figcaption>
        <h1>{unitName}</h1>
        <table>
          <tbody>
            <tr>
              <th>Class</th>
              <td>{preview == null ? "???" : preview.unitClass}</td>
            </tr>
            <tr>
              <th>Level</th>
              <td>{preview == null ? "? / ?" : preview.level[0] + " / " + preview.level[1]}</td>
            </tr>
          </tbody>
        </table>
      </figcaption>
    </figure>
    <form onChange={() => setIsUpdated(isUpdated)}>
      <OptionSelect {...{missingParams}} />
      <button onClick={e => console.log(e.currentTarget)} disabled={isUpdated} type="button">Preview</button>
      <button type="submit">Create</button>
    </form>
    <table>
      <tbody>
        <>
        {preview == null || preview.stats.map(statBundle => {
          const [stat, currentVal, localMax, absMax] = statBundle;
          return (
            <tr key={stat} className={currentVal === localMax ? "maxed-stat" : undefined}>
              <th>{stat}</th>
              <td>{currentVal}</td>
              <td>
                <meter min="0" max={absMax} value={currentVal} optimum={localMax}></meter>
              </td>
            </tr>
          );
        })
        }
        </>
      </tbody>
    </table>
    </>
  );
};

/* TODO
- Insert button to preview.
- Disable submit-button 'til the stats are clean.
- Hide stats for units who need more parameters.
*/

