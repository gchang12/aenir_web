import axios from 'axios';

import type {
  MorphInitParams,
  Morph,
  MissingParams,
} from "./_types";

const RESOURCE_URL: string = "http://localhost:8000/dracogate/api/morphs/";

function createMorph(kwargs: MorphInitParams) {
  const morphFetchTask = axios
    .post(RESOURCE_URL, kwargs)
    .then(resp => resp.data)
    .catch(err => console.log(err));
  return morphFetchTask;
};

export async function forceCreateMorph(kwargs: MorphInitParams) {
  const data = await createMorph(kwargs);
  if (data.missingParams != null) {
    // Repopulate `kwargs` with defaults.
    data.missingParams.forEach(entry => {
      const [key, values] = entry;
      const [defaultVal] = values;
      kwargs[key] = defaultVal;
    });
  };
  let morph = await createMorph(kwargs);
  morph.missingParams = data.missingParams;
  return morph;
};

