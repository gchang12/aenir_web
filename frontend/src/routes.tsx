import {
  useState,
  useEffect,
  useContext,
  useCallback,
  useRef,
  useMemo,
  Fragment,
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
} from "./lib/constants";
import {
  MorphMethodMenu,
  MorphMethodSelect,
  OptionSelect,
  CurrentStatsTable,
  BlankStatsTable,
  InputStatsTable,
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
  normalizeArgValues,
  calculateStatsDelta,
  retrieveMorph,
  getNullGrowthStats,
  statsAreCompatible,
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
          <li><NavLink to="/compare-morphs/">Compare</NavLink></li>
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
    <>
    <div id="MorphHub" className="unit-hub">
      <UnitHub {...{gameId, unitName, morph: current}}>
        <MorphMethodSelect {...{gameId, onMethodSelect, currentMethod: methodName}} />
      </UnitHub>
    </div>
    <Outlet />
    </>
  );
}

export function MorphMethodExecute() {
  const {methodName} = useParams();
  const {pk, fullMorph, paramBounds} = useLoaderData();
  //const [paramBounds2, setParamBounds2] = useState(paramBounds);
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
    const action = e.currentTarget.value;
    navigate(`/morphs/${pkLoc}/${action}`);
  }, [pkLoc]);
  const onFormChange = useCallback((e) => {
    //console.log(e.currentTarget);
    setPreviewMode(true);
  }, []);
  const onPreviewButtonClick = useCallback((e) => {
    const formData = new FormData(formRef.current)
    const args = normalizeArgValues(formData);
    simulateMorphMethod(pk, methodName, args)
      .then((response) => {
        setPreview(response.morph);
        // TODO: Come up with a better patch.
        //console.log("response.paramBounds:", response.paramBounds, "paramBounds:", paramBounds);
        //setPreviewMode(response.paramBounds != null && paramBounds != null && Object.keys(response.paramBounds)[0] == Object.keys(paramBounds)[0]);
        setPreviewMode(false);
        //setParamBounds2(response.paramBounds ?? []);
      });
  }, [pk, methodName]);
  const highlightMap = calculateStatsDelta(current, preview ?? current);
  return (
    <>
    <MorphHub {...{methodName}} />
    <div id="MorphPreview" className="unit-hub">
      <UnitHub {...{gameId, unitName, morph: previewMode == true ? current : preview, onFormChange, formRef, highlightMap}}>
      <MorphMethodMenu {...{methodName, paramBounds, morph: current, gameNo}} />
      <button disabled={previewMode !== true} onClick={onPreviewButtonClick} type="button">Preview</button>
        <button disabled={previewMode !== false} type="submit">Confirm</button>
      </UnitHub>
    </div>
    </>
  );
}

export function MorphComparison() {
  const {localMorphs} = useLoaderData();
  const [morphs, setMorphs] = useState([]);
  const [diff, setDiff] = useState(null);
  const [statsDelta, setStatsDelta] = useState([]);
  const loadMorph = useCallback((e) => {
    const pk = e.currentTarget.value;
    console.log("pk", pk);
    retrieveMorph(pk)
      .then(morph => {
        console.log("morph:", morph);
        console.log("morphs:", morphs);
        setMorphs([...morphs, {...morph, pk}]);
        setDiff(null);
      })
      .catch(err => console.log(err));
  }, [morphs]);
  const formRef = useRef(null);
  const formRef2 = useRef(null);
  const calculateDiff = useCallback((e) => {
    //console.log("morphs:", morphs);
    const avgMorph = morphs.at(0);
    const nullGrowthStats = getNullGrowthStats("fe" + avgMorph.initArgs.gameNo);
    //console.log("avgStats:", avgMorph.stats);
    const currentDiff = [];
    if (formRef.current.reportValidity()) {
      const inputStats = new FormData(formRef.current);
      let avgStat, diffValue;
      for (const [stat, inputStat] of inputStats.entries()) {
        if (nullGrowthStats.includes(stat)) {
          diffValue = null;
        } else {
          avgStat = avgMorph.stats.find(statArray => statArray[0] === stat)[1];
          diffValue = Math.round(100 * (Number(inputStat) - avgStat)) / 100;
        }
        currentDiff.push([stat, diffValue]);
      }; 
      setDiff(currentDiff);
      const zeroStats = avgMorph.stats.map(stat => [stat[0], 0]);
      setStatsDelta(calculateStatsDelta({stats: zeroStats}, {stats: currentDiff}));
    };
  }, [morphs]);
  const clearDiff = useCallback((e) => {
    setDiff(null);
  }, []);
  const removeMorph = useCallback((e) => {
    setMorphs(morphs.filter(morph => morph.pk !== e.currentTarget.value));
    setDiff(null);
  }, []);
  const attemptValidationAndCompare = useCallback((e) => {
    const [morph1, morph2] = morphs;
    const currentDiff = [];
    if (statsAreCompatible(morph1, morph2)) {
      const nullGrowthStats = getNullGrowthStats("fe" + morph1.initArgs.gameNo);
      let stat2, diffValue;
      for (const [stat, statValue] of morph1.morph.stats) {
        if (nullGrowthStats.includes(stat)) {
          diffValue = null;
        } else {
          stat2 = morph2.morph.stats.find(statBundle => statBundle[0] === stat)[1];
          diffValue = Math.round(100 * (Number(stat2) - statValue)) / 100;
        }
        currentDiff.push([stat, diffValue]);
      };
      setDiff(currentDiff);
      console.log(currentDiff);
      const zeroStats = morph1.morph.stats.map(stat => [stat[0], 0]);
      setStatsDelta(calculateStatsDelta({stats: zeroStats}, {stats: currentDiff}));
    };
  }, [morphs]);
  return (
    <div id="MorphComparison">
      <Form method="post">
        <select multiple disabled={morphs.length === 2} onChange={loadMorph}>
        {Object.entries(localMorphs).map(([indexNo, morph]) => {
          const {pk, gameId, unitName, morphId} = morph;
          console.log("Listing the morphs");
          return (
            <option key={indexNo} value={pk} disabled={morphs.map(morph => morph.pk).includes(pk)}>
              {"(" + indexNo + ") " + morphId}
            </option>
          );
        })
        }
        </select>
      </Form>
      <div className="unit-comparison">
      {morphs.length === 1 && morphs.slice(0, 1).map(morph => {
        console.log("Listing the selected morphs1");
        const {gameId, unitName} = getLocalMorphs().find(localMorph => localMorph.pk === morph.pk);
        return (
          <Fragment key={morph.pk}>
          <div className="UnitHub">
            <UnitHub {...{gameId, unitName, morph: morph.morph}} />
            <button value={morph.pk} onClick={removeMorph} type="button">Remove</button>
          </div>
          <div className="UnitHub">
            <ProfileIcon {...{gameId, unitName}}>
            {unitName}
            </ProfileIcon>
            <ClassLevelInfo {...{morph: morph.morph}} />
            <Form className="ConfirmationMenu" ref={formRef}>
              <InputStatsTable {...{gameId}} />
              <button onClick={calculateDiff} type="button">Compare</button>
            </Form>
          </div>
          </Fragment>
        );
      })
      }
      {morphs.length === 2 && morphs.map(morph => {
        console.log("Listing the selected morphs2");
        const {gameId, unitName} = getLocalMorphs().find(localMorph => localMorph.pk === morph.pk);
        return (
          <div className="UnitHub" key={morph.pk}>
            <UnitHub {...{gameId, unitName, morph: morph.morph}} />
            <button value={morph.pk} onClick={removeMorph} type="button">Remove</button>
          </div>
        );
      })
      }
      {morphs.length === 2 && (
        <button type="button" onClick={attemptValidationAndCompare}>Compare</button>
      )}
      {diff != null && (
        <>
        {/* <ClassLevelInfo {...{morph: morphs.at(0)?.morph}} /> */}
        <CurrentStatsTable {...{stats: diff, highlightMap: statsDelta}} />
        </>
      )}
      </div>
    </div>
  );
};
