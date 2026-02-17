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

/* TODO
OptionSelect: Provides options to select.
ProfileHead: Displays portrait and other info.
ProfileLevelAndClass: Displays level and class
StatTable: Displays stats in a table.
NOTE: Aren't these all liable to change?

Confirm:
- images are showing up
- links lead to expected destinations
- destinations contain expected content
- stats are present
- Gonzales-toggling works

Test:
- routes.
*/
