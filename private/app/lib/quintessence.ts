import axios from 'axios';

import type {
  GetMorphArgs,
  Morph,
  MissingParams,
} from "./_types";

const RESOURCE_URL: string = "http://localhost:8000/dracogate/api/morphs/";

function getMorph(args: GetMorphArgs) {
  const morphFetchTask = axios
    .get(RESOURCE_URL, {params: args})
    .then(resp => resp.data)
    .catch(err => console.log(err));
  return morphFetchTask;
};

export async function previewMorph(args: GetMorphArgs) {
  let morph: Morph;
  let [isSuccess, data] = await getMorph(args);
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
      /* console.log(key, defaultVal); */
    });
    args.kwargs = JSON.stringify(args.kwargs);
    /* console.log(args); */
    /* console.log(args.kwargs); */
    //console.log(kwargs);
    let [_, defaultMorph] = await getMorph(args);
    //console.log(defaultMorph);
    morph = defaultMorph;
  };
  morph.history = [["__init__", args]];
  return { morph, missingParams: Object.entries(data.missingParams) };
};

