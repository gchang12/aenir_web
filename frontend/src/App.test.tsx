import {
  render,
  screen,
} from "@testing-library/react";
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

/*
FE6 Roy (2)
- no change
FE4 Lakche (2)
- write test to display difference in stats.
FE6 Rutger (2)
- write test to display difference in stats.
FE6 Hugh (3)
- write test to display difference in stats.
FE6 Gonzales (3)
- write test to display difference in stats.
FE7 Lyn (1)
- write test to display difference in stats.
FE7 Nils (2)
- write test to display difference in stats.
FE7 Ninian (1)
FE8 Lyon (1)
FE10 Ike (DNE) (1)
FE7 Marth (DNE) (1)
*/

// getMorph(game_no, name, { father, hard_mode, number_of_declines, route, lyn_mode })

describe("FE6 Roy", () => {

  const server = setupServer(
    http.get("http://localhost:8000/dracogate/api/morphs/", () => {
      return HttpResponse.json({
        unitClass: "Lord",
        level: [1, 20],
        stats: [
          ["HP", 18, 60, 80],
          ["Pow", 5, 20, 30],
          ["Skl", 5, 20, 30],
          ["Spd", 7, 20, 30],
          ["Lck", 7, 30, 30],
          ["Def", 5, 20, 30],
          ["Res", 0, 20, 30],
          ["Con", 6, 20, 25],
          ["Mov", 5, 15, 15],
        ],
      });
    })
  );

  beforeAll(() => server.listen()); afterEach(() => server.resetHandlers()); afterAll(() => server.close());

  test("getMorph: successful request for stat-data with stat-validation.", async () => {
    const game_no = 6;
    const name = "Roy";
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
    const game_no = 6;
    const name = "Roy";
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

  const server = setupServer(
    http.get("http://localhost:8000/dracogate/api/morphs/", ({request}) => {
      const father = new URL(request.url).searchParams.get("father");
      let morph;
      if (father == null) {
        morph = {missingParams: {father: [
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
        ]}};
      } else {
      } if (father === "Lex") {
        morph = {
          unitClass: "Swordfighter",
          level: [1, 20],
          stats: [
            ["HP", 30, 80, 80],
            ["Str", 10, 22, 30],
            ["Mag", 0, 15, 30],
            ["Skl", 13, 25, 30],
            ["Spd", 13, 25, 30],
            ["Lck", 8, 30, 30],
            ["Def", 7, 20, 30],
            ["Res", 0, 15, 30],
          ],
        };
      } else if (father === "Claude") {
        morph = {
          unitClass: "Swordfighter",
          level: [1, 20],
          stats: [
            ["HP", 29, 80, 80],
            ["Str", 9, 22, 30],
            ["Mag", 1, 15, 30],
            ["Skl", 13, 25, 30],
            ["Spd", 13, 25, 30],
            ["Lck", 9, 30, 30],
            ["Def", 6, 20, 30],
            ["Res", 1, 15, 30],
          ],
        };
      } else if (father === "Arden") {
        morph = {
          unitClass: "Swordfighter",
          level: [1, 20],
          stats: [
            ["HP", 31, 80, 80],
            ["Str", 10, 22, 30],
            ["Mag", 0, 15, 30],
            ["Skl", 13, 25, 30],
            ["Spd", 13, 25, 30],
            ["Lck", 8, 30, 30],
            ["Def", 7, 20, 30],
            ["Res", 0, 15, 30],
          ],
        };
      };
      return HttpResponse.json(morph);
    })
  );

  beforeAll(() => server.listen()); afterEach(() => server.resetHandlers()); afterAll(() => server.close());

  test("getMorph: successful request for stat-data with {father:'Lex'}, with stat-validation.", async () => {
    const game_no = 4;
    const name = "Lakche";
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
    const game_no = 4;
    const name = "Lakche";
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
    const game_no = 4;
    const name = "Lakche";
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
    const game_no = 4;
    const name = "Lakche";
    const kwargs = {"father": "Arden"};
    const {morph} = await previewMorph(game_no, name, {});
    const morph2 = await getMorph(game_no, name, kwargs);
    expect(morph).toEqual(morph2);
  });

  test("previewMorph: if return-value matches the expected when kwargs are provided.", async () => {
    const game_no = 6;
    const name = "Hugh";
    const kwargs = {"father": "Lex"};
    const {morph} = await previewMorph(game_no, name, kwargs);
    const morph2 = await getMorph(game_no, name, kwargs);
    expect(morph).toEqual(morph2);
  });

  test("previewMorph: if 'missingParams' is returned if kwargs are provided, and if morph is non-null.", async () => {
    const game_no = 6;
    const name = "Hugh";
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

  const server = setupServer(
    http.get("http://localhost:8000/dracogate/api/morphs/", ({request}) => {
      const url = new URL(request.url);
      const hard_mode = url.searchParams.get("hard_mode");
      let morph;
      if (hard_mode == null) {
        morph = {missingParams: {hard_mode: [false, true]}};
      } else {
        if (hard_mode === "false") {
          morph = {
            unitClass: "Myrmidon",
            level: [4, 20],
            stats: [
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
          };
        } else if (hard_mode === "true") {
          morph = {
            unitClass: "Myrmidon",
            level: [4, 20],
            stats: [
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
          };
        };
      }
    return HttpResponse.json(morph);
    })
  )

  beforeAll(() => server.listen()); afterEach(() => server.resetHandlers()); afterAll(() => server.close());

  test("getMorph: unsuccessful request for stat-data.", async () => {
    const game_no = 6;
    const name = "Rutger";
    const kwargs = {};
    const morph = await getMorph(game_no, name, kwargs);
    const {missingParams} = morph;
    expect(missingParams["hard_mode"]).toEqual([false, true]);
  });

  test("getMorph: successful request for hard-mode stat-data, with stat-validation.", async () => {
    const game_no = 6;
    const name = "Rutger";
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
    const game_no = 6;
    const name = "Rutger";
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
    const game_no = 6;
    const name = "Rutger";
    const kwargs = {"hard_mode": false};
    const {morph} = await previewMorph(game_no, name, {});
    const morph2 = await getMorph(game_no, name, kwargs);
    expect(morph).toEqual(morph2);
  });

  test("previewMorph: if return-value matches the expected when kwargs are provided.", async () => {
    const game_no = 6;
    const name = "Hugh";
    const kwargs = {"hard_mode": false};
    const {morph} = await previewMorph(game_no, name, kwargs);
    const morph2 = await getMorph(game_no, name, kwargs);
    expect(morph).toEqual(morph2);
  });

  test("previewMorph: if 'missingParams' is returned if kwargs are provided, and if morph is non-null.", async () => {
    const game_no = 6;
    const name = "Hugh";
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

  const server = setupServer(
    http.get("http://localhost:8000/dracogate/api/morphs/", ({request}) => {
      const url = new URL(request.url);
      const number_of_declines = url.searchParams.get("number_of_declines");
      let morph;
      if (!["0", "1", "2", "3"].includes(number_of_declines)) {
        morph = {missingParams: {number_of_declines: [0, 1, 2, 3]}};
      } else if (number_of_declines === "2") {
        morph = {
          unitClass: "Mage",
          level: [15, 20],
          stats: [
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
        };
      } else if (number_of_declines === "0") {
        morph = {
          unitClass: "Mage",
          level: [15, 20],
          stats: [
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
        };
      };
      return HttpResponse.json(morph);
    })
  );

  beforeAll(() => server.listen()); afterEach(() => server.resetHandlers()); afterAll(() => server.close());

  test("getMorph: unsuccessful request for stat-data.", async () => {
    const game_no = 6;
    const name = "Hugh";
    const kwargs = {};
    const morph = await getMorph(game_no, name, kwargs);
    const {missingParams} = morph;
    expect(missingParams["number_of_declines"]).toEqual([0, 1, 2, 3]);
  });

  test("getMorph: successful request for stat-data with stat-validation {number_of_declines: 0}.", async () => {
    const game_no = 6;
    const name = "Hugh";
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
    const game_no = 6;
    const name = "Hugh";
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
    const game_no = 6;
    const name = "Hugh";
    const kwargs = {"number_of_declines": 4};
    const morph = await getMorph(game_no, name, kwargs);
    const {missingParams} = morph;
    expect(missingParams).not.toBeUndefined();
  });

  test("previewMorph: if return-value matches the expected when no kwargs are provided.", async () => {
    const game_no = 6;
    const name = "Hugh";
    const kwargs = {"number_of_declines": 0};
    const {morph} = await previewMorph(game_no, name, {});
    const morph2 = await getMorph(game_no, name, kwargs);
    expect(morph).toEqual(morph2);
  });

  test("previewMorph: if return-value matches the expected when kwargs are provided.", async () => {
    const game_no = 6;
    const name = "Hugh";
    const kwargs = {"number_of_declines": 2};
    const {morph} = await previewMorph(game_no, name, kwargs);
    const morph2 = await getMorph(game_no, name, kwargs);
    expect(morph).toEqual(morph2);
  });

  test("previewMorph: if 'missingParams' is returned if kwargs are provided, and if morph is non-null.", async () => {
    const game_no = 6;
    const name = "Hugh";
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

  const server = setupServer(
    http.get("http://localhost:8000/dracogate/api/morphs/", ({request}) => {
      const url = new URL(request.url);
      const hard_mode = url.searchParams.get("hard_mode");
      const route = url.searchParams.get("route");
      let morph = {};
      if (route == null || hard_mode == null) {
        morph;
        morph.missingParams = {};
        if (route == null) {
          morph.missingParams["route"] = ["Lalum", "Elphin"];
        };
        if (hard_mode == null) {
          morph.missingParams["hard_mode"] = [false, true];
        };
      } else {
        if (route === "Lalum") {
          if (hard_mode === "false") {
            morph = {
              unitClass: "Bandit",
              level: [5, 20],
              stats: [
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
            };
          } else if (hard_mode === "true") {
            morph = {
              unitClass: "Bandit",
              level: [5, 20],
              stats: [
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
            };
          };
        };
      };
      return HttpResponse.json(morph);
    })
  );

  beforeAll(() => server.listen()); afterEach(() => server.resetHandlers()); afterAll(() => server.close());

  test("getMorph: successful request for stat-data.", async () => {
    const game_no = 6;
    const name = "Gonzales";
    const kwargs = {"hard_mode": false, "route": "Lalum"};
    const morph = await getMorph(game_no, name, kwargs);
    const {missingParams} = morph;
    expect(missingParams).toBeUndefined();
  });

  test("getMorph: successful request for stat-data, with stat-validation.", async () => {
    const game_no = 6;
    const name = "Gonzales";
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
    const game_no = 6;
    const name = "Gonzales";
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
    const game_no = 6;
    const name = "Gonzales";
    const kwargs = {"hard_mode": false};
    const morph = await getMorph(game_no, name, kwargs);
    const {missingParams} = morph;
    expect(missingParams["route"]).toEqual(["Lalum", "Elphin"]);
  });

  test("getMorph: unsuccessful request for stat-data, with 'hard_mode' parameter missing.", async () => {
    const game_no = 6;
    const name = "Gonzales";
    const kwargs = {};
    const morph = await getMorph(game_no, name, kwargs);
    const {missingParams} = morph;
    expect(missingParams["route"]).toEqual(["Lalum", "Elphin"]);
    expect(missingParams["hard_mode"]).toEqual([false, true]);
  });

  test("previewMorph: if return-value matches the expected when no kwargs are provided.", async () => {
    const game_no = 6;
    const name = "Gonzales";
    const kwargs = {"hard_mode": false, "route": "Lalum"};
    const {morph} = await previewMorph(game_no, name, {});
    const morph2 = await getMorph(game_no, name, kwargs);
    expect(morph).toEqual(morph2);
  });

  test("previewMorph: if return-value matches the expected when kwargs are provided.", async () => {
    const game_no = 6;
    const name = "Gonzales";
    const kwargs = {"hard_mode": true, "route": "Elphin"};
    const {morph} = await previewMorph(game_no, name, kwargs);
    const morph2 = await getMorph(game_no, name, kwargs);
    expect(morph).toEqual(morph2);
  });

  test("previewMorph: if 'missingParams' is returned if kwargs are provided, and if morph is non-null.", async () => {
    const game_no = 6;
    const name = "Gonzales";
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

  const server = setupServer(
    http.get("http://localhost:8000/dracogate/api/morphs/", ({params}) => {
      const {game_no, name, lyn_mode} = params;
      let morph;
      if (lyn_mode == null) {
        morph = {missingParams: undefined};
      };
      return HttpResponse.json(morph);
    })
  );

  beforeAll(() => server.listen()); afterEach(() => server.resetHandlers()); afterAll(() => server.close());

  test("getMorph: successful request for stat-data.", async () => {
    const game_no = 7;
    const name = "Ninian";
    const kwargs = {};
    const morph = await getMorph(game_no, name, kwargs);
    const {missingParams} = morph;
    expect(missingParams).toBeUndefined();
  });

});

// lyn_mode
describe("FE7 Nils", () => {

  const server = setupServer(
    http.get("http://localhost:8000/dracogate/api/morphs/", ({request}) => {
      const lyn_mode = new URL(request.url).searchParams.get("lyn_mode");
      let morph;
      if (lyn_mode == null) {
        morph = {missingParams: {lyn_mode: [false, true]}};
      } else {
        morph = {
          unitClass: "Bard",
          level: [1, 20],
          stats: [
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
        };
      };
      return HttpResponse.json(morph);
    })
  );

  beforeAll(() => server.listen()); afterEach(() => server.resetHandlers()); afterAll(() => server.close());

  test("getMorph: unsuccessful request for stat-data.", async () => {
    const game_no = 7;
    const name = "Nils";
    const kwargs = {};
    const morph = await getMorph(game_no, name, kwargs);
    const {missingParams} = morph;
    expect(missingParams["lyn_mode"]).toEqual([false, true]);
  });

  test("getMorph: successful request for stat-data with stat-validation.", async () => {
    const game_no = 7;
    const name = "Nils";
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
    const game_no = 7;
    const name = "Nils";
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
    const game_no = 7;
    const name = "Nils";
    const kwargs = {"lyn_mode": false};
    const {morph} = await previewMorph(game_no, name, {});
    const morph2 = await getMorph(game_no, name, kwargs);
    expect(morph).toEqual(morph2);
  });

  test("previewMorph: if return-value matches the expected when kwargs are provided.", async () => {
    const game_no = 7;
    const name = "Nils";
    const kwargs = {"lyn_mode": true};
    const {morph} = await previewMorph(game_no, name, kwargs);
    const morph2 = await getMorph(game_no, name, kwargs);
    expect(morph).toEqual(morph2);
  });

  test("previewMorph: if 'missingParams' is returned if kwargs are provided, and if morph is non-null.", async () => {
    const game_no = 7;
    const name = "Nils";
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

  const server = setupServer(
    http.get("http://localhost:8000/dracogate/api/morphs/", ({params}) => {
      const {game_no, name} = params;
      let morph;
      return HttpResponse.json(morph);
    })
  );

  beforeAll(() => server.listen()); afterEach(() => server.resetHandlers()); afterAll(() => server.close());

  test("getMorph: a successful request for stat-data for an FE8 bonus unit.", async () => {
    const game_no = 8;
    const name = "Lyon";
    const kwargs = {};
    const morph = await getMorph(game_no, name, kwargs);
    const {missingParams} = morph;
    expect(missingParams).toBeUndefined();
  });

});

describe("FE10 Ike (DNE)", () => {

  const server = setupServer(
    http.get("http://localhost:8000/dracogate/api/morphs/", ({params}) => {
      const {game_no, name} = params;
      let morph = {error: "INVALID_GAME"};
      return HttpResponse.json(morph);
    })
  );

  beforeAll(() => server.listen()); afterEach(() => server.resetHandlers()); afterAll(() => server.close());

  test("getMorph: unsuccessful request for a game that aenir does not encompass.", async () => {
    const game_no = 10;
    const name = "Ike";
    const kwargs = {};
    const morph = await getMorph(game_no, name, kwargs);
    const {error} = morph;
    expect(error).toBe("INVALID_GAME");
  });

  test("previewMorph: if morph contains an error if bad game_no-name pair was provided.", async () => {
    const game_no = 10;
    const name = "Ike";
    const kwargs = {};
    const {morph, missingParams} = await previewMorph(game_no, name, kwargs);
    expect(missingParams).toBeUndefined();
    const {error} = morph;
    expect(error).toBe("INVALID_GAME");
  });

});

describe("FE7 Marth (DNE)", () => {

  const server = setupServer(
    http.get("http://localhost:8000/dracogate/api/morphs/", ({params}) => {
      const {game_no, name} = params;
      let morph = {error: "UNIT_DNE"};
      return HttpResponse.json(morph);
    })
  );

  beforeAll(() => server.listen()); afterEach(() => server.resetHandlers()); afterAll(() => server.close());

  test("previewMorph: if morph contains an error if bad game_no-name pair was provided.", async () => {
    const game_no = 7;
    const name = "Marth";
    const kwargs = {};
    const {morph, missingParams} = await previewMorph(game_no, name, kwargs);
    expect(missingParams).toBeUndefined();
    const {error} = morph;
    expect(error).toBe("UNIT_DNE");
  });

  test("getMorph: unsuccessful request for a unit that DNE.", async () => {
    const game_no = 7;
    const name = "Marth";
    const kwargs = {};
    const morph = await getMorph(game_no, name, kwargs);
    const {error} = morph;
    expect(error).toBe("UNIT_DNE");
  });

});

describe("FE7 Lyn", () => {

  const server = setupServer(
    http.get("http://localhost:8000/dracogate/api/morphs/", ({request}) => {
      const url = new URL(request.url);
      const lyn_mode = url.searchParams.get("lyn_mode");
      let morph;
      if (lyn_mode == null) {
        morph = {missingParams: {lyn_mode: [false, true]}}
      } else {
        if (lyn_mode === "false") {
          morph = {
            unitClass: "Lord",
            level: [4, 20],
            stats: [
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
          };
        } else if (lyn_mode === "true") {
          morph = {
            unitClass: "Lord",
            level: [1, 20],
            stats: [
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
          };
        };
      }
      return HttpResponse.json(morph);
    })
  );

  beforeAll(() => server.listen()); afterEach(() => server.resetHandlers()); afterAll(() => server.close());

  test("getMorph: unsuccessful request for stat-data, with 'lyn_mode' parameter missing..", async () => {
    const game_no = 7;
    const name = "Lyn";
    const kwargs = {};
    const morph = await getMorph(game_no, name, kwargs);
    const {missingParams} = morph;
    expect(missingParams["lyn_mode"]).toEqual([false, true]);
  });

  test("getMorph: successful request for stat-data with stat-validation.", async () => {
    const game_no = 7;
    const name = "Lyn";
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
    const game_no = 7;
    const name = "Lyn";
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
    const game_no = 7;
    const name = "Lyn";
    const kwargs = {"lyn_mode": false};
    const {morph} = await previewMorph(game_no, name, {});
    const morph2 = await getMorph(game_no, name, kwargs);
    expect(morph).toEqual(morph2);
  });

  test("previewMorph: if return-value matches the expected when kwargs are provided.", async () => {
    const game_no = 7;
    const name = "Lyn";
    const kwargs = {"lyn_mode": true};
    const {morph} = await previewMorph(game_no, name, kwargs);
    const morph2 = await getMorph(game_no, name, kwargs);
    expect(morph).toEqual(morph2);
  });

  test("previewMorph: if 'missingParams' is returned if kwargs are provided, and if morph is non-null.", async () => {
    const game_no = 7;
    const name = "Lyn";
    const kwargs = {"lyn_mode": true};
    const {morph, missingParams} = await previewMorph(game_no, name, kwargs);
    expect(missingParams).toEqual({lyn_mode: [false, true]});
    const {unitClass, level, stats} = morph;
    expect(unitClass).not.toBeUndefined();
    expect(level).not.toBeUndefined();
    expect(stats).not.toBeUndefined();
  });

});

function App() {
  return (
    <h1>Hello world</h1>
  );
};

describe("App", () => {
  it("should be in the document.", () => {
    render(<App />);
    expect(screen.getByText("Hello world")).toBeInTheDocument();
  });
});
