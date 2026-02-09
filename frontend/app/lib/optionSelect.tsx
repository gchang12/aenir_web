import React from "react";

import type {
  MissingParams,
} from "../lib/_types";

function FatherSelect({ choices, onChange } : { choices: Array<string>; onChange: any }) {
  // choices: ['Arden', 'Azel', 'Alec', 'Claude', 'Jamka', 'Dew', 'Noish', 'Fin', 'Beowolf', 'Holyn', 'Midayle', 'Levin', 'Lex']
  return (
    <>
    <label htmlFor="father">Father Select</label>
    <select name="father">
    {choices.map(choice => {
      return (
        <option key={choice} value={choice}>{choice}</option>
      );
    })
    }
    </select>
    </>
  );
};

function HardModeToggle({ choices, onChange } : { choices: Array<boolean>; onChange: any }) {
  // choices: [false, true]
  const [defaultChecked] = choices;
  return (
    <>
    <label htmlFor="hard_mode">Hard Mode</label>
    <input name="hard_mode" {...{defaultChecked}} type="checkbox" />
    </>
  );
};

function MageDecliner({ choices, onChange } : { choices: Array<number>; onChange: any }) {
  // choices: [0, 1, 2, 3]
  const [defaultValue]: [number] = choices;
  const priceByDeclineCount = {
    0: 10_000,
    1: 8_000,
    2: 6_000,
    3: 5_000,
  };
  return (
    <label htmlFor="number_of_declines">Gold Tendered</label>
    <select name="number_of_declines">
    {choices.map(choice => {
      const price = priceByDeclineCount[choice];
      return (
        <option key={choice} value={choice}>{price + " G"}</option>
      );
    })
    }
    </select>
  );
};

function RouteSelect({ choices, onChange } : { choices: Array<string>; onChange: any }) {
  // choices: ['Lalum', 'Elphin']
  const [defaultValue] = choices;
  return (
    <fieldset>
      <legend>Route Select</legend>
      {choices.map(choice => {
        return (
          <div className="route-select" key={choice}>
            <label htmlFor={choice}>{choice}</label>
            <input name="route" id={choice} value={choice} type="radio" defaultChecked={choice === defaultValue} />
          </div>
        );
      })
      }
    </fieldset>
  );
};

function LynModeToggle({ choices, onChange } : { choices: Array<boolean>; onChange: any }) {
  // choices: [false, true]
  const [defaultChecked] = choices;
  return (
    <>
    <label htmlFor="lyn_mode">Lyn Mode</label>
    <input name="lyn_mode" {...{defaultChecked}} type="checkbox" />
    </>
  );
};

export function compileOptionSelectControls({ missingParams } : MissingParams) : Array<React.ReactNode> {
  const widgets: Array<React.ReactNode> = [];
  missingParams.forEach(missingParamSet => {
    const [key, choices] = missingParamSet;
    switch(key) {
      case "father":
        widgets.push(<FatherSelect {...{choices, onChange}} />);
        break;
      case "route":
        widgets.push(<RouteSelect {...{choices, onChange}} />);
        break;
      case "number_of_declines":
        widgets.push(<MageDecliner {...{choices, onChange}} />);
        break;
      case "hard_mode":
        widgets.push(<HardModeToggle {...{choices, onChange}} />);
        break;
      case "lyn_mode":
        widgets.push(<LynModeToggle {...{choices, onChange}} />);
        break;
    });
  });
  return widgets;
};

