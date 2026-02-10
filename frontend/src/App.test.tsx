import {
  expect,
  test,
  describe,
  it,
  beforeAll,
  afterEach,
  afterAll,
} from 'vitest';

import {
  http,
  HttpResponse,
} from "msw";
import {
  setupServer,
} from "msw/node";

import {
  getMorph,
  previewMorph,
} from "./App";

// TODO: Mock server requests.
// TODO: Migrate tests to backend.

// TEST SKELETON

test("This is a test skeleton that demonstrates various features of the vitest testing framework.", () => {
  expect([]).toStrictEqual([])
  expect(2).toBe(2)
});

// getMorph

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

/*
  father
  hard_mode
  number_of_declines
  route
  lyn_mode
*/

test("This test sends a request for Morph-data for FE4 Lakche.", async () => {
  const game_no = 4;
  const name = "Lakche";
  const kwargs = {"father": "Lex"};
  const morph = await getMorph(game_no, name, kwargs);
  const { currentCls, currentLv, currentStats, maxStats, maxLv } = morph;
  expect(currentCls).toBe("Swordfighter");
  expect(currentLv).toBe(1);
  expect(maxLv).toBe(20);
  expect(currentStats).toStrictEqual(
    [
      ["HP", 30_00],
      ["Str", 10_00],
      ["Mag", 0],
      ["Skl", 13_00],
      ["Spd", 13_00],
      ["Lck", 8_00],
      ["Def", 7_00],
      ["Res", 0],
    ]
  );
  expect(maxStats).toStrictEqual(
    [
      ["HP", 80_00],
      ["Str", 22_00],
      ["Mag", 15_00],
      ["Skl", 25_00],
      ["Spd", 25_00],
      ["Lck", 30_00],
      ["Def", 20_00],
      ["Res", 15_00],
    ]
  )
});

test("This test sends an unsuccessful request for Morph-data for FE4 Lakche.", async () => {
  const game_no = 4;
  const name = "Lakche";
  const kwargs = {};
  const morph = await getMorph(game_no, name, kwargs);
  const { missingParams } = morph;
  const fatherList = [
    "Arden",
    "Azel",
    "Alec",
    "Claude",
    "Jamka",
    "Dew",
    "Noish",
    "Fin",
    "Beowolf",
    "Holyn",
    "Midayle",
    "Levin",
    "Lex",
  ];
  expect(missingParams["father"]).toStrictEqual(fatherList);
});

test("This test sends an unsuccessful request for Morph-data for FE6 Rutger.", async () => {
  const game_no = 6;
  const name = "Rutger";
  const kwargs = {};
  const morph = await getMorph(game_no, name, kwargs);
  const { missingParams } = morph;
  expect(missingParams["hard_mode"]).toStrictEqual([false, true]);
});

test("This test sends a successful request for Morph-data for FE6 Rutger.", async () => {
  const game_no = 6;
  const name = "Rutger";
  const kwargs = {"hard_mode": true};
  const morph = await getMorph(game_no, name, kwargs);
  const { missingParams } = morph;
  expect(missingParams).toBe(undefined);
});

test("This test sends an unsuccessful request for Morph-data for FE6 Hugh.", async () => {
  const game_no = 6;
  const name = "Hugh";
  const kwargs = {};
  const morph = await getMorph(game_no, name, kwargs);
  const { missingParams } = morph;
  expect(missingParams["number_of_declines"]).toStrictEqual([0, 1, 2, 3]);
});

test("This test sends an unsuccessful request for Morph-data for FE6 Hugh.", async () => {
  const game_no = 6;
  const name = "Hugh";
  const kwargs = {"number_of_declines": 3};
  const morph = await getMorph(game_no, name, kwargs);
  const { missingParams } = morph;
  expect(missingParams).toBe(undefined);
});

test("This test sends another unsuccessful request for Morph-data for FE6 Hugh.", async () => {
  const game_no = 6;
  const name = "Hugh";
  const kwargs = {"number_of_declines": 4};
  const morph = await getMorph(game_no, name, kwargs);
  const { missingParams } = morph;
  expect(missingParams).not.toBe(undefined);
});

test("This test sends a successful request for Morph-data for FE6 Gonzales.", async () => {
  const game_no = 6;
  const name = "Gonzales";
  const kwargs = {"hard_mode": false, "route": "Lalum"};
  const morph = await getMorph(game_no, name, kwargs);
  const { missingParams } = morph;
  expect(missingParams).toBe(undefined);
});

test("This test sends an unsuccessful request for Morph-data for FE6 Gonzales.", async () => {
  const game_no = 6;
  const name = "Gonzales";
  const kwargs = {"hard_mode": false};
  const morph = await getMorph(game_no, name, kwargs);
  const { missingParams } = morph;
  expect(missingParams["route"]).toStrictEqual(["Lalum", "Elphin"]);
});

test("This test sends an unsuccessful request for Morph-data for FE7 Lyn.", async () => {
  const game_no = 7;
  const name = "Lyn";
  const kwargs = {};
  const morph = await getMorph(game_no, name, kwargs);
  const { missingParams } = morph;
  expect(missingParams["lyn_mode"]).toStrictEqual([false, true]);
});

test("This test sends a request for Morph-data for FE7 Ninian.", async () => {
  const game_no = 7;
  const name = "Ninian";
  const kwargs = {};
  const morph = await getMorph(game_no, name, kwargs);
  const { missingParams } = morph;
  expect(missingParams).toBe(undefined);
});

test("This test sends a request for Morph-data for FE7 Nils.", async () => {
  const game_no = 7;
  const name = "Nils";
  // NOTE: I will have to exclude him.
  const kwargs = {};
  const morph = await getMorph(game_no, name, kwargs);
  const { missingParams } = morph;
  expect(missingParams["lyn_mode"]).toStrictEqual([false, true]);
});


test("This test sends another unsuccessful request for Morph-data for FE6 Hugh.", async () => {
  const game_no = 8;
  const name = "Lyon";
  const kwargs = {};
  const morph = await getMorph(game_no, name, kwargs);
  const { missingParams } = morph;
  expect(missingParams).toBe(undefined);
});

test("This test sends a request for Morph-data for a game that the aenir interface does not encompass.", async () => {
  const game_no = 10;
  const name = "Ike";
  // NOTE: I will have to exclude him.
  const kwargs = {};
  const morph = await getMorph(game_no, name, kwargs);
  const { error } = morph;
  expect(error).toBe("INVALID_GAME");
});

test("This test sends a request for Morph-data for a unit that doesn't exist in any of the games that aenir encompasses.", async () => {
  const game_no = 7;
  const name = "Marth";
  // NOTE: I will have to exclude him.
  const kwargs = {};
  const morph = await getMorph(game_no, name, kwargs);
  const { error } = morph;
  expect(error).toBe("UNIT_DNE");
});

test("This test affirms that invalid options are ignored.", async () => {
  const game_no = 6;
  const name = "Roy";
  const kwargs = {"nonsensical": "stuff"};
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

// previewMorph
