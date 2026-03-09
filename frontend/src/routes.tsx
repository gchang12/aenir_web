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
  CurrentStatsTable,
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
        const unitName = unit.name;
        return (
          <li key={unitName}>
            <NavLink to={["", "create-morph", gameId, unitName, ""].join("/")}>
              <ProfileIcon {...{gameId, unitName: unitName}} />
              <ClassLevelInfo morph={unit} />
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


/* TODO
- Insert button to preview.
- Disable submit-button 'til the stats are clean.
- Hide stats for units who need more parameters.
*/

export function UnitConfirm() {
  const {data, gameId, unitName} = useLoaderData();
  const {preview, missingParams} = data;
  return (
    <div id="UnitConfirm">
      <ProfileIcon {...{gameId, unitName}} />
      <ClassLevelInfo {...{morph}} />
      <OptionsMenu {...{disabled, onClick, morph}} />
      <></>
      <CurrentStatsTable {...{morph}} />
      <ConfirmationMenu {...{message, disabled}} />
    </div>
    </>
  ); */}
};
