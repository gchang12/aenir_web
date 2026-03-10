import axios from 'axios';

const RESOURCE_URL: string = "http://localhost:8000/dracogate/api/morphs/";

export function getMorph(game_no, name, kwargs) {
  const params = {
    game_no,
    name,
    ...kwargs,
  };
  const fetchTask = axios
    .get(RESOURCE_URL, {params})
    .then(resp => resp.data)
    .catch(err => console.log(err));
  return fetchTask; // returns either 'preview': {...} or 'missingParams': {...}
};

export function setLocalMorphs(value) {
  const morphsAsString = JSON.stringify(value);
  console.log("localStorage.setItem('morphs'," + morphsAsString + ");");
  return localStorage.setItem("morphs", morphsAsString);
};

export function getLocalMorphs() {
  const rawMorphs = localStorage.getItem("morphs");
  console.log("localStorage.getItem('morphs') = " + rawMorphs);
  return JSON.parse(rawMorphs);
};

export function createMorph(morph_id, game_no, name, options) {
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

// TODO: Test these for the love of criminy. These sort of rely on database data. Consider using mocks?

export function retrieveMorph(pk) {
  /*
    "morphId",
    "initArgs": {
      "gameNo",
      "unitName",
      "options",
    },
    "morph",
    "history",
  */
  const url: string = RESOURCE_URL + [pk, ""].join("/");
  const fetchTask = axios
    .get(url)
    .then(resp => resp.data)
    .catch(err => console.log(err));
  return fetchTask;
};

export function simulateMorphMethod(pk, method_name, args) {
  const url = RESOURCE_URL + [pk, method_name, ""].join("/");
  const fetchTask = axios
    .get(url, {params: args})
    .then(resp => resp.data)
    .catch(err => console.log(err));
  return fetchTask;
};

export function executeMorphMethod(pk, method_name, args) {
  const url = RESOURCE_URL + [pk, method_name, ""].join("/");
  const fetchTask = axios
    .patch(url, {params: args})
    .then(resp => resp.data)
    .catch(err => console.log(err));
  return fetchTask;
};

