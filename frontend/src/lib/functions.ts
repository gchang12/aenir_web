import axios from 'axios';
import {
  STAT_LIST,
} from "../constants";

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

export function getStatList(gameId) {
  const gameNo = Number(gameId.replace("fe", ""));
  switch (gameNo) {
    case 4:
      return STAT_LIST.GENEALOGY;
    case 5:
      return STAT_LIST.THRACIA;
    case 6:
    case 7:
    case 8:
      return STAT_LIST.GBA;
    case 9:
      return STAT_LIST.RADIANT;
  };
};

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

export function listMorphMethods(gameId) {
  // universal to FE{4..9}.
  const morphMethods = [
    "level_up",
    "promote",
  ];
  // set stat boosters
  switch (gameId) {
    case "fe4":
      break;
    case "fe5":
    case "fe6":
    case "fe7":
    case "fe8":
    case "fe9":
      morphMethods.push("use_stat_booster");
    default:
      throw new Error("Unrecognized game: " + gameId);
  };
  // set game-specific methods.
  switch (gameId) {
    case "fe4":
      break;
    case "fe5":
      morphMethods.push("set_scrolls");
      break;
    case "fe6":
      break;
    case "fe7":
      morphMethods.push("use_afas_drops");
      break;
    case "fe8":
      morphMethods.push("use_metiss_tome");
      break;
    case "fe9":
      morphMethods.push("set_bands");
      morphMethods.push("set_knight_ward");
      break;
    default:
      throw new Error("Unrecognized game: " + gameId);
  };
  return morphMethods;
}

