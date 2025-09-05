import {
  Outlet,
  NavLink,
} from 'react-router';
import {
  getFireEmblemGames,
} from '../../utility/functions';

function GameSelectMenu() {
  const feGames = getFireEmblemGames();
  return (
    <>
    <menu id="game-select">
      {feGames.map(currentGame => {
        const {no, title, name} = currentGame;
        return (
          <li key={name}>
            <NavLink to={`/create-morph/fe${no}/`}>
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
