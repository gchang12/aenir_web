import {
  redirect,
} from 'react-router';
import {
  useState,
} from 'react';
import type {
  Route,
} from "./+types/home";
import {
  findFireEmblemGame,
} from '../utility/functions';

import axios from 'axios';

{/* META */}

export function meta({}: Route.MetaArgs) {
  return [
    { title: "Aenir: A Fire Emblem stat calculator" },
    { name: "description", content: "Calculate Fire Emblem stats here!" },
  ];
}

export async function loader() {
  const sourceUrl = "http://127.0.0.1:8000/dracogate/api/preview_morph/";
  const morphList = (await axios.get(sourceUrl)).data;
  return {morphList};
};

function App({loaderData}) {
  const {morphList} = loaderData;
  return (
    <>
      <h1>Home</h1>
      {morphList.map(morph => {
        const game = findFireEmblemGame({gameNo: morph.game});
        const unit = morph.name
        morph.currentCls = morph.current_cls;
        morph.currentLv = morph.current_lv;
        morph.currentStats = morph.current_stats;
        morph.currentMaxes = morph.max_stats;
        const imgSuffix = game.no === 8 ? "gif" : "png";
        const imgFile = `${unit}.${imgSuffix}`;
        return (
          <>
          <figure>
            <img src={`/static/${game.name}/characters/${imgFile}`} alt={`Portrait of ${unit}, ${imgFile}`} />
            <figcaption>
              {unit}
            </figcaption>
          </figure>
          <table id="stats-table">
            <tbody>
              <tr key="Class">
                <th>Class</th>
                <td>{morph.currentCls}</td>
              </tr>
              <tr key="Lv">
                <th>Lv</th>
                <td>{morph.currentLv}</td>
              </tr>
              {morph.currentStats.map(statVal => {
                const [stat, value] = statVal;
                const globalMax = globalMaxes[stat];
                const classMax = globalMax === null ? null : morph.currentMaxes.find(someStat => someStat[0] === stat)[1];
                return (
                  <tr key={stat}>
                    <th>{stat}</th>
                    <td>{value}</td>
                    <td><meter min="0" max={globalMax} high={classMax} value={value}></meter></td>
                  </tr>
                );
              })
              }
            </tbody>
          </table>
        </>
      );
    })
    }
  </>
  );
};

export default App;
