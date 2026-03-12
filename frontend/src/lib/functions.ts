import axios from 'axios';
import {
  STAT_LIST,
  STAT_BOOSTERS,
} from "./constants";

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
  return localStorage.setItem("morphs", morphsAsString);
};

export function getLocalMorphs() {
  const rawMorphs = localStorage.getItem("morphs");
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
    .patch(url, args)
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
      break;
    default:
      throw new Error("Unrecognized game: " + gameId);
  };
  // set game-specific methods.
  /*
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
  */
  return morphMethods;
}

export function getNullArgs(methodName) {
  switch (methodName) {
    case "level_up":
      return {num_levels: 0};
    case "promote":
      return {promo_cls: ""};
    case "use_stat_booster":
      return {item_name: ""};
    case "set_scrolls":
      return {scrolls: [""]};
    case "use_afas_drops":
      return {};
    case "use_metiss_tome":
      return {};
    case "set_bands":
      return {bands: [""]};
    default:
      throw new Error(`Unrecognized method: '${methodName}'`);
  };
}

export function normalizeArgValues(formData) {
  const args = {};
  for (const [key, value] of formData.entries()) {
    switch (key) {
      case "num_levels":
      case "promo_cls":
      case "item_name":
      case "scrolls":
      case "bands":
        args[key] = value;
        break;
      default:
        throw new Error("Unrecognized argument: " + key);
    };
  };
  return args;
}

export function listStatBoosters(gameNo) {
  switch (gameNo) {
    case 4:
      throw new Error("FE4 has no stat boosters!");
    case 5:
      return STAT_BOOSTERS.THRACIA;
    case 6:
    case 7:
    case 8:
      return STAT_BOOSTERS.GBA;
    case 9:
      return STAT_BOOSTERS.RADIANT;
    default:
      throw new Error("Unrecognized game: " + gameNo);
  };
}

export function calculateStatsDelta(morph1, morph2) {
  const arrayLength = morph1.stats.length;
  const statsDelta = {};
  let statName, stat1, stat2;
  console.log(morph2.stats);
  for (let i=0; i < arrayLength; i++) {
    statName = morph1.stats[i][0];
    stat1 = morph1.stats[i][1];
    stat2 = morph2 == null ? null : morph2.stats[i][1];
    statsDelta[statName] = stat2 == null ? null : stat2 - stat1;
  };
  return statsDelta;
}

export function getNullGrowthStats(gameId) {
  switch (gameId) {
    case "fe4":
      return [];
    case "fe5":
      return ["Lead", "MS", "PC"];
    case "fe6":
    case "fe7":
    case "fe8":
      return ["Con", "Mov"];
    case "fe9":
      return ["Con", "Mov", "Wt"];
  };
};

export function statsAreCompatible(morph1, morph2) {
  function isGBAGame(morph) {
    return [6, 7, 8].includes(morph.initArgs.gameNo);
  };
  if (isGBAGame(morph1) && isGBAGame(morph2)) {
    return true;
  } else if (morph1.initArgs.gameNo === morph2.initArgs.gameNo) {
    return true;
  } else {
    return false;
  };
};
