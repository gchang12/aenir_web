import {
  GAMES,
} from "../constants";
import {
  getStatList,
} from "./functions";
import {
  useState,
} from "react";
import {
  Form,
} from "react-router";

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
  const [value, setValue] = useState(defaultChecked);
  return (
    <div className="HardModeToggle">
      <label htmlFor="_hard_mode">Hard Mode</label>
      <input id="_hard_mode" name="_hard_mode" {...{defaultChecked}} type="checkbox" onChange={() => setValue(!value)} />
      <input id="hard_mode" name="hard_mode" value={value} type="hidden" />
    </div>
  );
};

function LynModeToggle({choices}) {
  // choices: [false, true]
  const [defaultChecked] = choices;
  // const [checked, setChecked] = React.useState(defaultChecked);
  const [value, setValue] = useState(defaultChecked);
  return (
    <div className="LynModeToggle">
      <label htmlFor="_lyn_mode">Lyn Mode</label>
      <input id="_lyn_mode" name="_lyn_mode" {...{defaultChecked}} type="checkbox" onChange={() => setValue(!value)} />
      <input id="lyn_mode" name="lyn_mode" value={value} type="hidden" />
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
      <label htmlFor="chapter">Chapter</label>
      <select required name="chapter" id="chapter">
      {choices.map(choice => {
        return (
          <option key={choice} name="chapter" id={choice} type="radio" value={choice} defaultChecked={defaultValue === choice}>
            {choice}
          </option>
        );
      })
      }
      </select>
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

export function BlankStatsTable({gameId}) {
  const statList = getStatList(gameId);
  return (
    <table className="StatsTable">
      <tbody>
      {statList.map(stat => {
        return (
          <tr key={stat}>
            <th>{stat}</th>
            <td>???</td>
            <td>
              <meter min="0" value="0"></meter>
            </td>
          </tr>
        );
      })
      }
      </tbody>
    </table>
  );
};

export function CurrentStatsTable({stats}) {
  return (
    <table className="StatsTable">
      <tbody>
      {stats.map(([stat, currentValue, localMax, absMax]) => {
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

export function GrowthsStatsTable({stats, showNew}) {
  return (
    <table className="StatsTable">
      <tbody>
      {stats.map(stat => {
        const [statName, oldGrowth, newGrowth] = stat;
        const statValue = showNew ? newGrowth : oldGrowth;
        return (
          <tr key={statName}>
            <th>{statName}</th>
            <td>{statValue}</td>
            <td>
              <meter min="0" value="100"></meter>
            </td>
          </tr>
        );
      })
      }
      </tbody>
    </table>
  );
};

export function ProfileIcon({gameId, unitName, children}) {
  const gameName = GAMES.find(game => "fe" + game.no === gameId).name;
  const imgSuffix = gameId === "fe8" ? ".gif" :".png";
  return (
    <figure className={["ProfileIcon", gameId.toUpperCase()].join(" ")}>
      <img src={["", "images", gameName, "characters", unitName + imgSuffix].join("/")} />
      <figcaption>{children}</figcaption>
    </figure>
  );
};

export function ClassLevelInfo({morph}) {
  return (
    <table className="ClassLevelInfo">
      <tbody>
        <tr>
          <th>Class</th>
          <td>{morph.unitClass}</td>
        </tr>
        <tr>
          <th>Level</th>
          <td>{morph.level[0]}</td>
        </tr>
      </tbody>
    </table>
  );
};

export function BlankClassLevelInfo() {
  return (
    <table className="ClassLevelInfo">
      <tbody>
        <tr>
          <th>Class</th>
          <td>???</td>
        </tr>
        <tr>
          <th>Level</th>
          <td>???</td>
        </tr>
      </tbody>
    </table>
  );
};

export function ConfirmationMenu({previewMode, refetchMorph, message, children}) {
  return (
    <div className="ConfirmationMenu">
      <p>{message}</p>
      {children}
      <div className="buttons">
        <button disabled={!previewMode} onClick={refetchMorph} type="button">Update</button>
        <button type="submit" disabled={previewMode}>Create</button>
      </div>
    </div>
  );
};

export function UnitHub({gameId, unitName, morph, onChange, formRef, children}) {
  return (
    <>
    <ProfileIcon {...{gameId, unitName}}>
    {unitName}
    </ProfileIcon>
    {morph == null ? <BlankClassLevelInfo {...{gameId}} /> : <ClassLevelInfo {...{morph}} />}
    <Form onChange={onChange} ref={formRef} className="ConfirmationMenu" method="post">
      {children}
    </Form>
    {/* */}
    {morph == null ? <BlankStatsTable {...{gameId}} /> : <CurrentStatsTable {...{stats: morph.stats}} />}
    </>
  );
};

export function OperationMenu({gameNo}) {
  return (
    <>
    </>
  );
}
function LevelUpMenu() {
}
function PromotionMenu() {
}
function UseStatBoosterMenu() {
}
function SetBandsMenu() {
}
function SetScrollsMenu() {
}
function UseAfasDropsMenu() {
}
function UseMetissTomeMenu() {
}
function KnightWardMenu() {
}
export function MorphEvolutionMenu() {
}

