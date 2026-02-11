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

// TEST SKELETON

test("This is a test skeleton that demonstrates various features of the vitest testing framework.", () => {
  expect([]).toStrictEqual([])
  expect(2).toBe(2)
});

// getMorph

describe("FE6 Roy", () => {
  test("successful request for stat-data.", async () => {
    const game_no = 6;
    const name = "Roy";
    const kwargs = {};
    const morph = await getMorph(game_no, name, kwargs);
    const { unitClass, level, stats } = morph;
    expect(unitClass).toBe("Lord");
    expect(level).toStrictEqual([1, 20]);
    expect(stats).toStrictEqual(
      [
        ["HP", 18, 60, 80],
        ["Pow", 5, 20, 30],
        ["Skl", 5, 20, 30],
        ["Spd", 7, 20, 30],
        ["Lck", 7, 30, 30],
        ["Def", 5, 20, 30],
        ["Res", 0, 20, 30],
        ["Con", 6, 20, 25],
        ["Mov", 5, 15, 15],
      ]
    );
  });
  test("input of invalid options and that they are ignored.", async () => {
    const game_no = 6;
    const name = "Roy";
    const kwargs = {"nonsensical": "stuff"};
    const morph = await getMorph(game_no, name, kwargs);
    const { unitClass, level, stats } = morph;
    expect(unitClass).toBe("Lord");
    expect(level).toStrictEqual([1, 20]);
    expect(stats).toStrictEqual(
      [
        ["HP", 18, 60, 80],
        ["Pow", 5, 20, 30],
        ["Skl", 5, 20, 30],
        ["Spd", 7, 20, 30],
        ["Lck", 7, 30, 30],
        ["Def", 5, 20, 30],
        ["Res", 0, 20, 30],
        ["Con", 6, 20, 25],
        ["Mov", 5, 15, 15],
      ]
    );
  });
});

/*
  father
  hard_mode
  number_of_declines
  route
  lyn_mode
*/

describe("FE4 Lakche", () => {
  test("successful request for stat-data.", async () => {
    const game_no = 4;
    const name = "Lakche";
    const kwargs = {"father": "Lex"};
    const morph = await getMorph(game_no, name, kwargs);
    const { unitClass, level, stats } = morph;
    expect(unitClass).toBe("Swordfighter");
    expect(level).toStrictEqual([1, 20]);
    expect(stats).toStrictEqual(
      [
        ["HP", 30, 80, 80],
        ["Str", 10, 22, 30],
        ["Mag", 0, 15, 30],
        ["Skl", 13, 25, 30],
        ["Spd", 13, 25, 30],
        ["Lck", 8, 30, 30],
        ["Def", 7, 20, 30],
        ["Res", 0, 15, 30],
      ]
    );
  });
  test("unsuccessful request for stat-data.", async () => {
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
});

describe("FE6 Rutger", () => {
  test("unsuccessful request for stat-data.", async () => {
    const game_no = 6;
    const name = "Rutger";
    const kwargs = {};
    const morph = await getMorph(game_no, name, kwargs);
    const { missingParams } = morph;
    expect(missingParams["hard_mode"]).toStrictEqual([false, true]);
  });
  test("successful request for stat-data.", async () => {
    const game_no = 6;
    const name = "Rutger";
    const kwargs = {"hard_mode": true};
    const morph = await getMorph(game_no, name, kwargs);
    const { missingParams } = morph;
    expect(missingParams).toBe(undefined);
  });
});

describe("FE6 Hugh", () => {
  test("unsuccessful request for stat-data.", async () => {
    const game_no = 6;
    const name = "Hugh";
    const kwargs = {};
    const morph = await getMorph(game_no, name, kwargs);
    const { missingParams } = morph;
    expect(missingParams["number_of_declines"]).toStrictEqual([0, 1, 2, 3]);
  });
  test("successful request for stat-data.", async () => {
    const game_no = 6;
    const name = "Hugh";
    const kwargs = {"number_of_declines": 3};
    const morph = await getMorph(game_no, name, kwargs);
    const { missingParams } = morph;
    expect(missingParams).toBe(undefined);
  });
  test("another unsuccessful request for stat-data, providing an invalid option-value.", async () => {
    const game_no = 6;
    const name = "Hugh";
    const kwargs = {"number_of_declines": 4};
    const morph = await getMorph(game_no, name, kwargs);
    const { missingParams } = morph;
    expect(missingParams).not.toBe(undefined);
  });
});

describe("FE6 Gonzales", () => {
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
});

describe("FE7 Ninian", () => {
  test("successful request for stat-data.", async () => {
    const game_no = 7;
    const name = "Ninian";
    const kwargs = {};
    const morph = await getMorph(game_no, name, kwargs);
    const { missingParams } = morph;
    expect(missingParams).toBe(undefined);
  });
});

describe("FE7 Nils", () => {
  test("unsuccessful request for stat-data.", async () => {
    const game_no = 7;
    const name = "Nils";
    const kwargs = {};
    const morph = await getMorph(game_no, name, kwargs);
    const { missingParams } = morph;
    expect(missingParams["lyn_mode"]).toStrictEqual([false, true]);
  });

  test("successful request for stat-data.", async () => {
    const game_no = 7;
    const name = "Nils";
    const kwargs = {"lyn_mode": false};
    const morph = await getMorph(game_no, name, kwargs);
    const { missingParams } = morph;
    expect(missingParams).toBe(undefined);
  });
});


test("This test sends another successful request for Morph-data for FE6 Lyon.", async () => {
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

test("This test sends an unsuccessful request for Morph-data for FE7 Lyn.", async () => {
  const game_no = 7;
  const name = "Lyn";
  const kwargs = {};
  const morph = await getMorph(game_no, name, kwargs);
  const { missingParams } = morph;
  expect(missingParams["lyn_mode"]).toStrictEqual([false, true]);
});

// previewMorph
