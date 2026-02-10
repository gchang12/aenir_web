import {
  expect,
  test,
} from 'vitest';

import {
  getMorph,
  previewMorph,
} from "./App";

function sum(a, b) {
  return a + b;
}

test("Sends a request for data from the backend", () => {
  expect([]).toStrictEqual([])
});

test("This test sends a request for Morph-data for FE6 Roy.", async () => {
  const game_no = 6;
  const name = "Roy";
  const kwargs = {};
  const morph = await getMorph(game_no, name, kwargs);
  const { currentCls, currentLv, currentStats, maxStats, maxLv } = morph;
  expect(currentCls).toBe("Lord");
  expect(currentLv).toBe(1);
  expect(maxLv).toBe(20);
  expect(currentStats).toStrictEqual(
    [
      ["HP", 18_00],
      ["Pow", 5_00],
      ["Skl", 5_00],
      ["Spd", 7_00],
      ["Lck", 7_00],
      ["Def", 5_00],
      ["Res", 0],
      ["Con", 6_00],
      ["Mov", 5_00],
    ]
  );
  expect(maxStats).toStrictEqual(
    [
      ["HP", 60_00],
      ["Pow", 20_00],
      ["Skl", 20_00],
      ["Spd", 20_00],
      ["Lck", 30_00],
      ["Def", 20_00],
      ["Res", 20_00],
      ["Con", 20_00],
      ["Mov", 15_00],
    ]
  )
});
