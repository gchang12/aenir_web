import {
  GAMES,
} from "../constants";

function FatherSelect({choices}) {
  // choices: ['Arden', 'Azel', 'Alec', 'Claude', 'Jamka', 'Dew', 'Noish', 'Fin', 'Beowolf', 'Holyn', 'Midayle', 'Levin', 'Lex']
  return (
    <div className="FatherSelect">
      <label htmlFor="father">Father</label>
      <select id="father" required name="father">
      {choices.map(choice => {
        return (
          <option key={choice} defaultValue={choice}>{choice}</option>
        );
      })
      }
      </select>
    </div>
  );
};

function HardModeToggle({choices}) {
  // choices: [false, true]
  const [defaultChecked] = choices;
  // const [checked, setChecked] = React.useState(defaultChecked);
  return (
    <div className="HardModeToggle">
      <label htmlFor="hard_mode">Hard Mode</label>
      <input id="hard_mode" name="hard_mode" {...{defaultChecked}} type="checkbox" />
    </div>
  );
};

function LynModeToggle({choices}) {
  // choices: [false, true]
  const [defaultChecked] = choices;
  // const [checked, setChecked] = React.useState(defaultChecked);
  return (
    <div className="LynModeToggle">
      <label htmlFor="lyn_mode">Lyn Mode</label>
      <input id="lyn_mode" required name="lyn_mode" {...{defaultChecked}} type="checkbox" />
    </div>
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
    <div className="MageDecliner">
      <label htmlFor="number_of_declines">Gold Tendered</label>
      <select id="number_of_declines" required name="number_of_declines">
      {choices.map(choice => {
        const price = priceByDeclineCount[choice];
        return (
          <option key={choice} defaultValue={choice}>{price.toLocaleString() + " G"}</option>
        );
      })
      }
      </select>
    </div>
  );
};

function ChapterSelect({choices}) {
  // choices: ['Lalum', 'Elphin']
  const [defaultValue] = choices;
  return (
    <div className="ChapterSelect">
      <fieldset>
      <legend>Chapter</legend>
      {choices.map(choice => {
        return (
          <div className="chapter-choice" key={choice}>
            <label htmlFor={choice} required>{choice}</label>
            <input name="chapter" id={choice} type="radio" value={choice} defaultChecked={defaultValue === choice} />
          </div>
        );
      })
      }
      </fieldset>
    </div>
  );
};

export function OptionSelect({missingParams}) {
  return (
    <>
    {Object.entries(missingParams ?? {}).map(missingParamSet => {
      const [key, choices] = missingParamSet;
      switch(key) {
        case "father":
          return <FatherSelect key={key} {...{choices}} />;
        case "chapter":
          return <ChapterSelect key={key} {...{choices}} />;
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

export function CurrentStatsTable({morph}) {
  return (
    <table className="CurrentStatsTable">
      <tbody>
      {morph == null || morph.stats.map(([stat, currentValue, localMax, absMax]) => {
        return (
          <tr key={stat} className={currentValue === localMax ? "maxed-stat" : undefined}>
            <th>{stat}</th>
            <td>{currentValue}</td>
            <td>
              <meter min="0" value={currentValue} max={absMax} optimum={localMax}></meter>
            </td>
          </tr>
        );
      })
      }
      </tbody>
    </table>
  );
};

export function ProfileIcon({gameId, unitName}) {
  const gameName = GAMES.find(game => "fe" + game.no === gameId).name;
  const imgSuffix = gameId === "fe8" ? ".gif" :".png";
  return (
    <figure className={["ProfileIcon", gameId.toUpperCase()].join(" ")}>
      <img src={["", "images", gameName, "characters", unitName + imgSuffix].join("/")} />
      <figcaption>{unitName}</figcaption>
    </figure>
  );
};

export function ClassLevelInfo({morph}) {
  return (
    <table className="ClassLevelInfo">
      <tbody>
        <tr>
          <th>Class</th>
          <td>{morph == null ? "???" : morph.unitClass}</td>
        </tr>
        <tr>
          <th>Level</th>
          <td>{morph == null ? "???" : morph.level[0]}</td>
        </tr>
      </tbody>
    </table>
  );
};

export function OptionsMenu({disabled, onClick, children}) {
  return (
    <div className="OptionsMenu">
      {children}
      <button disabled={disabled} onClick={onClick} type="button">Preview</button>
    </div>
  );
};

export function ConfirmationMenu({message, disabled}) {
  return (
    <div className="ConfirmationMenu">
      <p>{message}</p>
      <button type="submit" disabled={disabled}>Create</button>
    </div>
  );
};
