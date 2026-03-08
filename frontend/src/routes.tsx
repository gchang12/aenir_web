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
  ProfileHead,
  ProfileLevelAndClass,
  StatTable,
  OptionSelect,
} from "./lib/Components";
import {
  previewMorph,
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
  const {morph, missingParams, unitName, gameId} = useLoaderData();
  // Fixes the data-reloading problem.
  const gameNo = gameId.replace("fe", "");
  const [morphId, setMorphId] = useState(gameId.toUpperCase() + " " + unitName);
  useEffect(() => {
    previewMorph(gameNo, unitName, {})
      .then(resp => {
        setKishuna(resp.morph);
        setMorphId(gameId.toUpperCase() + " " + unitName);
        // setMorphId(unitName);
      })
      .catch(err => console.log(err))
  }, [unitName]);
  const [kishuna, setKishuna] = useState(morph);
  const {stats, unitClass, level} = kishuna;
  const gameName = GAMES.find(game => gameId === "fe" + game.no)?.name;
  const imgSuffix = gameId === "fe8" ? ".gif" : ".png";
  function toggleButtonAbility(value) {
    const createMorphButton = document.querySelector("#create-morph-button");
    if (createMorphButton != null) {
      createMorphButton.disabled = value;
    };
  };
  function toggleCheckbox(value) {
    const checkbox = document.querySelector("form.create-morph > input[type='checkbox']");
    if (checkbox != null) {
      checkbox.checked = false;
    };
  };
  async function refetchMorph(e) {
    // Test to see if this works.
    toggleButtonAbility(true);
    const formData = new FormData(e.currentTarget);
    const kwargs = {
      game_no: gameNo,
      name: unitName,
    };
    for (const [key, value] of formData) {
      switch(value) {
        case "on":
          kwargs[key] = "true";
          break;
        case "off":
          kwargs[key] = "false";
          break;
        default:
          kwargs[key] = value;
          break;
      };
    };
    setKishuna((await previewMorph(gameNo, unitName, kwargs)).morph);
    // NOTE: Patch!
    toggleButtonAbility(false);
  };
  toggleButtonAbility(false);
  //toggleCheckbox(false);
  console.log("morphId: " + morphId);
  return (
    <>
    <ProfileHead imgSrc={["", "images", gameName, "characters", unitName + imgSuffix].join("/")}>
      <h2>{unitName}</h2>
      <table>
        <tbody>
        <ProfileLevelAndClass {...{unitClass, level}} />
        </tbody>
      </table>
      <Form onChange={refetchMorph} method="post" className="create-morph">
        <OptionSelect {...{missingParams}} />
        <label htmlFor="morph_id">Morph ID</label>
        <input id="morph_id" name="morph_id" type="text" defaultValue={morphId} required maxLength="25" />
        <button type="submit" id="create-morph-button">Create!</button>
      </Form>
    </ProfileHead>
    <table>
      <tbody>
      <StatTable {...{stats, highlight: true}} />
      </tbody>
    </table>
    </>
  );
};

export function Morphs() {
  /*
    {
      "morphId": vmorph.morph_id,
      "initArgs": {
        "gameNo": vmorph.game_no,
        "unitName": vmorph.name,
        "options": vmorph.options,
      },
      "morph": data,
      "history": vmorph.history,
    }
  */
  const {morphs} = useLoaderData();
  return (
    <>
    <h1>Morphs</h1>
    <menu>
    {Object.entries(morphs).map(([indexNo, morph]) => {
      console.log("morph:", Object.entries(morph));
      const {initArgs} = morph;
      const {level} = morph.morph;
      const [currentLv, maxLv] = level;
      const imgSuffix = morph.initArgs.gameNo === 8 ? ".gif" : ".png";
      const gameName = GAMES.find(game => game.no === morph.initArgs.gameNo)?.name;
      return (
        <li key={morph.pk}>
        <img src={["", "images", gameName, "characters", initArgs.unitName + imgSuffix].join("/")} />
        <NavLink to={"/morphs/" + indexNo}>
          <h2>{morph.morphId}</h2>
        </NavLink>
        <table>
          <tbody>
            <tr>
              <th>Game</th>
              <td>{"FE" + initArgs.gameNo}</td>
            </tr>
            <tr>
              <th>Name</th>
              <td>{initArgs.unitName}</td>
            </tr>
            <>
            {Object.entries(initArgs.options).map(([key, value]) => {
              return (
                <tr key={key}>
                  <th>{key}</th>
                  <td>{value}</td>
                </tr>
              );
            })
            }
            </>
            <tr>
              <th>Level</th>
              <td>{currentLv} / {maxLv}</td>
            </tr>
          </tbody>
        </table>
        </li>
      );
    })}
    </menu>
    </>
  );
};

export function EvolveMorph() {
  return (
    <>
    </>
  );
};
