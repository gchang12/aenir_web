function SelectWidget({choices, field, title, onClick}) {
  return (
    <>
      <label htmlFor={field}>{title}</label>
      <select id={field}>
        {choices.map(choice => {
          return (
            <option key={choice} data-fieldname={field} value={choice} onClick={onClick}>{choice}</option>
          );}
        )
        }
      </select>
    </>
  );
}

function RadioWidget({choices, field, onClick}) {
  return (
    <fieldset>
      <legend>Route</legend>
      {choices.map(choice => {
        return (
          <>
            <label htmlFor={field}>{choice}</label>
            <input type="radio" id={choice} value={choice} name={field} data-fieldname={field} onClick={onClick} />
          </>
        );
      })}
    </fieldset>
  );
};

function NumberWidget({choices, field, title, onClick}) {
  return (
    <>
      <label htmlFor={field}>{title}</label>
      <input type={inputType} id={field} name={field} min="0" max={choices.length - 1} data-fieldname={field} onClick={onClick} />
    </>
  );
}

function CheckboxWidget({field, title, onClick}) {
  return (
    <>
      <label htmlFor={field}>{title}</label>
      <input type={inputType} id={field} name={field} data-fieldname={field} onClick={onClick} />
    </>
  );
}

export function getOptionList({paramList, onClick}) {
  const possibleOptions = {
    father: ["Father", "select"],
    hard_mode: ["Hard Mode", "checkbox"],
    lyn_mode: ["Lyn Mode", "checkbox"],
    route: ["Route", "radio"],
    number_of_declines: ["Number of Declines", "number"],
  };
  const compiledOptions = [];
  let key = 0;
  Object.entries(paramList).forEach(params => {
    const [field, choices] = params;
    const [title, inputType] = possibleOptions[field];
    const inputWidget = {
      "select": (
        <SelectWidget choices={choices} field={field} title={title} onClick={onClick} />
      ),
      "radio": (
        <RadioWidget choices={choices} field={field} onClick={onClick} />
      ),
      "number": (
        <NumberWidget choices={choices} field={field} onClick={onClick} />
      ),
      "checkbox": (
        <CheckboxWidget field={field} title={title} onClick={onClick} />
      ),
    }[inputType]
    optionsToBeShown.push(
      <Fragment key={key}>
        {inputWidget}
      </Fragment>
    );
    key += 1;
  });
  return optionsToBeShown;
};

export function GameProfile({game}) {
  return (
    <figure>
      <img src={`/static/${game.name}/cover-art.png`} alt={`Cover art of FE${game.no}: ${game.title}`} />
      <figcaption>
        {game.title}
      </figcaption>
    </figure>
  );
}

function GameUrl({feGame}) {
  return (
    <a href={`/morphs/new-morph/fe${feGame.no}/`}>
      {feGame.title}
    {/* <GameProfile game={feGame} /> */}
    </a>
  );
}

export function UnitProfile({game, unit}) {
  const imgSuffix = game.no === 8 ? "gif" : "png";
  const imgFile = `${unit}.${imgSuffix}`;
  return (
    <figure>
      <img src={`/static/${game.name}/characters/${imgFile}`} alt={`Portrait of ${unit}, ${imgFile}`} />
      <figcaption>
        {unit}
      </figcaption>
    </figure>
  );
}

export function GameUrlList({gameList}) {
  return (
    <>
      {gameList.map(feGame => {
        return (
          <li key={feGame.no}>
            <GameUrl feGame={feGame} />
          </li>
        ); 
        })
      }
    </>
  );
}

function UnitUrl({game, unit}) {
  const gameRank = `fe${game.no}`;
  return (
    <a href={`/morphs/new-morph/${gameRank}/${unit}`}>
      <UnitProfile game={game} unit={unit} />
    </a>
  );
};

export function UnitUrlList({game, unitList}) {
  return (
    <>
      {unitList.map(unit => {
        return (
          <li key={unit}>
            <UnitUrl game={game} unit={unit} />
          </li>
        );
      })
      }
    </>
  );
}

export function StatTable({stats}) {
  return (
    <table>
      {stats.map(labelValue => {
          const [field, value] = labelValue;
          return (
            <tr>
              <th>{field}</th>
              <td>{value}</td>
            </tr>
          )
      })
      }
    </table>
  );
}
