import {
  useState,
} from 'react'
import {
  useLoaderData,
  useFetcher,
  NavLink,
  useParams,
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

export function GameSelect() {
  return (
    <nav>
      <menu>
      {GAMES.map(game => {
        const imgSrc = ["", "images", game.name, "cover-art.png"].join('/');
        return (
          <li key={game.no}>
            <NavLink to={["", 'create-morph', 'fe' + game.no, ''].join('/')}>
              <figure>
                <img src={imgSrc} alt={imgSrc} />
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

export function UnitSelect() {
  const {gameId} = useParams();
  const gameName = GAMES.find(game => gameId === "fe" + game.no)?.name;
  const unitListForGame = UNITS.filter(unit => gameId === "fe" + unit.gameNo);
  const imgSuffix = gameId === "fe8" ? ".gif" : ".png";
  return (
    <nav>
      <menu>
      {unitListForGame.map(unit => {
        const imgSrc = ["", "images", gameName, "characters", unit.name + imgSuffix].join('/');
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
  );
};

export function UnitConfirm() {
  const {morph, missingParams, unitName, gameId} = useLoaderData();
  // const fetcher = useFetcher();
  // console.log(gameId, unitName, missingParams);
  const gameName = GAMES.find(game => gameId === "fe" + game.no)?.name;
  const [kishuna, setKishuna] = useState(morph);
  const {stats, unitClass, level} = kishuna;
  const imgSuffix = gameId === "fe8" ? ".gif" : ".png";
  async function refetchMorph(e) {
    const game_no = gameId.replace("fe", "");
    const name = unitName;
    const kwargs = {};
    const formData = new FormData(e.currentTarget);
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
    setKishuna((await previewMorph(game_no, name, kwargs)).morph);
  };
  return (
    <>
    <form onChange={refetchMorph}>
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
      <button>Create!</button>
    </form>
    </>
  );
};

