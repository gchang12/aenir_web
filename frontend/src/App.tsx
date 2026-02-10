import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <div>
        <a href="https://vite.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <p>
          Edit <code>src/App.tsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
    </>
  )
}

export default App

// MY CODE

import axios from 'axios';

function getMorph(game_no, name, kwargs) {
  const RESOURCE_URL: string = "http://localhost:8000/dracogate/api/morphs/";
  const params = {
    game_no,
    name,
    ...kwargs,
  };
  const fetchTask = axios
    .get(RESOURCE_URL, {params})
    .then(resp => resp.data)
    .catch(err => console.log(err));
  return fetchTask;
};

async function previewMorph(game_no, name, kwargs) {
  let morph = await getMorph(game_no, name, kwargs);
  const { missingParams } = morph;
  if (typeof missingParams === 'object') {
    const kwargs2 = {...kwargs};
    Object.entries(missingParams).forEach(entry => {
      const [key, values] = entry;
      const [defaultVal] = values;
      kwargs2[key] = defaultVal;
    });
    morph = await getMorph(game_no, name, kwargs2);
  };
  return { morph, missingParams };
};

export {
  getMorph,
  previewMorph,
};

