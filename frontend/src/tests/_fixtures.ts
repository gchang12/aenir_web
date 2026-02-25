import {
  http,
  HttpResponse,
} from "msw";
import {
  setupServer,
} from "msw/node";

export class FE6Roster {
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

export class FE4Roster {
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

export class FE7Roster {
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

export class FE8Roster {
  static getLyon() {
    return undefined;
  };
};

export class FE10Roster {
  static getIke() {
    return {error: "INVALID_GAME"};
  };
};

