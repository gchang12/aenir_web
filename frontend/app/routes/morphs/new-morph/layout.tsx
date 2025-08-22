import {
  Outlet,
} from "react-router";

import {
  GameUrlList,
} from '../../../_components/morphs/new-morph.tsx';

export function Layout({ children }: { children: React.ReactNode }) {
  return (
    <article>
      <h1>Game Select</h1>
      <nav id="game-select">
        <menu>
          <GameUrlList gameList={fireEmblemGames} />
        </menu>
      </nav>
      {children}
    </article>
  );
};

{/* NOTE: It would be so fantastic if I knew what I was doing. */}
function MorphInitApp() {
  return <Outlet />;
};

export default MorphInitApp;
