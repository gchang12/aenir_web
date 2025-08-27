import {
  useState,
} from 'react';
import type {
  Route,
} from "./+types/home";

import axios from 'axios';

{/* META */}

export function meta({}: Route.MetaArgs) {
  return [
    { title: "Aenir: A Fire Emblem stat calculator" },
    { name: "description", content: "Calculate Fire Emblem stats here!" },
  ];
}

{/* WIDGETS */}

function FatherSelect({choices, field, title, onClick}) {
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

export function MorphOption({missingParams, onClick}) {
  const possibleOptions = {
    father: ["Father", "select"],
    hard_mode: ["Hard Mode", "checkbox"],
    lyn_mode: ["Lyn Mode", "checkbox"],
    route: ["Route", "radio"],
    number_of_declines: ["Number of Declines", "number"],
  };
  const [field, choices] = missingParams;
  const [title, inputType] = possibleOptions[field];
  return {
    "select": (
      <FatherSelect choices={choices} field={field} title={title} onClick={onClick} />
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

{/* IMAGES */}

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

export async function unitStatsLoader( {initParams} ) {
  const sourceUrl = "http://127.0.0.1:8000/dracogate/api/initializate_morph/";
  // containers for output
  let currentCls = null;
  let currentLv = null;
  let currentStats = null;
  let missingParams = null;
  let missingParams2 = null;
  let currentMaxes = null;
  let _;
  console.log("About to send POST request to URL.");
  await axios
    .post(sourceUrl,
      {data: initParams},
    )
    .then(res => {
      const data = res.data;
      const [success, value, value2, fetchedCls, fetchedLv] = data;
      console.log("Data has been fetched.");
      if (success) {
        currentStats = value;
        currentMaxes = value2;
        [currentCls, currentLv] = [fetchedCls, fetchedLv];
        console.log("Unit has been found. Level: " + currentLv);
      } else {
        missingParams = value;
        missingParams2 = value2;
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
    if (missingParams2 !== null) {
      const [field, choices] = missingParams;
      const defaultVal = choices[0];
      initParams[field] = defaultVal;
    };
    await axios
      .post(sourceUrl,
        {data: initParams},
      )
      .then(res => {
        const data = res.data;
        const [_, value, value2, fetchedCls, fetchedLv] = data;
        currentStats = value;
        currentMaxes = value2;
      })
      .catch(err => console.log(err));
  };
  console.log("End of unitStatsLoader");
  return [currentCls, currentLv, currentStats, currentMaxes, missingParams, missingParams2];
};

function App() {
  {/* STATE VARIABLES */}
  {/* For rendering */}
  const nullGame = {
    no: 0,
    name: '',
    title: '',
  };
  const [game, setGame] = useState(nullGame);
  const nullInitParams = {
    game: null,
    name: null,
  };
  const [initParams, setInitParams] = useState(nullInitParams);
  const nullMissingParams = null;
  {/* for submitting extra data to server */}
  const [missingParams, setMissingParams] = useState(nullMissingParams);
  const [missingParams2, setMissingParams2] = useState(nullMissingParams);
  const nullMorph = {
    ...nullInitParams,
    currentCls: null,
    currentLv: null,
    currentStats: null,
    currentMaxes: null,
    maxStats: null,
    history: null,
  };
  const [morph, setMorph] = useState(nullMorph);
  const feGames = getFireEmblemGames();
  const unitList = getUnitList({gameNo: game.no});
  async function tryCreateMorph(e) {
    const unitName = e.currentTarget.dataset.unit;
    const tempInitParams = {
      game: game.no,
      name: unitName,
    };
    unitStatsLoader({initParams: tempInitParams})
      .then(res => {
        const [fetchedCls, fetchedLv, fetchedStats, fetchedMaxes, fetchedParams, fetchedParams2] = res;
        setInitParams(tempInitParams);
        setMissingParams(fetchedParams);
        setMissingParams2(fetchedParams2);
        setMorph(
          {
            ...morph,
            currentMaxes: fetchedMaxes,
            currentCls: fetchedCls,
            currentLv: fetchedLv,
            currentStats: fetchedStats,
          }
        );
      })
      .catch(err => console.log(err));
  };
  async function retryCreateMorph(e) {
    const inputWidget = e.currentTarget;
    const field = inputWidget.dataset.fieldname;
    let value = inputWidget.value;
    if (inputWidget.type === "checkbox") {
      value = inputWidget.checked;
    } else if (field === "father") {
      const fatherName = inputWidget.value;
      const fatherPreview = document.getElementById("father-preview");
      const fatherImgSrc = `/static/genealogy-of-the-holy-war/characters/${fatherName}.png`;
      fatherPreview.src = fatherImgSrc;
      fatherPreview.alt = fatherImgSrc;
    };
    const tempInitParams = {...initParams};
    tempInitParams[field] = value;
    let _;
    unitStatsLoader({initParams: tempInitParams})
      .then(res => {
        const [_, fetchedStats, fetchedMaxes, fetchedCls, fetchedLv] = res.data;
        setInitParams(tempInitParams);
        setMorph(
          {
            ...morph,
            currentCls: fetchedCls,
            currentLv: fetchedLv,
            currentStats: fetchedStats,
            currentMaxes: fetchedMaxes,
          }
        );
      })
      .catch(err => console.log(err));
  };
  async function submitMorph(e) {
    alert("submitMorph");
  };
  return (
    <>
    <figure id="game-cover">
    {game.no !== 0 && (
      <>
      <img src={`/static/${game.name}/cover-art.png`} alt={`Cover art of FE${game.no}: ${game.title}`} />
      <figcaption>
        {game.title}
      </figcaption>
      </>
      )
    }
    </figure>
    <form id="morph-initializer">
      <label htmlFor="game-select">Select FE Game (4-9)</label>
      <select name="game" id="game-select">
        <option key="" value="" onClick={() => setGame(nullGame)}>{''}</option>;
        {feGames.map(currentGame => {
          const {no, title, name} = currentGame;
          return <option key={name} onClick={() => setGame(currentGame)}>{title}</option>;
        })
        }
      </select>
      <menu id="unit-selector">
      {unitList !== undefined && (
          unitList.map(name => {
            const imgSuffix = game.no === 8 ? "gif" : "png";
            const imgFile = `${name}.${imgSuffix}`;
            return (
              <li key={name}>
              <button data-unit={name} onClick={tryCreateMorph} type="button">
                <figure>
                  <img src={`/static/${game.name}/characters/${imgFile}`} alt={`Portrait of ${name}, ${imgFile}`} />
                  <figcaption>
                    {name}
                  </figcaption>
                </figure>
              </button>
              </li>
            );
          })
        )
      }
      </menu>
      {missingParams !== null && <MorphOption missingParams={missingParams} onClick={retryCreateMorph} /> }
      {missingParams2 !== null && <MorphOption missingParams={missingParams2} onClick={retryCreateMorph} /> }
      <button type="button" onClick={submitMorph}>
        Create Morph!
      </button>
      </form>
    <table id="stats-table">
      <tbody>
        {morph.currentStats !== null && morph.currentCls !== null && morph.currentLv !== null (
          (
            <>
            <tr>
              <th>Class</th>
              <td>{morph.currentCls}</td>
            </tr>
            <tr>
              <th>Lv</th>
              <td>{morph.currentLv}</td>
            </tr>
            </>
          )
          (
             morph.currentStats.map(statVal => {
               const [stat, value] = statVal;
               return (
                 <tr>
                   <th>{stat}</th>
                   <td>{value}</td>
                 </tr>
               );
             })
          )
        )}
      </tbody>
    </table>
    </>
  );
};

export default App;
