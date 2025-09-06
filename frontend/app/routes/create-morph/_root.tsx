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
  const sourceUrl = "http://127.0.0.1:8000/dracogate/api/initialize_morph/";
  const formData = await request.formData();
  const initParams = Object.fromEntries(formData);
  await axios.post(sourceUrl, {data: initParams});
  return redirect('/'); // where everything in session['morphs'] will be listed. limit: 5. stuff has to expire.
};

export default CreateMorph;
