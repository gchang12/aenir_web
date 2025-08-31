import {
  Outlet,
  NavLink,
} from 'react-router';

export function getFireEmblemGames() {
  return [
    {
      no: 4,
      title: "Genealogy of the Holy War",
      name: "genealogy-of-the-holy-war",
    },
    {
      no: 5,
      title: "Thracia 776",
      name: "thracia-776",
    },
    {
      no: 6,
      title: "Sword of Seals",
      name: "binding-blade",
    },
    {
      no: 7,
      title: "Blazing Sword",
      name: "blazing-sword",
    },
    {
      no: 8,
      title: "The Sacred Stones",
      name: "the-sacred-stones",
    },
    {
      no: 9,
      title: "Path of Radiance",
      name: "path-of-radiance",
    },
  ];
};

function GameSelectMenu() {
  const feGames = getFireEmblemGames();
  return (
    <>
    <menu id="game-select">
      {feGames.map(currentGame => {
        const {no, title, name} = currentGame;
        return (
          <li>
            <NavLink to={`/create/fe${no}/`}>
              <figure className="cover-art" width="300" height="145">
                <img src={`/static/${name}/cover-art.png`} alt={`Official cover for FE${no}: ${title}`} />
                <figcaption>FE{no}: {title}</figcaption>
              </figure>
            </NavLink>
          </li>
        );
      })
      }
    </menu>
    <Outlet />
    </>
  );
};

export default GameSelectMenu;
