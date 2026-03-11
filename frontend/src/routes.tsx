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
  useNavigate,
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
  MorphMethodMenu,
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
  simulateMorphMethod,
  executeMorphMethod,
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
  const onFormChange = useCallback(() => {
    setPreviewMode(true);
  }, []);
  return (
    <div id="UnitConfirm" className="unit-hub">
    <UnitHub {...{gameId, unitName, morph: preview, formRef, onFormChange}}>
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

export function MorphHub({methodName = null}) {
  const {pk, fullMorph} = useLoaderData();
  const {initArgs, morph} = fullMorph;
  const {gameNo, unitName} = initArgs;
  const gameId = "fe" + gameNo;
  const [current, setCurrent] = useState(morph);
  const [preview, setPreview] = useState(null);
  const navigate = useNavigate();
  const {pkLoc} = useParams();
  useEffect(() => {
    setCurrent(fullMorph.morph);
  }, [pk]);
  const onMethodSelect = useCallback((e) => {
    const action = e.currentTarget.value ?? "";
    navigate(`/morphs/${pkLoc}/${action}`);
  }, [pkLoc]);
  return (
    <div id="MorphHub" className="unit-hub">
      <UnitHub {...{gameId, unitName, morph: current}}>
        <MorphMethodSelect {...{gameId, onMethodSelect, currentMethod: methodName}} />
      </UnitHub>
    </div>
  );
}

export function MorphMethodExecute() {
  const {methodName} = useParams();
  const {pk, fullMorph, paramBounds} = useLoaderData();
  const {gameNo, unitName} = fullMorph.initArgs;
  const gameId = "fe" + gameNo;
  const [current, setCurrent] = useState(fullMorph.morph);
  const [preview, setPreview] = useState(null);
  const [previewMode, setPreviewMode] = useState(null);
  const {pkLoc} = useParams();
  const formRef = useRef(null);
  const navigate = useNavigate();
  useEffect(() => {
    setCurrent(fullMorph.morph);
  }, [pk]);
  const onMethodSelect = useCallback((e) => {
    //console.log(e.currentTarget);
    const action = e.currentTarget.value ?? "";
    navigate(`/morphs/${pkLoc}/${action}`);
  }, [pkLoc]);
  const onFormChange = useCallback((e) => {
    //console.log(e.currentTarget);
    setPreviewMode(true);
  }, []);
  const onPreviewButtonClick = useCallback((e) => {
    console.log(e.currentTarget);
    console.log(formRef.current);
    const formData = new FormData(formRef.current);
    const args = {};
    for (const [key, value] of formData.entries()) {
      console.log("key:", key, "value:", value);
      switch (key) {
        case "num_levels":
          args[key] = (value - current.level[0]);
          break;
        case "promo_cls":
        case "item_name":
        case "scrolls":
        case "bands":
          args[key] = value;
          break;
        default:
          throw new Error("Unrecognized argument:" + key);
      };
    };
    console.log("args:", Object.entries(args));
    simulateMorphMethod(pk, methodName, args)
      .then(({morph}) => {
        console.log(Object.entries(morph));
        setPreview(morph);
        setPreviewMode(false);
      });
  }, [pk, methodName]);
  return (
    <>
    <MorphHub {...{methodName}} />
    <div id="MorphPreview" className="unit-hub">
      <UnitHub {...{gameId, unitName, morph: preview, onFormChange, formRef}}>
        <MorphMethodMenu {...{methodName, paramBounds, morph: current}} />
        <button disabled={previewMode !== true} onClick={onPreviewButtonClick} type="button">Preview</button>
        <button disabled={previewMode !== false} type="submit">Confirm</button>
      </UnitHub>
    </div>
    </>
  );
}

