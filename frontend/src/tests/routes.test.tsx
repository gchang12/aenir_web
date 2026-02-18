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
    expect(0).toBe(1);
  });

  it("lists game titles.", () => {
    expect(0).toBe(1);
  });

  it("renders images of each game.", () => {
    expect(0).toBe(1);
  });

  it("contains links that lead the user to the expected destination.", () => {
    expect(0).toBe(1);
  });

});

describe("UnitSelect", () => {

  it("shows the images of all units.", () => {
    expect(0).toBe(1);
  });

  it("shows the names of all units.", () => {
    expect(0).toBe(1);
  });

  it("affirms that the expected destinations contain the expected content", () => {
    expect(0).toBe(1);
  });

});

describe("UnitConfirm", () => {

  it("shows the image of the selected unit.", () => {
    expect(0).toBe(1);
  });

  it("shows the class and level of the selected unit.", () => {
    expect(0).toBe(1);
  });

  it("shows the stats of the selected unit.", () => {
    expect(0).toBe(1);
  });

  it("allows the user to toggle the initialization options (father, hard_mode, lyn_mode, route, number_of_declines), the stats changing in accordance with the selection.", () => {
    expect(0).toBe(1);
  });

  it("allows the user to toggle Gonzales' initialization options.", () => {
    expect(0).toBe(1);
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
