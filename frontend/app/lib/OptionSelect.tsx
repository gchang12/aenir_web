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
    <>
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
    </>
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

export function OptionSelect({ missingParams, onChange } : { missingParams: MissingParams; onChange: any }) : React.ReactNode {
  return (
    <>
    {missingParams.map(missingParamSet => {
      console.log(missingParamSet);
      const [key, choices] = missingParamSet;
      console.log(key, choices);
      switch(key) {
        case "father":
          return <FatherSelect key={key} {...{choices, onChange}} />;
        case "route":
          return <RouteSelect key={key} {...{choices, onChange}} />;
        case "number_of_declines":
          return <MageDecliner key={key} {...{choices, onChange}} />;
        case "hard_mode":
          return <HardModeToggle key={key} {...{choices, onChange}} />;
        case "lyn_mode":
          return <LynModeToggle key={key} {...{choices, onChange}} />;
      };
      })
    }
    </>
  );
};

