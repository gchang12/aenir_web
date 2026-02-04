import axios from 'axios';

type MorphInitKwargs = {
  father?: string;
  hard_mode?: boolean;
  number_of_declines?: number;
  route?: string;
  lyn_mode?: boolean;
};

type Morph = {
};

function createMorph(game_no: number, name: string, kwargs: MorphInitKwargs) {
  let morph;
  let initKwargs = {game_no, name, ...kwargs};
  axios
    .get("http://localhost:8000/")
    .then();
};
