import type { Route } from "./+types/home";

import axios from 'axios';
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
      <tbody>
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
      </tbody>
    </table>
  );
}

export function meta({}: Route.MetaArgs) {
  return [
    { title: "Aenir: A Fire Emblem stat calculator" },
    { name: "description", content: "Calculate Fire Emblem stats here!" },
  ];
}

export function getFireEmblemGames() {
  return [
    {
      no: 4,
      title: "Genealogy of the Holy War",
      name: "genealogy-of-the-holy-war",
    },
    {
      no: 5,
      title: "Thracia 776",
      name: "thracia-776",
    },
    {
      no: 6,
      title: "Sword of Seals",
      name: "binding-blade",
    },
    {
      no: 7,
      title: "Blazing Sword",
      name: "blazing-sword",
    },
    {
      no: 8,
      title: "The Sacred Stones",
      name: "the-sacred-stones",
    },
    {
      no: 9,
      title: "Path of Radiance",
      name: "path-of-radiance",
    },
  ];
};

export function findFireEmblemGame({params}) {
  const fireEmblemGames = getFireEmblemGames();
  const game = fireEmblemGames.find(gameObj => `fe${gameObj.no}`=== params.game);
  return game;
}

export function getUnitList({gameNo}) {
  const unitListByGame = {
    4: [
      'Sigurd',
      'Noish',
      'Alec',
      'Arden',
      'Cuan',
      'Ethlin',
      'Fin',
      'Lex',
      'Azel',
      'Midayle',
      'Adean',
      'Dew',
      'Ira',
      'Diadora',
      'Jamka',
      'Holyn',
      'Lachesis',
      'Levin',
      'Sylvia',
      'Fury',
      'Beowolf',
      'Briggid',
      'Claude',
      'Tiltyu',
      'Mana',
      'Radney',
      'Roddlevan',
      'Oifey',
      'Tristan',
      'Dimna',
      'Yuria',
      'Femina',
      'Amid',
      'Johan',
      'Johalva',
      'Shanan',
      'Daisy',
      'Janne',
      'Aless',
      'Laylea',
      'Linda',
      'Asaello',
      'Hawk',
      'Hannibal',
      'Sharlow',
      'Celice',
      'Leaf',
      'Altenna',
      'Rana',
      'Lakche',
      'Skasaher',
      'Delmud',
      'Lester',
      'Fee',
      'Arthur',
      'Patty',
      'Nanna',
      'Leen',
      'Tinny',
      'Faval',
      'Sety',
      'Corpul',
    ],
    5: [
      'Leaf',
      'Fin',
      'Evayle',
      'Halvan',
      'Othin',
      'Dagda',
      'Tania',
      'Marty',
      'Ronan',
      'Rifis',
      'Safy',
      'Brighton',
      'Machua',
      'Lara',
      'Felgus',
      'Karin',
      'Dalsin',
      'Asvel',
      'Nanna',
      'Hicks',
      'Shiva',
      'Carrion',
      'Selphina',
      'Kein',
      'Alva',
      'Robert',
      'Fred',
      'Olwen',
      'Mareeta',
      'Salem',
      'Pahn',
      'Tina',
      'Trewd',
      'Glade',
      'Dean',
      'Eda',
      'Homeros',
      'Linoan',
      'Ralph',
      'Eyrios',
      'Sleuf',
      'Sara',
      'Miranda',
      'Shanam',
      'Misha',
      'Xavier',
      'Amalda',
      'Conomore',
      'Delmud',
      'Cyas',
      'Sety',
      'Galzus',
    ],
    6: [
      'Roy',
      'Marcus',
      'Allen',
      'Lance',
      'Wolt',
      'Bors',
      'Merlinus',
      'Ellen',
      'Dieck',
      'Wade',
      'Lott',
      'Thany',
      'Chad',
      'Lugh',
      'Clarine',
      'Rutger',
      'Saul',
      'Dorothy',
      'Sue',
      'Zealot',
      'Treck',
      'Noah',
      'Astohl',
      'Lilina',
      'Wendy',
      'Barth',
      'Oujay',
      'Fir',
      'Shin',
      'Gonzales',
      'Geese',
      'Klein',
      'Tate',
      'Lalum',
      'Echidna',
      'Elphin',
      'Bartre',
      'Ray',
      'Cath',
      'Miredy',
      'Percival',
      'Cecilia',
      'Sofiya',
      'Igrene',
      'Garret',
      'Fa',
      'Hugh',
      'Zeis',
      'Douglas',
      'Niime',
      'Dayan',
      'Juno',
      'Yodel',
      'Karel',
    ],
    7: [
      'Lyn',
      'Sain',
      'Kent',
      'Florina',
      'Wil',
      'Dorcas',
      'Serra',
      'Erk',
      'Rath',
      'Matthew',
      'Nils',
      'Lucius',
      'Wallace',
      'Eliwood',
      'Lowen',
      'Marcus',
      'Rebecca',
      'Bartre',
      'Hector',
      'Oswin',
      'Guy',
      'Merlinus',
      'Priscilla',
      'Raven',
      'Canas',
      'Dart',
      'Fiora',
      'Legault',
      'Ninian',
      'Isadora',
      'Heath',
      'Hawkeye',
      'Geitz',
      'Farina',
      'Pent',
      'Louise',
      'Karel',
      'Harken',
      'Nino',
      'Jaffar',
      'Vaida',
      'Karla',
      'Renault',
      'Athos',
    ],
    8: [
      'Eirika',
      'Seth',
      'Franz',
      'Gilliam',
      'Vanessa',
      'Moulder',
      'Ross',
      'Garcia',
      'Neimi',
      'Colm',
      'Artur',
      'Lute',
      'Natasha',
      'Joshua',
      'Ephraim',
      'Forde',
      'Kyle',
      'Orson',
      'Tana',
      'Amelia',
      'Innes',
      'Gerik',
      'Tethys',
      'Marisa',
      "L'Arachel",
      'Dozla',
      'Saleh',
      'Ewan',
      'Cormag',
      'Rennac',
      'Duessel',
      'Knoll',
      'Myrrh',
      'Syrene',
      'Caellach',
      'Riev',
      'Ismaire',
      'Selena',
      'Glen',
      'Hayden',
      'Valter',
      'Fado',
      'Lyon',
    ],
    9: [
      'Ike',
      'Titania',
      'Oscar',
      'Boyd',
      'Rhys',
      'Shinon',
      'Gatrie',
      'Soren',
      'Mia',
      'Ilyana',
      'Marcia',
      'Mist',
      'Rolf',
      'Lethe',
      'Mordecai',
      'Volke',
      'Kieran',
      'Brom',
      'Nephenee',
      'Zihark',
      'Jill',
      'Sothe',
      'Astrid',
      'Makalov',
      'Stefan',
      'Muarim',
      'Tormod',
      'Devdan',
      'Tanith',
      'Reyson',
      'Janaff',
      'Ulki',
      'Calill',
      'Tauroneo',
      'Ranulf',
      'Haar',
      'Lucia',
      'Bastian',
      'Geoffrey',
      'Largo',
      'Elincia',
      'Ena',
      'Nasir',
      'Tibarn',
      'Naesala',
      'Giffca',
    ],
  };
  return unitListByGame[gameNo];
}

export function unitListLoader( {game} ) {
  const gameNo = game.no;
  return getUnitList({gameNo});
}

export async function unitStatsLoader( {initParams} ) {
  const sourceUrl = "http://127.0.0.1:8000/dracogate/api/initialization_view/";
  // containers for output
  let metaStats = {
    currentCls: null,
    currentLv: null,
  };
  let currentStats = null;
  let missingParams = null;
  console.log("About to send POST request to URL.");
  await axios
    .post(sourceUrl,
      {data: initParams},
    )
    .then(res => {
      const data = res.data;
      const [success, clsLv, value] = data;
      console.log("Data has been fetched.");
      if (success) {
        currentStats = value;
        [metaStats.currentCls, metaStats.currentLv] = clsLv
        console.log("Unit has been found. Level: " + metaStats.currentLv);
      } else {
        missingParams = value;
        console.log("Failure. missingParams: " + missingParams);
      };
    })
    .catch(err => console.log(err));
  console.log("Checking if missingParams need to be populated.");
  if (missingParams !== null) {
    console.log("missingParams not null: " + missingParams);
    const [field, choices] = missingParams;
    const defaultVal = choices[0];
    initParams[field] = defaultVal;
    await axios
      .post(sourceUrl,
        {data: initParams},
      )
      .then(res => {
        const data = res.data;
        const [_, clsLv, value] = data;
        [metaStats.currentCls, metaStats.currentLv] = clsLv;
        currentStats = value;
      })
      .catch(err => console.log(err));
  };
  console.log("End of unitStatsLoader");
  return [metaStats, currentStats, missingParams];
};

export async function newUnitSaver( {initParams, showError} ) {
  const sourceUrl = "http://127.0.0.1:8000/dracogate/api/initialization_view/";
  alert("About to send PUT request to URL.");
  await axios
    .put(sourceUrl,
      {data: initParams},
    )
    .then(res => {
        return alert("PUT request successful");
      })
    .catch(err => console.log(err));
  return null;
};
