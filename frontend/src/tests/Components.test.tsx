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

import {
  server,
} from "./_fixtures";

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

describe("OptionSelect", () => {

  it("provides options to select for 'hard_mode'.", () => {
    expect(0).toBe(1);
  });

  it("provides options to select for 'father'.", () => {
    expect(0).toBe(1);
  });

  it("provides options to select for 'lyn_mode'.", () => {
    expect(0).toBe(1);
  });

  it("provides options to select for 'route'.", () => {
    expect(0).toBe(1);
  });

  it("provides options to select for 'number_of_declines'.", () => {
    expect(0).toBe(1);
  });

});

describe("ProfileHead", () => {

  it("displays the portrait-image and children provided.", () => {
    expect(0).toBe(1);
  });

});

describe("ProfileLevelAndClass", () => {

  it("displays the level and class of the unit.", () => {
    expect(0).toBe(1);
  });

});

describe("StatTable", () => {

  it("shows the stats and names thereof.", () => {
    expect(0).toBe(1);
  });

});
