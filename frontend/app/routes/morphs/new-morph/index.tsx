import {
  GameUrlList,
} from '../../../components/morphs/new-morph.tsx';
import {
  getFireEmblemGames
} from '../../../constants/morphs/new-morph.tsx';

function Main() {
  const fireEmblemGames = getFireEmblemGames();
  return (
    <>
      <article>
        <h1>Game Select</h1>
        <nav id="game-select">
          <menu>
            <GameUrlList gameList={fireEmblemGames} />
          </menu>
        </nav>
      </article>
    </>
  );
};

export default Main;
