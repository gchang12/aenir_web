import {
  Outlet,
  NavLink,
  useParams,
} from 'react-router';
import {
  findFireEmblemGame,
  getUnitList,
} from '../../utility/functions';

function UnitSelectMenu() {
  const {feGame} = useParams();
  const game = findFireEmblemGame({feGame});
  const unitList = getUnitList({gameNo: game.no});
  return (
    <>
    <menu id="unit-select">
    {unitList.map(name => {
      const imgSuffix = game.no === 8 ? "gif" : "png";
      const imgFile = `${name}.${imgSuffix}`;
      const href = `/create/${feGame}/${name}/`;
      return (
        <li key={name}>
        {/* <NavLink to={href}> */}
          <NavLink to={href} reloadDocument>
            <figure>
              <img src={`/static/${game.name}/characters/${imgFile}`} alt={`Portrait of ${name}, ${imgFile}`} />
              <figcaption>{name}</figcaption>
            </figure>
          </NavLink>
            {/* </NavLink> */}
        </li>
      );
    })
    }
    </menu>
    <Outlet />
    </>
  );
};

export default UnitSelectMenu;
