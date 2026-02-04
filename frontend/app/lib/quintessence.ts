import axios from 'axios';

import type {
  MorphInitParams,
  Morph,
  MissingParams,
} from "./_types";

const RESOURCE_URL: string = "http://localhost:8000/dracogate/api/morphs/";

export function createMorph(kwargs: MorphInitParams) : [Morph, MissingParams] {
  let morph: Morph;
  let missingParams: MissingParams;
  axios
    .post(RESOURCE_URL, kwargs)
    .then(resp => {
      const data = resp.data;
      missingParams = Object.entries(data.missingParams ?? {});
      if (missingParams) {
        missingParams.forEach(entry => {
          const [key, values] = entry;
          const [defaultVal] = values;
          kwargs[key] = defaultVal;
        });
        axios
          .post(RESOURCE_URL, kwargs)
          .then(resp => {
            morph = resp.data;
            morph.missingParams = missingParams;
          });
      } else {
        morph = data;
      };
    });
  return [morph, missingParams];
};

