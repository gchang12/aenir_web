export type Game = {
  no: number;
  name: string;
  title: string;
};

export type MorphInitParams = {
  game_no: number;
  name: string;
  father?: string;
  hard_mode?: boolean;
  number_of_declines?: number;
  route?: string;
  lyn_mode?: boolean;
};

export type Stats = Array<[string, number]>;

export type Morph = {
  currentCls: string;
  currentLv: number;
  currentStats: Stats;
  currentMaxes: Stats;
  missingParams?: Array<[string, Array<any>]>;
};

export type MissingParams = Array<[string, Array<any>]>;

export type Unit = {
  gameNo: number;
  name: string;
  class: string;
  lv: number;
};

/*
export enum GameID {
  FE4 = "fe4",
  FE5 = "fe5",
  FE6 = "fe6",
  FE7 = "fe7",
  FE8 = "fe8",
  FE9 = "fe9",
};
export type GameID = "fe4" | "fe5" | "fe6" | "fe7" | "fe8" | "fe9";
*/

export type GameID = string;

