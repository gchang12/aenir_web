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
    render(<div><GameSelect /></div>);
    let linkElement;
    for (let game_no=4; game_no <= 9; game_no++) {
      linkElement = screen.getByText("FE" + game_no);
      expect(linkElement).toBeVisible();
      expect(linkElement).toHaveAttribute("href", "/create-morph/fe" + game_no + "/");
    };
    /* /create-morph/fe{4..9} */
  });

  it("lists game titles.", () => {
    render(<div><GameSelect /></div>);
    let linkElement;
    for (let game_no=4; game_no <= 9; game_no++) {
      linkElement = screen.getByText("FE" + game_no);
      expect(linkElement).toBeVisible();
      expect(linkElement).toHaveAttribute("href", "/create-morph/fe" + game_no + "/");
    };
  });

  it("renders images of each game.", () => {
    render(<div><GameSelect /></div>);
    const linkElements = screen.getAllByRole('image');
    // Check if they're all visible
    linkElements.forEach(linkElement => expect(linkElement).toBeVisible());
    // Check if they've got the right alt-image
    // Check if they've got the right src
    const gameNames = [
      "genealogy-of-the-holy-war",
      "thracia-776",
      "binding-blade",
      "blazing-sword",
      "the-sacred-stones",
      "path-of-radiance",
    ];
    for (const [indexNo, name] in Object.entries(gameNames)) {
      linkElement = linkElements[indexNo];
      expect(linkElement).toHaveAttribute("src", "/images/" + name + "/cover-art.png");
      expect(linkElement).toHaveAttribute("alt", "/images/" + name + "/cover-art.png");
    };
  });

  it("renders links.", () => {
    render(<div><GameSelect /></div>);
    const linkElements = screen.getAllByRole('link');
    let linkElement;
    let href;
    for (let game_no=4; game_no <= 9; game_no++) {
      href = "/create-morph/fe" + game_no + "/";
      linkElement = screen.getByAltText(href);
      expect(linkElement).toHaveTextContent("FE" + game_no);
      expect(linkElement).toBeVisible();
      expect(linkElement).toHaveAttribute("href", href);
    };
  });

});

describe("UnitSelect", () => {

  it("shows the image of a unit.", () => {
    // NOTE: must use useParams hook.
    expect(0).toBe(1);
  });

  it("shows the name of a unit.", () => {
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
