import axios from 'axios';
import {
  getUnitList,
} from '../../constants/morphs/new-morph.tsx';

export async function unitListLoader( {game} ) {
  const sourceUrl = "http://127.0.0.1:8000/dracogate/api/initialization_view/"
  let unitList = [];
  await axios
    .get(sourceUrl,
      {params: {game: game.no}},
    )
    .then(res => unitList.push(...res.data))
    .catch(err => {
      unitList = null;
    });
  return unitList;
}

function unitListLoader2( {game} ) {
  return getUnitList({game.no});
}

export async function unitStatsLoader( {initParams} ) {
  const sourceUrl = "http://127.0.0.1:8000/dracogate/api/initialization_view/"
  // containers for output
  let metaStats = {
    currentCls: null,
    currentLv: null,
  };
  let currentStats = null;
  let missingParams = null;
  await axios
    .post(sourceUrl,
      initParams,
    )
    .then(res => {
      const data = res.data;
      const [success, clsLv, value] = data;
      if (success) {
        currentStats = value;
        metaStats.currentCls, metaStats.currentLv = clsLv
      } else {
        missingParams = value;
      };
    })
    .catch(err => console.log(err));
  if (missingParams !== null) {
    for (const item of Object.entries(missingParams)) {
      const [field, choices] = item;
      const defaultVal = choices[0];
      initParams[field] = defaultVal;
    };
    await axios
      .post(sourceUrl,
        {data: initParams},
      )
      .then(res => {
        const data = res.data;
        const [_, clsLv, value] = data;
        [currentCls, currentLv] = clsLv;
        currentStats = value;
      })
      .catch(err => console.log(err));
  }
  return [metaStats, currentStats, missingParams];
};
