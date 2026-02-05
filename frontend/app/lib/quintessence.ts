import axios from 'axios';

import type {
  MorphInitParams,
  Morph,
  MissingParams,
} from "./_types";

const RESOURCE_URL: string = "http://localhost:8000/dracogate/api/morphs/";

function createMorph(args: MorphInitParams) {
  const morphFetchTask = axios
    .get(RESOURCE_URL, {params: args})
    .then(resp => resp.data)
    .catch(err => console.log(err));
  return morphFetchTask;
};

export async function forceCreateMorph(args: MorphInitParams) {
  let morph: Morph;
  const [isSuccess, data] = await createMorph(args);
  if (isSuccess) {
    morph = data;
  } else {
    // Repopulate `args` with defaults.
    //console.log(data);
    args.kwargs = {};
    Object.entries(data.missingParams).forEach(entry => {
      const [key, values] = entry;
      const [defaultVal] = values;
      args.kwargs[key] = defaultVal;
    });
    args.kwargs = JSON.stringify(args.kwargs);
    //console.log(kwargs);
    let [_, defaultMorph] = await createMorph(args);
    //console.log(defaultMorph);
    morph = defaultMorph;
    morph.missingParams = data.missingParams;
  };
  return morph;
};

