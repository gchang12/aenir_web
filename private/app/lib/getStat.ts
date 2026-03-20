import type {
  Stats,
} from "./_types";

function getStatByName(stats: Stats, statName: string) : number {
  const statVal: number = stats.find(stat => stat[0] === statName)[1];
  return statVal;
};

function getStatByLoc(stats: Stats, statLoc: number) : number {
  return stats[number]?.get(1);
};

export function getStat(stats: Stats, statNameOrLoc: string | number) : number {
  switch(typeof statNameOrLoc) {
    case 'string':
      return getStatByName(stats, statNameOrLoc);
    case 'number':
      return getStatByLoc(stats, statNameOrLoc);
  };
};
