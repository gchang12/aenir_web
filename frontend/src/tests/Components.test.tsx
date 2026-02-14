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
  previewMorph,
} from "../lib/functions";
import {
  StatTable,
} from "../lib/Components";

class FE6Roster {

  static getRoy() {
    return {
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
    };
  };

  static getMarcus() {
    return {
      unitClass: "Paladin",
      level: [1, 20],
      stats: [
        ["HP", 32, 60, 80],
        ["Pow", 9, 25, 30],
        ["Skl", 14, 28, 30],
        ["Spd", 11, 25, 30],
        ["Lck", 10, 30, 30],
        ["Def", 9, 25, 30],
        ["Res", 8, 25, 30],
        ["Con", 11, 20, 20],
        ["Mov", 8, 15, 15],
      ],
    };
  };

  static getRutger(hard_mode) {
    switch(hard_mode) {
      case null:
        return {missingParams: {hard_mode: [false, true]}};
      case "false":
        return {
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
      case "true":
        return {
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
      default:
        return;
    };
  };

  static getHugh(number_of_declines) {
    switch(number_of_declines) {
      case "0":
        return {
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
      case "2":
        return {
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
      default:
        return {missingParams: {number_of_declines: [0, 1, 2, 3]}};
    };
  };

  static getGonzales(route, hard_mode) {
    if (route == null || hard_mode == null) {
      let morph = {missingParams: {}};
      if (route == null) {
        morph.missingParams["route"] = ["Lalum", "Elphin"];
      };
      if (hard_mode == null) {
        morph.missingParams["hard_mode"] = [false, true];
      };
      return morph;
    };
    if (route !== "Lalum") {
      return;
    } else {
      switch(hard_mode) {
        case "false":
          return {
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
        case "true":
          return {
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
        default:
          return;
      };
    };
  };

};

class FE4Roster {

  // FE4
  static getLakche(father) {
    switch(father) {
      case null:
        return {missingParams: {father: [
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
      case "Lex":
        return {
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
      case "Claude":
        return {
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
      case "Arden":
        return {
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
      default:
        return;
    };
  };

};

class FE7Roster {

  static getNinian(lyn_mode) {
    switch(lyn_mode) {
      case null:
        return {missingParams: undefined};
      default:
        return;
    };
  };

  static getNils(lyn_mode) {
    switch(lyn_mode) {
      case null:
        return {missingParams: {lyn_mode: [false, true]}};
      case "true":
        return {
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
      case "false":
        return {
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
      default:
        return;
    };
 };

 static getLyn(lyn_mode) {
   switch(lyn_mode) {
     case null:
       return {missingParams: {lyn_mode: [false, true]}};
     case "false":
       return {
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
     case "true":
       return {
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
  };

  static getMarth() {
    return {error: "UNIT_DNE"};
  };

};

class FE8Roster {

  static getLyon() {
    return undefined;
  };

};

class FE10Roster {

  static getIke() {
    return {error: "INVALID_GAME"};
  };

};

const server = setupServer(
  http.get("http://localhost:8000/dracogate/api/morphs/", ({request}) => {
    const url = new URL(request.url);
    // mandatory parameters
    const game_no = url.searchParams.get("game_no");
    const name = url.searchParams.get("name");
    // optional parameters
    const lyn_mode = url.searchParams.get("lyn_mode");
    const father = url.searchParams.get("father");
    const hard_mode = url.searchParams.get("hard_mode");
    const number_of_declines = url.searchParams.get("number_of_declines");
    const route = url.searchParams.get("route");
    // Initialize blank morph
    let morph;

    switch(game_no) {
      case "6":
        switch(name) {
          case "Roy":
            morph = FE6Roster.getRoy();
            break;
          case "Marcus":
            morph = FE6Roster.getMarcus();
            break;
          case "Rutger":
            morph = FE6Roster.getRutger(hard_mode);
            break;
          case "Hugh":
            morph = FE6Roster.getHugh(number_of_declines);
            break;
          case "Gonzales":
            morph = FE6Roster.getGonzales(route, hard_mode);
            break;
        };
        break;
      case "4":
        switch(name) {
          case "Lakche":
            morph = FE4Roster.getLakche(father);
            break;
        };
      case "7":
        switch(name) {
          case "Ninian":
            morph = FE7Roster.getNinian(lyn_mode);
            break;
          case "Nils":
            morph = FE7Roster.getNils(lyn_mode);
            break;
          case "Lyn":
            morph = FE7Roster.getLyn(lyn_mode);
            break;
          case "Marth":
            morph = FE7Roster.getMarth();
            break;
        };
      case "8":
        switch (name) {
          case "Lyon":
            morph = FE8Roster.getLyon();
            break;
        };
      case "10":
        switch(name) {
          case "Ike":
            morph = FE10Roster.getIke();
            break;
        };
    };

    return HttpResponse.json(morph);
  })
);


describe("StatTable", () => {

  beforeAll(() => server.listen()); afterEach(() => server.resetHandlers()); afterAll(() => server.close());

  it("should reload stats upon navigation.", async () => {
    let {morph, missingParams} = await previewMorph(6, "Roy", {});
    console.log(morph, missingParams);
    render(<table><tbody><StatTable stats={morph.stats} highlight={false} /></tbody></table>);
    // HP=18
    expect(screen.getByText("18")).toBeInTheDocument();
    ({morph, missingParams} = await previewMorph(6, "Marcus", {}));
    console.log(morph, typeof morph, missingParams);
    render(<table><tbody><StatTable stats={morph.stats} highlight={false} /></tbody></table>);
    // HP=32
    expect(screen.getByText("32")).toBeInTheDocument();
  });

});


