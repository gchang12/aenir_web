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

  test("successful request for stat-data.", async () => {
    const game_no = 6;
    const name = "Roy";
    const kwargs = {};
    const morph = await getMorph(game_no, name, kwargs);
    const { unitClass, level, stats } = morph;
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
  test("input of invalid options and that they are ignored.", async () => {
    const game_no = 6;
    const name = "Roy";
    const kwargs = {"nonsensical": "stuff"};
    const morph = await getMorph(game_no, name, kwargs);
    const { unitClass, level, stats } = morph;
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
    http.get("http://localhost:8000/dracogate/api/morphs/", ({params, request}) => {
      const {game_no, name} = params;
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
      };
      return HttpResponse.json(morph);
    })
  );

  beforeAll(() => server.listen()); afterEach(() => server.resetHandlers()); afterAll(() => server.close());

  test("successful request for stat-data.", async () => {
    const game_no = 4;
    const name = "Lakche";
    const kwargs = {"father": "Lex"};
    const morph = await getMorph(game_no, name, kwargs);
    const { unitClass, level, stats } = morph;
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
    expect(missingParams["father"]).toEqual(fatherList);
  });
});

// hard_mode
describe("FE6 Rutger", () => {

  const server = setupServer(
    http.get("http://localhost:8000/dracogate/api/morphs/", ({params, request}) => {
      const {game_no, name} = params;
      const url = new URL(request.url);
      const hard_mode = url.searchParams.get("hard_mode");
      let morph;
      if (hard_mode == null) {
        morph = {missingParams: {hard_mode: [false, true]}};
      } else {
        morph = {unitClass: "", level: [0, 0], stats: []};
      };
      return HttpResponse.json(morph);
    })
  );

  beforeAll(() => server.listen()); afterEach(() => server.resetHandlers()); afterAll(() => server.close());

  test("unsuccessful request for stat-data.", async () => {
    const game_no = 6;
    const name = "Rutger";
    const kwargs = {};
    const morph = await getMorph(game_no, name, kwargs);
    const { missingParams } = morph;
    expect(missingParams["hard_mode"]).toEqual([false, true]);
  });
  test("successful request for stat-data.", async () => {
    const game_no = 6;
    const name = "Rutger";
    const kwargs = {"hard_mode": true};
    const morph = await getMorph(game_no, name, kwargs);
    const { missingParams } = morph;
    expect(missingParams).toBeUndefined();
  });
});

//  number_of_declines
describe("FE6 Hugh", () => {

  const server = setupServer(
    http.get("http://localhost:8000/dracogate/api/morphs/", ({params, request}) => {
      const {game_no, name} = params;
      const url = new URL(request.url);
      const number_of_declines = url.searchParams.get("number_of_declines");
      let morph;
      if (!["0", "1", "2", "3"].includes(number_of_declines)) {
        morph = {missingParams: {number_of_declines: [0, 1, 2, 3]}};
      } else {
        morph = {unitClass: "", level: [0, 0], stats: []};
      };
      return HttpResponse.json(morph);
    })
  );

  beforeAll(() => server.listen()); afterEach(() => server.resetHandlers()); afterAll(() => server.close());

  test("unsuccessful request for stat-data.", async () => {
    const game_no = 6;
    const name = "Hugh";
    const kwargs = {};
    const morph = await getMorph(game_no, name, kwargs);
    const { missingParams } = morph;
    expect(missingParams["number_of_declines"]).toEqual([0, 1, 2, 3]);
  });
  test("successful request for stat-data.", async () => {
    const game_no = 6;
    const name = "Hugh";
    const kwargs = {"number_of_declines": 3};
    const morph = await getMorph(game_no, name, kwargs);
    const { missingParams } = morph;
    expect(missingParams).toBeUndefined();
  });
  test("another unsuccessful request for stat-data, providing an invalid option-value.", async () => {
    const game_no = 6;
    const name = "Hugh";
    const kwargs = {"number_of_declines": 4};
    const morph = await getMorph(game_no, name, kwargs);
    const { missingParams } = morph;
    expect(missingParams).not.toBeUndefined();
  });
});

// route
describe("FE6 Gonzales", () => {

  const server = setupServer(
    http.get("http://localhost:8000/dracogate/api/morphs/", ({params, request}) => {
      const {game_no, name} = params;
      const url = new URL(request.url);
      const hard_mode = url.searchParams.get("hard_mode");
      const route = url.searchParams.get("route");
      let morph;
      if (route == null || hard_mode == null) {
        morph = {};
        morph.missingParams = {};
        if (route == null) {
          morph.missingParams["route"] = ["Lalum", "Elphin"];
        };
        if (hard_mode == null) {
          morph.missingParams["hard_mode"] = [false, true];
        };
      };
      return HttpResponse.json(morph);
    })
  );

  beforeAll(() => server.listen()); afterEach(() => server.resetHandlers()); afterAll(() => server.close());

  test("successful request for stat-data.", async () => {
    const game_no = 6;
    const name = "Gonzales";
    const kwargs = {"hard_mode": false, "route": "Lalum"};
    const morph = await getMorph(game_no, name, kwargs);
    const { missingParams } = morph;
    expect(missingParams).toBeUndefined();
  });
  test("unsuccessful request for stat-data, with 'route' parameter missing.", async () => {
    const game_no = 6;
    const name = "Gonzales";
    const kwargs = {"hard_mode": false};
    const morph = await getMorph(game_no, name, kwargs);
    const { missingParams } = morph;
    expect(missingParams["route"]).toEqual(["Lalum", "Elphin"]);
  });
  test("unsuccessful request for stat-data, with 'hard_mode' parameter missing.", async () => {
    const game_no = 6;
    const name = "Gonzales";
    const kwargs = {};
    const morph = await getMorph(game_no, name, kwargs);
    const { missingParams } = morph;
    expect(missingParams["route"]).toEqual(["Lalum", "Elphin"]);
    expect(missingParams["hard_mode"]).toEqual([false, true]);
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

  test("successful request for stat-data.", async () => {
    const game_no = 7;
    const name = "Ninian";
    const kwargs = {};
    const morph = await getMorph(game_no, name, kwargs);
    const { missingParams } = morph;
    expect(missingParams).toBeUndefined();
  });
});

// lyn_mode
describe("FE7 Nils", () => {

  const server = setupServer(
    http.get("http://localhost:8000/dracogate/api/morphs/", ({params, request}) => {
      const {game_no, name} = params;
      const lyn_mode = new URL(request.url).searchParams.get("lyn_mode");
      let morph;
      if (lyn_mode == null) {
        morph = {missingParams: {lyn_mode: [false, true]}};
      } else {
        morph = {unitClass: "", level: [0, 0], stats: []};
      };
      return HttpResponse.json(morph);
    })
  );

  beforeAll(() => server.listen()); afterEach(() => server.resetHandlers()); afterAll(() => server.close());

  test("unsuccessful request for stat-data.", async () => {
    const game_no = 7;
    const name = "Nils";
    const kwargs = {};
    const morph = await getMorph(game_no, name, kwargs);
    const { missingParams } = morph;
    expect(missingParams["lyn_mode"]).toEqual([false, true]);
  });
  test("successful request for stat-data.", async () => {
    const game_no = 7;
    const name = "Nils";
    const kwargs = {"lyn_mode": false};
    const morph = await getMorph(game_no, name, kwargs);
    const { missingParams } = morph;
    expect(missingParams).toBeUndefined();
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

  test("a successful request for stat-data for an FE8 bonus unit.", async () => {
    const game_no = 8;
    const name = "Lyon";
    const kwargs = {};
    const morph = await getMorph(game_no, name, kwargs);
    const { missingParams } = morph;
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

  test("unsuccessful request for a game that aenir does not encompass.", async () => {
    const game_no = 10;
    const name = "Ike";
    const kwargs = {};
    const morph = await getMorph(game_no, name, kwargs);
    const { error } = morph;
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

  test("unsuccessful request for a unit that DNE.", async () => {
    const game_no = 7;
    const name = "Marth";
    const kwargs = {};
    const morph = await getMorph(game_no, name, kwargs);
    const { error } = morph;
    expect(error).toBe("UNIT_DNE");
  });
});

describe("FE7 Lyn", () => {

  const server = setupServer(
    http.get("http://localhost:8000/dracogate/api/morphs/", ({params}) => {
      const {game_no, name, lyn_mode} = params;
      let morph = {missingParams: {}};
      if (lyn_mode == null) {
        morph.missingParams["lyn_mode"] = [false, true];
      };
      return HttpResponse.json(morph);
    })
  );

  beforeAll(() => server.listen()); afterEach(() => server.resetHandlers()); afterAll(() => server.close());

  test("unsuccessful request for stat-data, with 'lyn_mode' parameter missing..", async () => {
    const game_no = 7;
    const name = "Lyn";
    const kwargs = {};
    const morph = await getMorph(game_no, name, kwargs);
    const { missingParams } = morph;
    expect(missingParams["lyn_mode"]).toEqual([false, true]);
  });
});

// previewMorph
