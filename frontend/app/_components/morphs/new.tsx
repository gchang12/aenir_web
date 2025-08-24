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
      <figure>
        <img id="father-preview" src="/static/genealogy-of-the-holy-war/characters/Arden.png" alt="/static/genealogy-of-the-holy-war/characters/Arden.png" />
        <figcaption>
          Father
        </figcaption>
      </figure>
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
      <input type="number" id={field} name={field} min="0" max={choices.length - 1} data-fieldname={field} onClick={onClick} />
    </>
  );
}

function CheckboxWidget({field, title, onClick}) {
  return (
    <>
      <label htmlFor={field}>{title}</label>
      <input type="checkbox" id={field} name={field} data-fieldname={field} onClick={onClick} />
    </>
  );
}

export function MorphOption1({params, onClick}) {
  const possibleOptions = {
    father: ["Father", "select"],
    hard_mode: ["Hard Mode", "checkbox"],
    lyn_mode: ["Lyn Mode", "checkbox"],
    number_of_declines: ["Number of Declines", "number"],
  };
  const [field, choices] = params;
  const [title, inputType] = possibleOptions[field];
  return {
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
  }[inputType];
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
    <a href={`/morphs/new/fe${feGame.no}/`}>
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
    <a href={`/morphs/new/${gameRank}/${unit}`}>
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

{/* export function StatTable({stats, maxStats, thClassNames, tdClassNames}) { */}
export function StatTable({stats}) {
  {/* TODO: meter, progress, max-stats, class-names */}
  return (
    <table>
      {stats.map(labelValue => {
          const [field, value] = labelValue;
          return (
            <tr key={field}>
              <th>{field}</th>
              <td>{value}</td>
            </tr>
          )
      })
      }
    </table>
  );
}
