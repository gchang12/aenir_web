import axios from 'axios';

import type {
  MorphInitParams,
  Morph,
  MissingParams,
} from "./_types";

const RESOURCE_URL: string = "http://localhost:8000/dracogate/api/morphs/";

function createMorph(kwargs: MorphInitParams) {
  const morphFetchTask = axios
    .get(RESOURCE_URL, {params: kwargs})
    .then(resp => resp.data)
    .catch(err => console.log(err));
  return morphFetchTask;
};

export async function forceCreateMorph(kwargs: MorphInitParams) {
  let morph: Morph;
  const [isSuccess, data] = await createMorph(kwargs);
  if (isSuccess) {
    morph = data;
  } else {
    // Repopulate `kwargs` with defaults.
    //console.log(data);
    kwargs.kwargs = {};
    Object.entries(data.missingParams).forEach(entry => {
      const [key, values] = entry;
      const [defaultVal] = values;
      kwargs.kwargs[key] = defaultVal;
    });
    kwargs.kwargs = JSON.stringify(kwargs.kwargs);
    //console.log(kwargs);
    let [_, defaultMorph] = await createMorph(kwargs);
    //console.log(defaultMorph);
    morph = defaultMorph;
    morph.missingParams = data.missingParams;
  };
  return morph;
};

