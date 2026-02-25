import {
  expect,
  test,
  describe,
} from 'vitest';

import {
  getMorph,
  previewMorph,
  createMorph,
} from "../lib/functions";

describe("FE6 Roy", () => {


  const game_no = 6;
  const name = "Roy";

  test("getMorph: successful request for stat-data with stat-validation.", async () => {
    const kwargs = {};
    const morph = await getMorph(game_no, name, kwargs);
    const {unitClass, level, stats} = morph;
    expect(unitClass).toBe("Lord");
    expect(level).toEqual([1, 20]);
    expect(stats).toEqual(
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

  test("getMorph: input of invalid options and that they are ignored.", async () => {
    const kwargs = {"nonsensical": "stuff"};
    const morph = await getMorph(game_no, name, kwargs);
    const {unitClass, level, stats} = morph;
    expect(unitClass).toBe("Lord");
    expect(level).toEqual([1, 20]);
    expect(stats).toEqual(
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

// father
describe("FE4 Lakche", () => {


  const game_no = 4;
  const name = "Lakche";

  test("getMorph: successful request for stat-data with {father:'Lex'}, with stat-validation.", async () => {
    const kwargs = {"father": "Lex"};
    const morph = await getMorph(game_no, name, kwargs);
    const {unitClass, level, stats} = morph;
    expect(unitClass).toBe("Swordfighter");
    expect(level).toEqual([1, 20]);
    expect(stats).toEqual(
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

  test("getMorph: successful request for stat-data with {father:'Claude'}, with stat-validation.", async () => {
    const kwargs = {"father": "Claude"};
    const morph = await getMorph(game_no, name, kwargs);
    const {unitClass, level, stats} = morph;
    expect(unitClass).toBe("Swordfighter");
    expect(level).toEqual([1, 20]);
    expect(stats).toEqual(
      [
        ["HP", 29, 80, 80],
        ["Str", 9, 22, 30],
        ["Mag", 1, 15, 30],
        ["Skl", 13, 25, 30],
        ["Spd", 13, 25, 30],
        ["Lck", 9, 30, 30],
        ["Def", 6, 20, 30],
        ["Res", 1, 15, 30],
      ]
    );
  });

  test("getMorph: unsuccessful request for stat-data.", async () => {
    const kwargs = {};
    const morph = await getMorph(game_no, name, kwargs);
    const {missingParams} = morph;
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
    expect(missingParams["father"]).toEqual(fatherList);
  });

  test("previewMorph: if return-value matches the expected when no kwargs are provided.", async () => {
    const kwargs = {"father": "Arden"};
    const {morph} = await previewMorph(game_no, name, {});
    const morph2 = await getMorph(game_no, name, kwargs);
    expect(morph).toEqual(morph2);
  });

  test("previewMorph: if return-value matches the expected when kwargs are provided.", async () => {
    const kwargs = {"father": "Lex"};
    const {morph} = await previewMorph(game_no, name, kwargs);
    const morph2 = await getMorph(game_no, name, kwargs);
    expect(morph).toEqual(morph2);
  });

  test("previewMorph: if 'missingParams' is returned if kwargs are provided, and if morph is non-null.", async () => {
    const kwargs = {"father": "Claude"};
    const {morph, missingParams} = await previewMorph(game_no, name, kwargs);
    expect(missingParams).toEqual({father: [
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
    ]});
    const {unitClass, level, stats} = morph;
    expect(unitClass).not.toBeUndefined();
    expect(level).not.toBeUndefined();
    expect(stats).not.toBeUndefined();
  });


});

// hard_mode
describe("FE6 Rutger", () => {


  const game_no = 6;
  const name = "Rutger";

  test("getMorph: unsuccessful request for stat-data.", async () => {
    const kwargs = {};
    const morph = await getMorph(game_no, name, kwargs);
    const {missingParams} = morph;
    expect(missingParams["hard_mode"]).toEqual([false, true]);
  });

  test("getMorph: successful request for hard-mode stat-data, with stat-validation.", async () => {
    const kwargs = {"hard_mode": true};
    const morph = await getMorph(game_no, name, kwargs);
    const {unitClass, level, stats} = morph;
    expect(unitClass).toBe("Myrmidon");
    expect(level).toEqual([4, 20]);
    expect(stats).toEqual(
      [
        ["HP", 26, 60, 80],
        ["Pow", 9, 20, 30],
        ["Skl", 14, 20, 30],
        ["Spd", 15, 20, 30],
        ["Lck", 4, 30, 30],
        ["Def", 6, 20, 30],
        ["Res", 1, 20, 30],
        ["Con", 7, 20, 25],
        ["Mov", 5, 15, 15],
      ]
    );
  });

  test("getMorph: successful request for normal-mode stat-data, with stat-validation.", async () => {
    const kwargs = {"hard_mode": false};
    const morph = await getMorph(game_no, name, kwargs);
    const {unitClass, level, stats} = morph;
    expect(unitClass).toBe("Myrmidon");
    expect(level).toEqual([4, 20]);
    expect(stats).toEqual(
      [
        ["HP", 22, 60, 80],
        ["Pow", 7, 20, 30],
        ["Skl", 12, 20, 30],
        ["Spd", 13, 20, 30],
        ["Lck", 2, 30, 30],
        ["Def", 5, 20, 30],
        ["Res", 0, 20, 30],
        ["Con", 7, 20, 25],
        ["Mov", 5, 15, 15],
      ]
    );
  });

  test("previewMorph: if return-value matches the expected when no kwargs are provided.", async () => {
    const kwargs = {"hard_mode": false};
    const {morph} = await previewMorph(game_no, name, {});
    const morph2 = await getMorph(game_no, name, kwargs);
    expect(morph).toEqual(morph2);
  });

  test("previewMorph: if return-value matches the expected when kwargs are provided.", async () => {
    const kwargs = {"hard_mode": false};
    const {morph} = await previewMorph(game_no, name, kwargs);
    const morph2 = await getMorph(game_no, name, kwargs);
    expect(morph).toEqual(morph2);
  });

  test("previewMorph: if 'missingParams' is returned if kwargs are provided, and if morph is non-null.", async () => {
    const kwargs = {"hard_mode": false};
    const {morph, missingParams} = await previewMorph(game_no, name, kwargs);
    expect(missingParams).toEqual({hard_mode: [false, true]});
    const {unitClass, level, stats} = morph;
    expect(unitClass).not.toBeUndefined();
    expect(level).not.toBeUndefined();
    expect(stats).not.toBeUndefined();
  });

});

//  number_of_declines
describe("FE6 Hugh", () => {


  const game_no = 6;
  const name = "Hugh";

  test("getMorph: unsuccessful request for stat-data.", async () => {
    const kwargs = {};
    const morph = await getMorph(game_no, name, kwargs);
    const {missingParams} = morph;
    expect(missingParams["number_of_declines"]).toEqual([0, 1, 2, 3]);
  });

  test("getMorph: successful request for stat-data with stat-validation {number_of_declines: 0}.", async () => {
    const kwargs = {"number_of_declines": 0};
    const morph = await getMorph(game_no, name, kwargs);
    const {unitClass, level, stats} = morph;
    expect(unitClass).toBe("Mage");
    expect(level).toEqual([15, 20]);
    expect(stats).toEqual(
      [
        ["HP", 26, 60, 80],
        ["Pow", 13, 20, 30],
        ["Skl", 11, 20, 30],
        ["Spd", 12, 20, 30],
        ["Lck", 10, 30, 30],
        ["Def", 9, 20, 30],
        ["Res", 9, 20, 30],
        ["Con", 7, 20, 25],
        ["Mov", 5, 15, 15],
      ]
    );
  });

  test("getMorph: successful request for stat-data with stat-validation.", async () => {
    const kwargs = {"number_of_declines": 2};
    const morph = await getMorph(game_no, name, kwargs);
    const {unitClass, level, stats} = morph;
    expect(unitClass).toBe("Mage");
    expect(level).toEqual([15, 20]);
    expect(stats).toEqual(
      [
        ["HP", 24, 60, 80],
        ["Pow", 11, 20, 30],
        ["Skl", 9, 20, 30],
        ["Spd", 10, 20, 30],
        ["Lck", 8, 30, 30],
        ["Def", 7, 20, 30],
        ["Res", 7, 20, 30],
        ["Con", 7, 20, 25],
        ["Mov", 5, 15, 15],
      ]
    );
  });

  test("getMorph: another unsuccessful request for stat-data, providing an invalid option-value.", async () => {
    const kwargs = {"number_of_declines": 4};
    const morph = await getMorph(game_no, name, kwargs);
    const {missingParams} = morph;
    expect(missingParams).not.toBeUndefined();
  });

  test("previewMorph: if return-value matches the expected when no kwargs are provided.", async () => {
    const kwargs = {"number_of_declines": 0};
    const {morph} = await previewMorph(game_no, name, {});
    const morph2 = await getMorph(game_no, name, kwargs);
    expect(morph).toEqual(morph2);
  });

  test("previewMorph: if return-value matches the expected when kwargs are provided.", async () => {
    const kwargs = {"number_of_declines": 2};
    const {morph} = await previewMorph(game_no, name, kwargs);
    const morph2 = await getMorph(game_no, name, kwargs);
    expect(morph).toEqual(morph2);
  });

  test("previewMorph: if 'missingParams' is returned if kwargs are provided, and if morph is non-null.", async () => {
    const kwargs = {"number_of_declines": 2};
    const {morph, missingParams} = await previewMorph(game_no, name, kwargs);
    expect(missingParams).toEqual({"number_of_declines": [0, 1, 2, 3]});
    const {unitClass, level, stats} = morph;
    expect(unitClass).not.toBeUndefined();
    expect(level).not.toBeUndefined();
    expect(stats).not.toBeUndefined();
  });

});

// route
describe("FE6 Gonzales", () => {


  const game_no = 6;
  const name = "Gonzales";

  test("getMorph: successful request for stat-data.", async () => {
    const kwargs = {"hard_mode": false, "route": "Lalum"};
    const morph = await getMorph(game_no, name, kwargs);
    const {missingParams} = morph;
    expect(missingParams).toBeUndefined();
  });

  test("getMorph: successful request for stat-data, with stat-validation.", async () => {
    const kwargs = {"hard_mode": false, "route": "Lalum"};
    const morph = await getMorph(game_no, name, kwargs);
    const {unitClass, level, stats} = morph;
    expect(unitClass).toBe("Bandit");
    expect(level).toEqual([5, 20]);
    expect(stats).toEqual(
      [
        ["HP", 36, 60, 80],
        ["Pow", 12, 20, 30],
        ["Skl", 5, 20, 30],
        ["Spd", 9, 20, 30],
        ["Lck", 5, 30, 30],
        ["Def", 6, 20, 30],
        ["Res", 0, 20, 30],
        ["Con", 15, 20, 25],
        ["Mov", 5, 15, 15],
      ]
    );
  });

  test("getMorph: successful request for hard-mode stat-data, with stat-validation.", async () => {
    const kwargs = {"hard_mode": true, "route": "Lalum"};
    const morph = await getMorph(game_no, name, kwargs);
    const {unitClass, level, stats} = morph;
    expect(unitClass).toBe("Bandit");
    expect(level).toEqual([5, 20]);
    expect(stats).toEqual(
      [
        ["HP", 43, 60, 80],
        ["Pow", 16, 20, 30],
        ["Skl", 7, 20, 30],
        ["Spd", 11, 20, 30],
        ["Lck", 6, 30, 30],
        ["Def", 7, 20, 30],
        ["Res", 1, 20, 30],
        ["Con", 15, 20, 25],
        ["Mov", 5, 15, 15],
      ]
    );
  });

  test("getMorph: unsuccessful request for stat-data, with 'route' parameter missing.", async () => {
    const kwargs = {"hard_mode": false};
    const morph = await getMorph(game_no, name, kwargs);
    const {missingParams} = morph;
    expect(missingParams["route"]).toEqual(["Lalum", "Elphin"]);
  });

  test("getMorph: unsuccessful request for stat-data, with 'hard_mode' parameter missing.", async () => {
    const kwargs = {};
    const morph = await getMorph(game_no, name, kwargs);
    const {missingParams} = morph;
    expect(missingParams["route"]).toEqual(["Lalum", "Elphin"]);
    expect(missingParams["hard_mode"]).toEqual([false, true]);
  });

  test("previewMorph: if return-value matches the expected when no kwargs are provided.", async () => {
    const kwargs = {"hard_mode": false, "route": "Lalum"};
    const {morph} = await previewMorph(game_no, name, {});
    const morph2 = await getMorph(game_no, name, kwargs);
    expect(morph).toEqual(morph2);
  });

  test("previewMorph: if return-value matches the expected when kwargs are provided.", async () => {
    const kwargs = {"hard_mode": true, "route": "Elphin"};
    const {morph} = await previewMorph(game_no, name, kwargs);
    const morph2 = await getMorph(game_no, name, kwargs);
    expect(morph).toEqual(morph2);
  });

  test("previewMorph: if 'missingParams' is returned if kwargs are provided, and if morph is non-null.", async () => {
    const kwargs = {"hard_mode": true, "route": "Lalum"};
    const {morph, missingParams} = await previewMorph(game_no, name, kwargs);
    expect(missingParams).toEqual({"hard_mode": [false, true], "route": ["Lalum", "Elphin"]});
    const {unitClass, level, stats} = morph;
    expect(unitClass).not.toBeUndefined();
    expect(level).not.toBeUndefined();
    expect(stats).not.toBeUndefined();
  });

});

describe("FE7 Ninian", () => {


  const game_no = 7;
  const name = "Ninian";

  test("getMorph: successful request for stat-data.", async () => {
    const kwargs = {};
    const morph = await getMorph(game_no, name, kwargs);
    const {missingParams} = morph;
    expect(missingParams).toBeUndefined();
  });

});

// lyn_mode
describe("FE7 Nils", () => {


  const game_no = 7;
  const name = "Nils";

  test("getMorph: unsuccessful request for stat-data.", async () => {
    const kwargs = {};
    const morph = await getMorph(game_no, name, kwargs);
    const {missingParams} = morph;
    expect(missingParams["lyn_mode"]).toEqual([false, true]);
  });

  test("getMorph: successful request for stat-data with stat-validation.", async () => {
    const kwargs = {"lyn_mode": false};
    const morph = await getMorph(game_no, name, kwargs);
    const {unitClass, level, stats} = morph;
    expect(unitClass).toBe("Bard");
    expect(level).toEqual([1, 20]);
    expect(stats).toEqual(
      [
        ["HP", 14, 60, 80],
        ["Pow", 0, 10, 30],
        ["Skl", 0, 10, 30],
        ["Spd", 12, 30, 30],
        ["Lck", 10, 30, 30],
        ["Def", 5, 24, 30],
        ["Res", 4, 26, 30],
        ["Con", 3, 20, 25],
        ["Mov", 5, 15, 15],
      ]
    );
  });

  test("getMorph: successful request for stat-data with stat-validation.", async () => {
    const kwargs = {"lyn_mode": true};
    const morph = await getMorph(game_no, name, kwargs);
    const {unitClass, level, stats} = morph;
    expect(unitClass).toBe("Bard");
    expect(level).toEqual([1, 20]);
    expect(stats).toEqual(
      [
        ["HP", 14, 60, 80],
        ["Pow", 0, 10, 30],
        ["Skl", 0, 10, 30],
        ["Spd", 12, 30, 30],
        ["Lck", 10, 30, 30],
        ["Def", 5, 24, 30],
        ["Res", 4, 26, 30],
        ["Con", 3, 20, 25],
        ["Mov", 5, 15, 15],
      ]
    );
  });

  test("previewMorph: if return-value matches the expected when no kwargs are provided.", async () => {
    const kwargs = {"lyn_mode": false};
    const {morph} = await previewMorph(game_no, name, {});
    const morph2 = await getMorph(game_no, name, kwargs);
    expect(morph).toEqual(morph2);
  });

  test("previewMorph: if return-value matches the expected when kwargs are provided.", async () => {
    const kwargs = {"lyn_mode": true};
    const {morph} = await previewMorph(game_no, name, kwargs);
    const morph2 = await getMorph(game_no, name, kwargs);
    expect(morph).toEqual(morph2);
  });

  test("previewMorph: if 'missingParams' is returned if kwargs are provided, and if morph is non-null.", async () => {
    const kwargs = {"lyn_mode": true};
    const {morph, missingParams} = await previewMorph(game_no, name, kwargs);
    expect(missingParams).toEqual({lyn_mode: [false, true]});
    const {unitClass, level, stats} = morph;
    expect(unitClass).not.toBeUndefined();
    expect(level).not.toBeUndefined();
    expect(stats).not.toBeUndefined();
  });

});

describe("FE8 Lyon", () => {


  const game_no = 8;
  const name = "Lyon";

  test("getMorph: a successful request for stat-data for an FE8 bonus unit.", async () => {
    const kwargs = {};
    const morph = await getMorph(game_no, name, kwargs);
    const {missingParams} = morph;
    expect(missingParams).toBeUndefined();
  });

});

describe("FE10 Ike (DNE)", () => {


  const game_no = 10;
  const name = "Ike";

  test("getMorph: unsuccessful request for a game that aenir does not encompass.", async () => {
    const kwargs = {};
    const morph = await getMorph(game_no, name, kwargs);
    const {error} = morph;
    expect(error).toBe("INVALID_GAME");
  });

  test("previewMorph: if morph contains an error if bad game_no-name pair was provided.", async () => {
    const kwargs = {};
    const {morph, missingParams} = await previewMorph(game_no, name, kwargs);
    expect(missingParams).toBeUndefined();
    const {error} = morph;
    expect(error).toBe("INVALID_GAME");
  });

});

describe("FE7 Marth (DNE)", () => {


  const game_no = 7;
  const name = "Marth";

  test("previewMorph: if morph contains an error if bad game_no-name pair was provided.", async () => {
    const kwargs = {};
    const {morph, missingParams} = await previewMorph(game_no, name, kwargs);
    expect(missingParams).toBeUndefined();
    const {error} = morph;
    expect(error).toBe("UNIT_DNE");
  });

  test("getMorph: unsuccessful request for a unit that DNE.", async () => {
    const kwargs = {};
    const morph = await getMorph(game_no, name, kwargs);
    const {error} = morph;
    expect(error).toBe("UNIT_DNE");
  });

});

describe("FE7 Lyn", () => {


  const game_no = 7;
  const name = "Lyn";

  test("getMorph: unsuccessful request for stat-data, with 'lyn_mode' parameter missing..", async () => {
    const kwargs = {};
    const morph = await getMorph(game_no, name, kwargs);
    const {missingParams} = morph;
    expect(missingParams["lyn_mode"]).toEqual([false, true]);
  });

  test("getMorph: successful request for stat-data with stat-validation.", async () => {
    const kwargs = {"lyn_mode": true};
    const morph = await getMorph(game_no, name, kwargs);
    const {unitClass, level, stats} = morph;
    expect(unitClass).toBe("Lord");
    expect(level).toEqual([1, 20]);
    expect(stats).toEqual(
      [
        ["HP", 16, 60, 80],
        ["Pow", 4, 20, 30],
        ["Skl", 7, 20, 30],
        ["Spd", 9, 20, 30],
        ["Lck", 5, 30, 30],
        ["Def", 2, 20, 30],
        ["Res", 0, 20, 30],
        ["Con", 5, 20, 25],
        ["Mov", 5, 15, 15],
      ]
    );
  });

  test("getMorph: successful request for stat-data with stat-validation.", async () => {
    const kwargs = {"lyn_mode": false};
    const morph = await getMorph(game_no, name, kwargs);
    const {unitClass, level, stats} = morph;
    expect(unitClass).toBe("Lord");
    expect(level).toEqual([4, 20]);
    expect(stats).toEqual(
      [
        ["HP", 18, 60, 80],
        ["Pow", 5, 20, 30],
        ["Skl", 10, 20, 30],
        ["Spd", 11, 20, 30],
        ["Lck", 5, 30, 30],
        ["Def", 2, 20, 30],
        ["Res", 0, 20, 30],
        ["Con", 5, 20, 25],
        ["Mov", 5, 15, 15],
      ]
    );
  });

  test("previewMorph: if return-value matches the expected when no kwargs are provided.", async () => {
    const kwargs = {"lyn_mode": false};
    const {morph} = await previewMorph(game_no, name, {});
    const morph2 = await getMorph(game_no, name, kwargs);
    expect(morph).toEqual(morph2);
  });

  test("previewMorph: if return-value matches the expected when kwargs are provided.", async () => {
    const kwargs = {"lyn_mode": true};
    const {morph} = await previewMorph(game_no, name, kwargs);
    const morph2 = await getMorph(game_no, name, kwargs);
    expect(morph).toEqual(morph2);
  });

  test("previewMorph: if 'missingParams' is returned if kwargs are provided, and if morph is non-null.", async () => {
    const kwargs = {"lyn_mode": true};
    const {morph, missingParams} = await previewMorph(game_no, name, kwargs);
    expect(missingParams).toEqual({lyn_mode: [false, true]});
    const {unitClass, level, stats} = morph;
    expect(unitClass).not.toBeUndefined();
    expect(level).not.toBeUndefined();
    expect(stats).not.toBeUndefined();
  });

});
