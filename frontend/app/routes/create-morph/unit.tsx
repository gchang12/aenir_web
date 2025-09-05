import {
  useState,
  useEffect,
} from 'react';
import {
  Form,
  useParams,
  useNavigate,
  redirect,
} from 'react-router';

import axios from 'axios';

import {
  findFireEmblemGame,
} from '../../utility/functions';

function FatherSelect({choices, field, title, onClick}) {
  return (
    <>
      <label htmlFor={field}>{title}</label>
      <select name="father" id={field}>
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
          <div className="route" key={choice}>
            <label htmlFor={field}>{choice}</label>
            <input type="radio" id={choice} name={field} data-fieldname={field} onClick={onClick} />
          </div>
        );
      })}
    </fieldset>
  );
};

function NumberWidget({choices, field, title, onClick}) {
  return (
    <>
      <label htmlFor={field}>{title}</label>
      <input type="number" id={field} name={field} defaultValue="0" min="0" max={choices.length - 1} data-fieldname={field} onClick={onClick} />
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

function MorphOption({missingParams, onClick}) {
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

async function initializeUnit( {tempInitParams} ) {
  const sourceUrl = "http://127.0.0.1:8000/dracogate/api/initialize_morph/";
  // containers for output
  let cls = null;
  let lv = null;
  let stats = null;
  let maxes = null;
  let params1 = null;
  let params2 = null;
  const initParams = {...tempInitParams};
  {/* console.log("First POST with data: " + Object.entries(initParams)); */}
  const [success, data] = (await axios.get(sourceUrl, {params: initParams})).data;
  if (success) {
    const {current_stats, current_maxes, current_cls, current_lv} = data;
    [stats, maxes, cls, lv] = [current_stats, current_maxes, current_cls, current_lv];
  } else {
    const { missing_params, missing_params2 } = data;
    [params1, params2] = [missing_params, missing_params2];
  };
  if (params1 !== null || params2 !== null) {
    if (params1 !== null) {
      const [field, choices] = params1;
      const defaultVal = choices[0];
      initParams[field] = defaultVal;
    };
    if (params2 !== null) {
      const [field, choices] = params2;
      const defaultVal = choices[0];
      initParams[field] = defaultVal;
    };
    {/* console.log("Second POST with data: " + Object.entries(initParams)); */}
    const [_, data] = (await axios.get(sourceUrl, {params: initParams},)).data;
    const { current_stats, current_maxes, current_cls, current_lv } = data;
    [stats, maxes, cls, lv] = [current_stats, current_maxes, current_cls, current_lv];
  };
  return {data: {cls, lv, stats, maxes, params1, params2}};
};

export async function clientLoader({params}: Route.LoaderArgs) {
  const { feGame, feUnit } = params;
  const game = findFireEmblemGame({feGame});
  const params0 = {
    game: game.no,
    name: feUnit,
  };
  const { cls, lv, stats, maxes, params1, params2, } = (await initializeUnit({tempInitParams: params0})).data;
  const morph0 = {
    currentCls: cls,
    currentLv: lv,
    currentStats: stats,
    currentMaxes: maxes,
  };
  console.log(`clientLoader: game='${game.title}', unit='${feUnit}', stats[HP]='${morph0.currentStats}`);
  return {game, feUnit, morph0, params0, params1, params2};
};

function UnitConfirmMenu({loaderData}: Route.ComponentProps) {
  const {game, feUnit, morph0, params0, params1, params2} = loaderData;
  console.log(`UnitConfirmMenu: game='${game.title}', unit='${feUnit}'`);
  const [morph, setMorph] = useState(morph0);
  const [initParams, setInitParams] = useState(params0);
  const [missingParams, setMissingParams] = useState(params1);
  const [missingParams2, setMissingParams2] = useState(params2);
  const imgSuffix = game.no === 8 ? "gif" : "png";
  const imgFile = `${feUnit}.${imgSuffix}`;
  async function recreateMorph(e) {
    const inputWidget = e.currentTarget;
    const field = inputWidget.dataset.fieldname;
    let value = inputWidget.value;
    if (field === "hard_mode") {
      value = inputWidget.checked;
    } else if (field === "father") {
      const fatherName = inputWidget.value;
      const fatherPreview = document.getElementById("father-preview");
      const fatherImgSrc = `/static/genealogy-of-the-holy-war/characters/${fatherName}.png`;
      fatherPreview.src = fatherImgSrc;
      fatherPreview.alt = fatherImgSrc;
    } else if (field === "number_of_declines") {
      value = Number(value);
    } else if (field === "route") {
      value = inputWidget.id;
    };
    const tempInitParams = {...initParams};
    tempInitParams[field] = value;
    const {cls, lv, stats, maxes, params1, params2} = (await initializeUnit({tempInitParams})).data;
    setInitParams(tempInitParams);
    setMorph(
      {
        ...morph,
        currentCls: cls,
        currentLv: lv,
        currentStats: stats,
        currentMaxes: maxes,
      }
    );
  };
  return (
    <div>
      <figure>
        <img src={`/static/${game.name}/characters/${imgFile}`} alt={`Portrait of ${feUnit}, ${imgFile}`} />
        <figcaption>
          {feUnit}
        </figcaption>
      </figure>
      <table id="stats-table">
        <tbody>
          <tr key="Class">
            <th>Class</th>
            <td>{morph.currentCls}</td>
          </tr>
          <tr key="Lv">
            <th>Lv</th>
            <td>{morph.currentLv}</td>
          </tr>
          {morph.currentStats.map(statVal => {
            const [stat, value] = statVal;
            return (
              <tr key={stat}>
                <th>{stat}</th>
                <td>{value}</td>
              </tr>
            );
          })
          }
        </tbody>
      </table>
      <Form action="/create-morph/" method="POST">
        <input value={game.no} name="game" type="hidden" readOnly />
        <input value={feUnit} name="unit" type="hidden" readOnly />
        {missingParams !== null && <MorphOption missingParams={missingParams} onClick={recreateMorph} /> }
        {missingParams2 !== null && <MorphOption missingParams={missingParams2} onClick={recreateMorph} /> }
        <button>Create Morph!</button>
      </Form>
    </div>
  );
};

export default UnitConfirmMenu;
