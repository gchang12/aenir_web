import {
  redirect,
} from 'react-router';
import axios from 'axios';
import {
  getUnitList,
} from '../../_constants/morphs/new-morph.tsx';

export function unitListLoader( {game} ) {
  const gameNo = game.no;
  return getUnitList({gameNo});
}

export async function unitStatsLoader( {initParams} ) {
  const sourceUrl = "http://127.0.0.1:8000/dracogate/api/initialization_view/";
  // containers for output
  let metaStats = {
    currentCls: null,
    currentLv: null,
  };
  let currentStats = null;
  let missingParams = null;
  console.log("About to send POST request to URL.");
  await axios
    .post(sourceUrl,
      {data: initParams},
    )
    .then(res => {
      const data = res.data;
      const [success, clsLv, value] = data;
      console.log("Data has been fetched.");
      if (success) {
        currentStats = value;
        [metaStats.currentCls, metaStats.currentLv] = clsLv
        console.log("Unit has been found. Level: " + metaStats.currentLv);
      } else {
        missingParams = value;
        console.log("Failure. missingParams: " + missingParams);
      };
    })
    .catch(err => console.log(err));
  console.log("Checking if missingParams need to be populated.");
  if (missingParams !== null) {
    console.log("missingParams not null: " + missingParams);
    const [field, choices] = missingParams;
    const defaultVal = choices[0];
    initParams[field] = defaultVal;
    await axios
      .post(sourceUrl,
        {data: initParams},
      )
      .then(res => {
        const data = res.data;
        const [_, clsLv, value] = data;
        [metaStats.currentCls, metaStats.currentLv] = clsLv;
        currentStats = value;
      })
      .catch(err => console.log(err));
  };
  console.log("End of unitStatsLoader");
  return [metaStats, currentStats, missingParams];
};

export function newUnitSaver( {initParams, showError} ) {
  const sourceUrl = "http://127.0.0.1:8000/dracogate/api/initialization_view/";
  console.log("About to send PUT request to URL.");
  return axios.put(sourceUrl, {data: initParams});
};
