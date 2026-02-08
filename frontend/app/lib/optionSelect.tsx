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
        <option value={choice}>
        {choice}
        </option>
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
    <fieldset>
      <legend>Hard Mode</legend>
      {/* <label> </label> */}
      <input name="hard_mode" {...{defaultChecked}} type="checkbox" />
    </fieldset>
  );
};

function MageDecliner({ choices, onChange } : { choices: Array<number>; onChange: any }) {
  // choices: [0, 1, 2, 3]
  const min: number = choices.at(0);
  const max: number = choices.at(-1);
  const [defaultValue] = choices;
  return (
    <fieldset>
      <legend>Number of Declines</legend>
      <input name="number_of_declines" type="number" {...{min, max, defaultValue}} />
        {/* <label> </label> */}
    </fieldset>
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
          <div className="route-select">
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
    <fieldset>
      <legend>Lyn Mode</legend>
      {/* <label> </label> */}
      <input name="lyn_mode" {...{defaultChecked}} type="checkbox" />
    </fieldset>
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

