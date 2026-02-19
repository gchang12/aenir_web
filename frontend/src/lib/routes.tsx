import {
  useState,
  useEffect,
} from 'react'
import {
  useLoaderData,
  useFetcher,
  useParams,
  NavLink,
  Outlet,
} from "react-router";
import {
  ProfileHead,
  ProfileLevelAndClass,
  StatTable,
  OptionSelect,
} from "./Components";
import {
  GAMES,
  UNITS,
} from "./constants";
import {
  previewMorph,
} from "./functions";

export function Root() {
  return (
    <>
    <nav>
      <menu>
        <li><NavLink to="/create-morph/">Select Game</NavLink></li>
        <li><NavLink to="/create-morph/fe6/">Select Unit - FE6</NavLink></li>
        <li><NavLink to="/create-morph/fe6/Roy">Confirm FE6 Roy</NavLink></li>
        <li><NavLink to="/create-morph/fe6/Rutger">Confirm FE6 Rutger</NavLink></li>
      </menu>
    </nav>
    <Outlet />
    </>
  );
};

export function GameSelect() {
  return (
    <>
    <main id="create-morph">
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
    </main>
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
  const fetcher = useFetcher();
  const [kishuna, setKishuna] = useState(morph);
  // Fixes the data-reloading problem.
  useEffect(() => {
    const game_no = gameId.replace("fe", "");
    const name = unitName;
    console.log(game_no, name);
    previewMorph(game_no, name, {})
      .then(resp => setKishuna(resp.morph))
      .catch(err => console.log(err))
  }, [unitName]);
  /*
  useEffect(async () => {
    previewMorph(game_no, name, {})
      .then(resp => resp.data)
      .then(data => setKishuna(data.morph))
      .catch(err => console.log(err))
  }, [unitName]);
  */
  // const fetcher = useFetcher();
  // console.log(gameId, unitName, missingParams);
  const gameName = GAMES.find(game => gameId === "fe" + game.no)?.name;
  const {stats, unitClass, level} = kishuna;
  const imgSuffix = gameId === "fe8" ? ".gif" : ".png";
  function toggleButtonAbility(value) {
    const createMorphButton = document.querySelector("#create-morph-button");
    if (createMorphButton != null) {
      createMorphButton.disabled = value;
    };
  };
  async function refetchMorph(e) {
    // Test to see if this works.
    toggleButtonAbility(true);
    const formData = new FormData(e.currentTarget);
    const kwargs = {};
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
    // console.log(Object.entries(kwargs));
    const game_no = kwargs["game_no"];
    const name = kwargs["name"];
    setKishuna((await previewMorph(game_no, name, kwargs)).morph);
  };
  const morphId = "Morph-" + new Date().toISOString().replaceAll(/[.:-]/g, "").replace("T", "_");
  // const morphId = "";
  toggleButtonAbility(false);
  return (
    <>
    <form onChange={refetchMorph} method="post" className="create-morph">
      <ProfileHead figureTitle={unitName} imgSrc={["", "images", gameName, "characters", unitName + imgSuffix].join("/")}>
        <table>
          <tbody>
          <ProfileLevelAndClass {...{unitClass, level}} />
          <OptionSelect {...{missingParams}} />
          </tbody>
        </table>
      </ProfileHead>
      <table>
        <tbody>
        <StatTable {...{stats, highlight: true}} />
        </tbody>
      </table>
      <input name="game_no" value={gameId.replace("fe", "")} type="hidden" />
      <input name="name" value={unitName} type="hidden" />
      {/* TODO: Reinsert this if the user is logged in. */}
      <input name="morph_id" type="text" defaultValue={morphId} required maxlength="25" />
      {/* <input name="morph_id" type="hidden" defaultValue={morphId} required maxLength="25" /> */}
      <button type="submit" id="create-morph-button">Create!</button>
    </form>
    </>
  );
};

