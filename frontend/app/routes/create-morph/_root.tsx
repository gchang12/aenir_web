import {
  redirect,
} from 'react-router';

import axios from 'axios';

function CreateMorph() {
  return <h1>CreateMorph</h1>;
};

export async function action({params, request}) {
  // send parameters to server
  // server saves morph to session
  // server loads session morphs into root
  console.log(`params: ${params}`);
  console.log(`request: ${request}`);
  const sourceUrl = `http://127.0.0.1:8000/dracogate/api/initialize_morph/`;
  await axios.put(sourceUrl, {data: params});
  return redirect('/');
};

export default CreateMorph;
