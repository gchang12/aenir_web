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
// import { page, } from "vitest/browser";

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
  OptionSelect,
  ProfileLevelAndClass,
  ProfileHead,
} from "../lib/Components";

import {
  server,
} from "./_fixtures";

/* TODO
  - Learn how to query for elements on the page.
  - Learn how to make assertions about attributes of certain elements.
*/

describe("StatTable", () => {

  beforeAll(() => server.listen()); afterEach(() => server.resetHandlers()); afterAll(() => server.close());

  it("should reload stats upon navigation.", async () => {
    let {morph, missingParams} = await previewMorph(6, "Roy", {});
    //console.log(morph, missingParams);
    render(<table><tbody><StatTable stats={morph.stats} highlight={false} /></tbody></table>);
    // HP=18
    expect(screen.getByText("18")).toBeInTheDocument();
    ({morph, missingParams} = await previewMorph(6, "Marcus", {}));
    //console.log(morph, typeof morph, missingParams);
    render(<table><tbody><StatTable stats={morph.stats} highlight={false} /></tbody></table>);
    // HP=32
    expect(screen.getByText("32")).toBeInTheDocument();
  });

  it("shows the stats and names thereof.", () => {
    const stats = [
      ["HP", 10, 50, 99],
      ["Pow", 20, 50, 99],
      ["Spd", 30, 50, 99],
      ["Lck", 40, 50, 99],
      ["Def", 50, 50, 99],
    ];
    render(<table><tbody><StatTable {...{stats}} /></tbody></table>);
    const rowHeaders = screen.getAllByRole("columnheader");
    for (const [indexNo, rowHeader] of Object.entries(rowHeaders)) {
      expect(rowHeader).toHaveTextContent(stats[indexNo][0]);
    };
  });

});

describe("OptionSelect", () => {

  it("provides options to select for 'hard_mode'.", () => {
    const missingParams = {hard_mode: [true, false]};
    render(<table><tbody><OptionSelect {...{missingParams}} /></tbody></table>);
    const role = "checkbox";
    //expect(0).toBe(1);
    expect(screen.getByRole(role)).toBeChecked();
  });

  it("provides options to select for 'father'.", () => {
    const missingParams = {father: ["Arden", "Lex", "Claude"]};
    render(<table><tbody><OptionSelect {...{missingParams}} /></tbody></table>);
    const role = "combobox";
    expect(screen.getByRole(role)).toHaveValue("Arden");
    //expect(0).toBe(1);
  });

  it("provides options to select for 'lyn_mode'.", () => {
    const missingParams = {lyn_mode: [true, false]};
    render(<table><tbody><OptionSelect {...{missingParams}} /></tbody></table>);
    const role = "checkbox";
    // expect(screen.getByRole(role)).toHaveValue("Arden");
    expect(screen.getByRole(role)).toBeChecked();
    //expect(0).toBe(1);
  });

  it("provides options to select for 'route'.", () => {
    const missingParams = {route: ["A", "B"]};
    render(<form><table><tbody><OptionSelect {...{missingParams}} /></tbody></table></form>);
    const role = "form";
    expect(screen.getByRole(role)).toHaveFormValues(["A", "B"]);
    //expect(0).toBe(1);
  });

  it("provides options to select for 'number_of_declines'.", () => {
    const missingParams = {number_of_declines: [1, 3]};
    render(<table><tbody><OptionSelect {...{missingParams}} /></tbody></table>);
    const role = "combobox";
    expect(screen.getByRole(role)).toHaveDisplayValue("8,000 G");
    //expect(0).toBe(1);
  });

});

describe("ProfileHead", () => {

  it("displays the portrait-image and children provided.", () => {
    const figureTitle = "Portrait";
    const imgSrc = "";
    render(<div><ProfileHead {...{figureTitle, imgSrc}}><iframe src="" className="ProfileHead-child"></iframe></ProfileHead></div>);
    expect(screen.getByRole("heading")).toHaveTextContent("Portrait");
    // expect(0).toBe(1);
  });

});

describe("ProfileLevelAndClass", () => {

  it("displays the level and class of the unit.", () => {
    const unitClass = "Unit Class";
    const level = [0, 1];
    render(<table><tbody><ProfileLevelAndClass {...{unitClass, level}} /></tbody></table>);
    const columnHeaders = screen.getAllByRole("columnheader");
    expect(columnHeaders[0]).toHaveTextContent("Class");
    expect(columnHeaders[1]).toHaveTextContent("Lv");
    expect(columnHeaders[2]).toBeUndefined();
    const cells = screen.getAllByRole("cell");
    expect(cells[0]).toHaveTextContent("Unit Class");
    expect(cells[1]).toHaveTextContent("0 / 1");
    //expect(0).toBe(1);
  });

});
