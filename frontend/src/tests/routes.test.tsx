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

describe("GameSelect", () => {

  it("lists all game-ID's.", () => {
  });

  it("lists game titles.", () => {
  });

  it("renders images of each game.", () => {
  });

});

describe("UnitSelect", () => {

  it("shows the images of all units.", () => {
  });

  it("shows the names of all units.", () => {
  });

});

describe("UnitConfirm", () => {

  it("shows the image of the selected unit.", () => {
  });

  it("shows the class and level of the selected unit.", () => {
  });

  it("shows the stats of the selected unit.", () => {
  });

  it("allows the user to toggle the initialization options (father, hard_mode, lyn_mode, route, number_of_declines), the stats changing in accordance with the selection.", () => {
  });

});

/* TODO
Root
GameSelect:
- lists game-ID's
- lists titles
- shows images of each game
UnitSelect
- shows unit image
- shows unit name
- shows unit class and level
UnitConfirm
- shows unit image
- shows unit name
- shows unit class and level
- shows unit stats
- allows user to toggle options and the like
*/
