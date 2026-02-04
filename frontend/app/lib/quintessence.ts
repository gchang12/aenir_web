import axios from 'axios';

import type {
  MorphInitArgs,
  Morph,
} from "./_types";

export function createMorph(kwargs: MorphInitArgs) {
  let morph: Morph;
  axios
    .post("http://localhost:8000/dracogate/api/morphs/")
    .then();
};

