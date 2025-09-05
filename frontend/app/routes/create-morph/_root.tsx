import {
  redirect,
} from 'react-router';

function CreateMorph() {
  return <h1>CreateMorph</h1>;
};

export async function action({params, request}) {
  // send parameters to server
  // server saves morph to session
  // server loads session morphs into root
  return redirect('/');
};

export default CreateMorph;
