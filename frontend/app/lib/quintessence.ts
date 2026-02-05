import axios from 'axios';

import type {
  MorphInitParams,
  Morph,
  MissingParams,
} from "./_types";

const RESOURCE_URL: string = "http://localhost:8000/dracogate/api/morphs/";

async function createMorph(kwargs: MorphInitParams) : [Morph, MissingParams] {
  const morphFetch = axios
    .post(RESOURCE_URL, kwargs)
    .then(resp => {
      const data = resp.data;
      missingParams = Object.entries(data.missingParams ?? {});
      return [data, missingParams];
    });
  const [morph, missingParams] = await morphFetch;
  return [morph, missingParams];
};

export async function forceCreateMorph(kwargs: MorphInitParams) : [Morph, MissingParams] {
  let [morph, missingParams] = await createMorph(kwargs);
  if (missingParams.length > 0) {
    // Repopulate `kwargs` with defaults.
    missingParams.forEach(entry => {
      const [key, values] = entry;
      const [defaultVal] = values;
      kwargs[key] = defaultVal;
    });
  };
  const [morph, missingParams] = await createMorph(kwargs);
  return [morph, missingParams];
};

