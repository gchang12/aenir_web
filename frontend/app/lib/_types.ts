export type Game = {
  gameNo: number;
  name: string;
  title: string;
};

export type MorphInitArgs = {
  game_no: number;
  name: string;
  father?: string;
  hard_mode?: boolean;
  number_of_declines?: number;
  route?: string;
  lyn_mode?: boolean;
};

export type Morph = {
  currentCls: str;
  currentLv: number;
  currentStats: Array<[str, number]>;
  currentMaxes: Array<[str, number]>;
};

export type Stats = Array<[str, number]>;

export type Unit = {
  game: number;
  name: string;
  class: string;
  lv: number;
};
