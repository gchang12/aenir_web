
function FatherSelect({choices}) {
  // choices: ['Arden', 'Azel', 'Alec', 'Claude', 'Jamka', 'Dew', 'Noish', 'Fin', 'Beowolf', 'Holyn', 'Midayle', 'Levin', 'Lex']
  return (
    <>
    <tr>
      <th><label htmlFor="father">Father Select</label></th>
      <td>
        <select required name="father">
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

function HardModeToggle({choices}) {
  // choices: [false, true]
  const [defaultChecked] = choices;
  // const [checked, setChecked] = React.useState(defaultChecked);
  return (
    <>
    <tr>
      <th><label htmlFor="hard_mode">Hard Mode</label></th>
      <td><input required name="hard_mode" {...{defaultChecked}} type="checkbox" />
      {/* <input name="hard_mode" value={!checked} type="hidden" /> */}
      </td>
    </tr>
    </>
  );
};

function LynModeToggle({choices}) {
  // choices: [false, true]
  const [defaultChecked] = choices;
  // const [checked, setChecked] = React.useState(defaultChecked);
  return (
    <>
    <tr>
      <th><label htmlFor="lyn_mode">Lyn Mode</label></th>
      <td><input required name="lyn_mode" {...{defaultChecked}} type="checkbox" />
      {/* <input name="lyn_mode" value={!checked} type="hidden" /> */}
      </td>
    </tr>
    </>
  );
};

function MageDecliner({choices}) {
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
        <select required name="number_of_declines">
        {choices.map(choice => {
          const price = priceByDeclineCount[choice];
          return (
            <option key={choice} value={choice}>{price.toLocaleString() + " G"}</option>
          );
        })
        }
        </select>
      </td>
    </tr>
    </>
  );
};

function RouteSelect({choices}) {
  // choices: ['Lalum', 'Elphin']
  const [defaultValue] = choices;
  return (
    <tr>
      <th>Route</th>
      <td>
      {choices.map(choice => {
        return (
          <div className="route-choice" key={choice}>
            <label htmlFor={choice} required>{choice}</label>
            <input required name="route" id={choice} value={choice} type="radio" defaultChecked={choice === defaultValue} />
          </div>
        );
      })
      }
      </td>
    </tr>
  );
};

export function OptionSelect({missingParams}) {
  return (
    <>
    {Object.entries(missingParams ?? {}).map(missingParamSet => {
      // console.log(missingParamSet);
      const [key, choices] = missingParamSet;
      // console.log(key, choices);
      switch(key) {
        case "father":
          return <FatherSelect key={key} {...{choices}} />;
        case "route":
          return <RouteSelect key={key} {...{choices}} />;
        case "number_of_declines":
          return <MageDecliner key={key} {...{choices}} />;
        case "hard_mode":
          return <HardModeToggle key={key} {...{choices}} />;
        case "lyn_mode":
          return <LynModeToggle key={key} {...{choices}} />;
      };
      })
    }
    </>
  );
};

export function ProfileHead({figureTitle, imgSrc, children}) {
  return (
    <>
    <figure>
      <img src={imgSrc} alt={imgSrc} />
      <figcaption>
        <h2>{figureTitle}</h2>
        <div className="ProfileHead-children">{children}</div>
      </figcaption>
    </figure>
    </>
  );
};

export function ProfileLevelAndClass({unitClass, level}) {
  const [currentLv, maxLv] = level;
  return (
    <>
    <tr>
      <th>Class</th>
      <td>{unitClass}</td>
    </tr>
    <tr>
      <th>Lv</th>
      <td>{currentLv} / {maxLv}</td>
    </tr>
    </>
  );
};

// TODO: Modify highlight-option
export function StatTable({stats, highlight}) {
  const className = highlight === true ? "maxed-stat" : undefined;
  return (
    <>
    {stats.map(([stat, currentValue, localMax, absMax]) => {
      return (
        <tr key={stat} className={currentValue === localMax ? className : undefined}>
          <th>{stat}</th>
          <td>{currentValue}</td>
          <td>
            <meter min="0" value={currentValue} max={absMax} high={localMax}></meter>
          </td>
        </tr>
      );
    })
    }
    </>
  );
};

