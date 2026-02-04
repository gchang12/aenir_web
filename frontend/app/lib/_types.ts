export type Game = {
  no: number;
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
  gameNo: number;
  name: string;
  class: string;
  lv: number;
};

export enum GameID {
  FE4 = "fe4",
  FE5 = "fe5",
  FE6 = "fe6",
  FE7 = "fe7",
  FE8 = "fe8",
  FE9 = "fe9",
};
