import {
  Form,
} from 'react-router';

function UnitConfirmMenu() {
  return (
    <Form>
                <figure>
                  <img src={`/static/${game.name}/characters/${imgFile}`} alt={`Portrait of ${name}, ${imgFile}`} />
                  <figcaption>
                    {name}
                  </figcaption>
                </figure>
      {missingParams !== null && <MorphOption missingParams={missingParams} onClick={retryCreateMorph} /> }
      {missingParams2 !== null && <MorphOption missingParams={missingParams2} onClick={retryCreateMorph} /> }
      <button type="button" onClick={submitMorph}>
        Create Morph!
      </button>
      </form>
    <table id="stats-table">
      <tbody>
        {morph.currentCls !== null && (
            <tr key="Class">
              <th>Class</th>
              <td>{morph.currentCls}</td>
            </tr>
          )
        }
        {morph.currentLv !== null && (
            <tr key="Lv">
              <th>Lv</th>
              <td>{morph.currentLv}</td>
            </tr>
          )
        }
        {morph.currentStats !== null && (
          (
             morph.currentStats.map(statVal => {
               const [stat, value] = statVal;
               return (
                 <tr key={stat}>
                   <th>{stat}</th>
                   <td>{value}</td>
                 </tr>
               );
             })
          )
        )}
      </tbody>
    </table>
    </Form>
  );
};
