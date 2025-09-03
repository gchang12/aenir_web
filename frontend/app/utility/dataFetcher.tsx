import axios from 'axios';

export async function initializeUnit( {tempInitParams} ) {
  const sourceUrl = "http://127.0.0.1:8000/dracogate/api/initialize_morph/";
  // containers for output
  let cls = null;
  let lv = null;
  let stats = null;
  let maxes = null;
  let params1 = null;
  let params2 = null;
  const initParams = {...tempInitParams};
  {/* console.log("First POST with data: " + Object.entries(initParams)); */}
  await axios
    .post(sourceUrl,
      {data: initParams},
    )
    .then(res => {
      const [success, data] = res.data;
      if (success) {
        const {current_stats, current_maxes, current_cls, current_lv} = data;
        [stats, maxes, cls, lv] = [current_stats, current_maxes, current_cls, current_lv];
      } else {
        const { missing_params, missing_params2 } = data;
        [params1, params2] = [missing_params, missing_params2]
      }
    })
    .catch(err => {
      const [success, data] = err.response.data;
      const { missing_params, missing_params2 } = data;
      [params1, params2] = [missing_params, missing_params2]
    });
  if (params1 !== null || params2 !== null) {
    if (params1 !== null) {
      const [field, choices] = params1;
      const defaultVal = choices[0];
      initParams[field] = defaultVal;
    };
    if (params2 !== null) {
      const [field, choices] = params2;
      const defaultVal = choices[0];
      initParams[field] = defaultVal;
    };
    {/* console.log("Second POST with data: " + Object.entries(initParams)); */}
    await axios
      .post(sourceUrl,
        {data: initParams},
      )
      .then(res => {
        const [_, data] = res.data;
        const { current_stats, current_maxes, current_cls, current_lv } = data;
        [stats, maxes, cls, lv] = [current_stats, current_maxes, current_cls, current_lv];
        {/* console.log("Class: " + cls + ", Lv: " + lv); */}
      })
      .catch(err => {
        alert(err);
      });
  };
  return {cls, lv, stats, maxes, params1, params2};
};

