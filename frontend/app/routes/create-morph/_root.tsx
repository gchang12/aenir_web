import {
  redirect,
} from 'react-router';

function CreateMorph() {
  return <h1>CreateMorph</h1>;
};

export async function action({params, request}) {
  return redirect('/');
};

export default CreateMorph;
