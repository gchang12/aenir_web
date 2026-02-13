import React from "react";

import type {
  MissingParams,
} from "../lib/_types";

function FatherSelect({ choices, onChange } : { choices: Array<string>; onChange: any }) {
  // choices: ['Arden', 'Azel', 'Alec', 'Claude', 'Jamka', 'Dew', 'Noish', 'Fin', 'Beowolf', 'Holyn', 'Midayle', 'Levin', 'Lex']
  return (
    <>
    <tr>
      <th><label htmlFor="father">Father Select</label></th>
      <td>
        <select name="father">
        {choices.map(choice => {
          return (
            <option key={choice} value={choice}>{choice}</option>
          );
        })
        }
        </select>
      </td>
    </tr>
    </>
  );
};

function HardModeToggle({ choices, onChange } : { choices: Array<boolean>; onChange: any }) {
  // choices: [false, true]
  const [defaultChecked] = choices;
  const [checked, setChecked] = React.useState(defaultChecked);
  return (
    <>
    <tr>
      <th><label htmlFor="hard_mode">Hard Mode</label></th>
      <td><input onClick={e => setChecked(e.currentTarget.checked ? true : false)} name="_hard_mode" {...{defaultChecked: checked}} type="checkbox" /><input name="hard_mode" value={defaultChecked} type="hidden" /></td>
    </tr>
    </>
  );
};

function LynModeToggle({ choices, onChange } : { choices: Array<boolean>; onChange: any }) {
  // choices: [false, true]
  const [defaultChecked] = choices;
  const [checked, setChecked] = React.useState(defaultChecked);
  return (
    <>
    <tr>
      <th><label htmlFor="lyn_mode">Hard Mode</label></th>
      <td><input onClick={e => setChecked(e.currentTarget.checked ? true : false)} name="_lyn_mode" {...{defaultChecked: checked}} type="checkbox" /><input name="lyn_mode" value={defaultChecked} type="hidden" /></td>
    </tr>
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
    <tr>
      <th><label htmlFor="number_of_declines">Gold Tendered</label></th>
      <td>
        <select name="number_of_declines">
        {choices.map(choice => {
          const price = priceByDeclineCount[choice];
          return (
            <option key={choice} value={choice}>{price + " G"}</option>
          );
        })
        }
        </select>
      </td>
    </tr>
    </>
  );
};

function RouteSelect({ choices, onChange } : { choices: Array<string>; onChange: any }) {
  // choices: ['Lalum', 'Elphin']
  const [defaultValue] = choices;
  return (
    <tr>
      <th>Route</th>
      <td>
      {choices.map(choice => {
        return (
          <div className="route-choice" key={choice}>
            <label htmlFor={choice}>{choice}</label>
            <input name="route" id={choice} value={choice} type="radio" defaultChecked={choice === defaultValue} />
          </div>
        );
      })
      }
      </td>
    </tr>
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

