import {
  useState,
  useEffect,
  useContext,
  useCallback,
  useRef,
} from 'react'
import {
  useLoaderData,
  // NOTE: https://github.com/remix-run/react-router/issues/11184
  // fetcher.data does not work.
  //useFetcher,
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
  MorphMethodSelect,
  OptionSelect,
  CurrentStatsTable,
  BlankStatsTable,
  GrowthsStatsTable,
  ProfileIcon,
  ClassLevelInfo,
  BlankClassLevelInfo,
  ConfirmationMenu,
  UnitHub,
} from "./lib/Components";
import {
  getMorph,
  getLocalMorphs,
  setLocalMorphs,
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
              <ProfileIcon {...{gameId, unitName}}>
              {unitName}
              </ProfileIcon>
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


export function UnitConfirm() {
  {/* const [morphId, setMorphId] = useState(""); */}
  const {gameId, unitName} = useParams();
  const {morph} = useLoaderData();
  const [preview, setPreview] = useState(morph.preview);
  const [previewMode, setPreviewMode] = useState(false);
  const formRef = useRef(null);
  useEffect(() => {
    setPreviewMode(morph.missingParams != null);
    setPreview(morph.preview);
  }, [unitName]);
  const refetchMorph = useCallback(() => {
    const game_no = Number(gameId.replace("fe", ""));
    const name = unitName;
    const options = {};
    const formData = new FormData(formRef.current);
    for (const [key, value] of formData.entries()) {
      options[key] = value;
    };
    console.log(`getMorph(${game_no}, ${name}, ${Object.entries(options)})`);
    getMorph(game_no, name, options)
      .then(morph => {
        console.log("morph:", Object.entries(morph));
        setPreview(morph.preview);
        setPreviewMode(false);
      });
  }, [unitName]);
  const message = previewMode ? "Please update your morph." : "Please confirm the selection.";
  console.log("UnitConfirm.preview:", preview);
  const onChange = useCallback(() => {
    setPreviewMode(true);
  }, []);
  return (
    <div id="UnitConfirm" className="unit-hub">
    <UnitHub {...{gameId, unitName, morph: preview, formRef, onChange}}>
      <ConfirmationMenu {...{message, previewMode, refetchMorph}}>
        <OptionSelect {...{missingParams: morph.missingParams}} />
      </ConfirmationMenu>
    </UnitHub>
    </div>
  );
};

export function Morphs() {
  if (!getLocalMorphs()) {
    setLocalMorphs([]);
  };
  const localMorphs = getLocalMorphs();
  return (
    <div id="Morphs">
      <menu>
      {Object.entries(localMorphs).map(([indexNo, morphKey]) => {
        const {pk, morphId, gameId, unitName} = morphKey;
        return (
          <li key={pk}>
            <NavLink to={"/morphs/" + indexNo}>
              <ProfileIcon {...{gameId, unitName}}>
                {morphId}
              </ProfileIcon>
            </NavLink>
          </li>
        );
      })
      }
      </menu>
      <Outlet />
    </div>
  );
}

export function EvolveMorph() {
  const {fullMorph} = useLoaderData();
  const {initArgs, morph} = fullMorph;
  const {gameNo, unitName} = initArgs;
  const gameId = "fe" + gameNo;
  const [preview, setPreview] = useState(morph);
  const formRef = useRef(null);
  //const [previewMode, setPreviewMode] = useState(false);
  useEffect(() => {
    ///setPreviewMode(true);
    setPreview(fullMorph.morph);
  }, [unitName]);
  const onChange = useCallback(() => {
    console.log("onChange");
    //setPreviewMode(true);
  }, []);
  return (
    <div id="EvolveMorph" className="unit-hub">
    <UnitHub {...{gameId, unitName, morph: preview, formRef, onChange}}>
      <MorphMethodSelect {...{gameId, onChange}} />
      <button onClick={(e) => console.log(e.currentTarget)} type="button">Preview</button>
    </UnitHub>
    </div>
  );
}
