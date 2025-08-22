import {
  GameUrlList,
} from '../../../_components/morphs/new-morph.tsx';
import {
  getFireEmblemGames
} from '../../../_constants/morphs/new-morph.tsx';

function Main({ children }: { children: React.ReactNode }) {
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
        {children}
      </article>
    </>
  );
};

export default Main;
