import {
  useState,
  useEffect,
  useContext,
  useCallback,
  useRef,
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
  ProfileIcon,
  ClassLevelInfo,
  ConfirmationMenu,
} from "./lib/Components";
import {
  getMorph,
} from "./lib/functions";

export function Root() {
  return (
    <>
    <header>
      <Link to="/">
        <img src="/logo.png" width="300" />
      </Link>
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
      <nav id="GameSelect">
        <menu>
        {GAMES.map(game => {
          const imgSrc = ["", "images", game.name, "cover-art.png"].join('/');
          return (
            <li key={game.no}>
              <NavLink to={["", 'create-morph', 'fe' + game.no, ''].join('/')}>
                <figure>
                  <img src={imgSrc} alt={imgSrc} height="100" />
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
    <nav id="UnitSelect">
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
  const morph = preview;
  const [previewMode, setPreviewMode] = useState(false);
  const fetcher = useFetcher();
  const formRef = useRef(null);
  useEffect(() => {
    setPreviewMode(missingParams != null);
  }, [unitName]);
  const refetchMorph = useCallback((e) => {
    setPreviewMode(false);
    const game_no = Number(gameId.replace("fe", ""));
    const name = unitName;
    // TODO: populate this with form data.
    const options = {};
    // TODO: fetcher.load(`/create-morph/${gameId}/${unitName}/?`./?searchParam1=k&sesarchParam2=...)
  }, [unitName]);
  const message = previewMode ? `Please provide extra parameters for ${unitName}.` : "Please confirm the selection.";
  return (
    <div id="UnitConfirm">
      <ProfileIcon {...{gameId, unitName}} />
      <ClassLevelInfo {...{morph}} />
      <fetcher.Form onChange={() => setPreviewMode(true)} ref={formRef}>
        <ConfirmationMenu onClick={refetchMorph} {...{message, disabled: previewMode}}>
          <OptionSelect {...{missingParams}} />
        </ConfirmationMenu>
      </fetcher.Form>
      {/* */}
      <CurrentStatsTable {...{morph}} />
    </div>
  );
s};
