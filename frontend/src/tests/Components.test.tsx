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
  render,
} from "vitest-browser-react";

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

describe("StatTable", () => {

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
    expect(screen.getByRole(role)).toBeChecked();
  });

  it("provides options to select for 'father'.", () => {
    const missingParams = {father: ["Arden", "Lex", "Claude"]};
    render(<table><tbody><OptionSelect {...{missingParams}} /></tbody></table>);
    const role = "combobox";
    expect(screen.getByRole(role)).toHaveValue("Arden");
  });

  it("provides options to select for 'lyn_mode'.", () => {
    const missingParams = {lyn_mode: [true, false]};
    render(<table><tbody><OptionSelect {...{missingParams}} /></tbody></table>);
    const role = "checkbox";
    // expect(screen.getByRole(role)).toHaveValue("Arden");
    expect(screen.getByRole(role)).toBeChecked();
  });

  it("provides options to select for 'route'.", () => {
    const missingParams = {route: ["A", "B"]};
    render(<table><tbody><OptionSelect {...{missingParams}} /></tbody></table>);
    const labelText = "A";
    expect(screen.getByLabelText(labelText)).toBeChecked();
  });

  it("provides options to select for 'number_of_declines'.", () => {
    const missingParams = {number_of_declines: [1, 3]};
    render(<table><tbody><OptionSelect {...{missingParams}} /></tbody></table>);
    const role = "combobox";
    expect(screen.getByRole(role)).toHaveDisplayValue("8,000 G");
  });

});

describe("ProfileHead", () => {

  it("displays the portrait-image and children provided.", () => {
    const figureTitle = "Portrait";
    const imgSrc = "";
    render(<div><ProfileHead {...{figureTitle, imgSrc}}><iframe src="" className="ProfileHead-child"></iframe></ProfileHead></div>);
    expect(screen.getByRole("heading")).toHaveTextContent("Portrait");
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
  });

});
