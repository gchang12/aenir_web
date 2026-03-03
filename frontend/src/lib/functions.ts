import axios from 'axios';

export function getMorph(game_no, name, kwargs) {
  const RESOURCE_URL: string = "http://localhost:8000/dracogate/api/morphs/";
  const params = {
    game_no,
    name,
    ...kwargs,
  };
  const fetchTask = axios
    .get(RESOURCE_URL, {params})
    .then(resp => resp.data)
    .catch(err => console.log(err));
  return fetchTask;
};

export async function previewMorph(game_no, name, kwargs) {
  let morph = await getMorph(game_no, name, {});
  const {missingParams} = morph;
  if (typeof missingParams === 'object') {
    const newKwargs = {};
    Object.entries(missingParams).forEach(([key, values]) => {
      // const [key, values] = entry;
      const [defaultVal] = values;
      newKwargs[key] = defaultVal;
    });
    Object.entries(kwargs).forEach(([key, value]) => {
      // const [key, value] = entry;
      newKwargs[key] = value;
    });
    morph = await getMorph(game_no, name, newKwargs);
  };
  return {morph, missingParams};
};

export function createMorph(morph_id, game_no, name, options) {
  const RESOURCE_URL: string = "http://localhost:8000/dracogate/api/morphs/";
  const data = {
    morph_id,
    game_no,
    name,
    ...options,
  };
  const fetchTask = axios
    .post(RESOURCE_URL, data)
    .then(resp => resp.data)
    .catch(err => console.log(err));
  return fetchTask;
};
