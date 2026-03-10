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


export function UnitConfirm() {
  const {gameId, unitName} = useParams();
  const {morph} = useLoaderData();
  const [preview, setPreview] = useState(morph.preview);
  const [previewMode, setPreviewMode] = useState(false);
  const fetcher = useFetcher();
  const formRef = useRef(null);
  useEffect(() => {
    setPreviewMode(morph.missingParams != null);
    setPreview(morph.preview);
    console.log("useEffect.fetcher:", fetcher);
  }, [unitName]);
  const refetchMorph = useCallback(() => {
    const queryList = [];
    const formData = new FormData(formRef.current);
    for (const [key, value] of formData.entries()) {
      queryList.push(key + "=" + value);
    };
    const url = `/create-morph/${gameId}/${unitName}/?` + queryList.join("&")
    console.log("Loading data from:", url);
    const morph = fetcher.load(url)
      .then(() => {
        console.log("Done loading data!")
        const {morph} = fetcher.data;
        console.log("fetcher.data.morph:", morph);
        console.log("UnitConfirm.refetchMorph:", queryList);
        //setPreviewMode(false);
        return morph;
      })
    //setPreview(morph.preview);
    // Shouldn't this always be defined?
  }, [unitName]);
  const message = previewMode ? `Please provide extra parameters for ${unitName}.` : "Please confirm the selection.";
  console.log("UnitConfirm.preview:", morph.preview);
  //console.log("missingParams:", missingParams);
  return (
    <div id="UnitConfirm">
      <ProfileIcon {...{gameId, unitName}} />
      <ClassLevelInfo {...{morph: morph.preview}} />
      <fetcher.Form onChange={() => setPreviewMode(true)} ref={formRef}>
        <ConfirmationMenu {...{message, previewMode, refetchMorph}}>
          <OptionSelect {...{missingParams: morph.missingParams}} />
        </ConfirmationMenu>
      </fetcher.Form>
      {/* */}
      <CurrentStatsTable {...{morph: morph.preview}} />
    </div>
  );
};

