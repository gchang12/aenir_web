import {
  GAMES,
  MORPH_METHOD_NAMES,
} from "./constants";
import {
  getStatList,
  listMorphMethods,
  simulateMorphMethod,
  executeMorphMethod,
} from "./functions";
import {
  useState,
  useCallback,
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
          <option key={choice} name="chapter" id={choice} value={choice} defaultChecked={defaultValue === choice}>
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
  const fillValue = "-";
  return (
    <table className="StatsTable">
      <tbody>
      {statList.map(stat => {
        return (
          <tr key={stat}>
            <th>{stat}</th>
            <td>{fillValue}</td>
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
  const fillValue = "-";
  return (
    <table className="ClassLevelInfo">
      <tbody>
        <tr>
          <th>Class</th>
          <td>{fillValue}</td>
        </tr>
        <tr>
          <th>Level</th>
          <td>{fillValue}</td>
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

export function UnitHub({gameId, unitName, morph, onFormChange, formRef, children}) {
  return (
    <>
    <ProfileIcon {...{gameId, unitName}}>
    {unitName}
    </ProfileIcon>
    {morph == null ? <BlankClassLevelInfo /> : <ClassLevelInfo {...{morph}} />}
    <Form onChange={onFormChange} ref={formRef} className="ConfirmationMenu" method="post">
      {children}
    </Form>
    {/* */}
    {morph == null ? <BlankStatsTable {...{gameId}} /> : <CurrentStatsTable {...{stats: morph.stats}} />}
    </>
  );
};

export function MorphMethodSelect({gameId, onMethodSelect, currentMethod}) {
  const morphMethods = listMorphMethods(gameId);
  return (
    <div className="SelectMorphMethod">
      <label htmlFor="morphMethod">Action</label>
      <select required name="morphMethod" id="morphMethod" onChange={onMethodSelect} defaultValue={currentMethod}>
        <option name="morphMethod" value=""></option>
        {morphMethods.map(method => {
          const displayName = MORPH_METHOD_NAMES[method];
          return (
            <option name="morphMethod" key={method} value={method}>
              {displayName}
            </option>
          );
        })
        }
      </select>
    </div>
  );
};

function LevelUpMenu({paramBounds, morph}) {
  const errorMsg = morph.level[0] >= paramBounds[1] ?  `Cannot level-up past LV${paramBounds[1]}.` : null;
  return (
    <div className="LevelUpMenu">
      <label htmlFor="level_up">Levels</label>
      <input id="level_up" disabled={paramBounds[0] == null} type="number" name="num_levels" min="1" placeholder={paramBounds[0] == null ? undefined : 0} max={paramBounds == null ? undefined : paramBounds[1] - paramBounds[0] + 1} step="1" />
      {errorMsg == null || (
        <p>{errorMsg}</p>
      )}
    </div>
  );
}

function PromoteMenu({paramBounds, morph}) {
  // upon change, show error message
  const [errorMsg, setErrorMsg] = useState("");
  const checkForErrors = useCallback((e) => {
    console.log(e.currentTarget);
    const promoCls = e.currentTarget.value;
    const minPromoLv = paramBounds.find(paramBoundEntry => paramBoundEntry[1] === promoCls)[0];
    if (morph.level.at(0) < minPromoLv) {
      setErrorMsg(`Must be at least Lv. ${minPromoLv} to promtoe.`);
    };
  }, [paramBounds]);
  return (
    <div className="PromoteMenu">
      <label htmlFor="promote">Promote</label>
      <select id="promote" name="promote">
      {paramBounds.map(([_, promoCls]) => {
        return (
          <option key={promoCls} value={promoCls}>
          {promoCls}
          </option>
        );
      })
      }
      </select>
      {errorMsg === "" || <p>{errorMsg}</p>}
    </div>
  );
}

function UseStatBoosterMenu() {
  return (
    <h1>
    Promote
    </h1>
  );
}
function SetBandsMenu() {
  return (
    <h1>
    Equip Bands
    </h1>
  );
}
function SetScrollsMenu() {
  return (
    <h1>
    Equip Scrolls
    </h1>
  );
}
function UseAfasDropsMenu() {
  return (
    <h1>
    Use Afas's Drops
    </h1>
  );
}
function UseMetissTomeMenu() {
  return (
    <h1>
    Use Metis's Tome
    </h1>
  );
}

export function MorphMethodMenu({methodName, paramBounds, morph}) {
  switch (methodName) {
    case "level_up":
      return <LevelUpMenu {...{paramBounds, morph}} />
    case "promote":
      return <PromoteMenu {...{paramBounds, morph}} />
    case "use_stat_booster":
      return <UseStatBoosterMenu {...{paramBounds, morph}} />
    case "set_scrolls":
      return <SetScrollsMenu {...{paramBounds, morph}} />
    case "use_afas_drops":
      return <UseAfasDropsMenu {...{paramBounds, morph}} />
    case "use_metiss_tome":
      return <UseMetissTomeMenu {...{paramBounds, morph}} />
    case "set_bands":
      return <SetBandsMenu {...{paramBounds, morph}} />
    default:
      throw new Error(`Unrecgonized method: '${methodName}'`);
  };
}

