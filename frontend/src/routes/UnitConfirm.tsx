import {
  useLoaderData,
} from "react-router";

function UnitConfirm2() {
  return (
    <form>
      <div>
        <h1>Game Name</h1>
        <figure>
          <img src="" />
          <figcaption>Unit Name</figcaption>
        </figure>
        <table>
          <tbody>
            <tr>
              <th>Lv</th>
              <td>0</td>
            </tr>
            <tr>
              <th>Class</th>
              <td></td>
            </tr>
            <tr>
              <th>Option</th>
              <td>Widget</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div>
        <table>
          <tbody>
            <tr>Stat-Name</tr>
            <td>Stat-Value</td>
          </tbody>
        </table>
      </div>
      <button>Create</button>
    </form>
  );
};

function UnitConfirm() {
  const loaderData = useLoaderData();
  const {morph, missingParams, unitName, gameId} = loaderData;
  const {stats, unitClass, level} = morph;
  const imgSuffix = gameId === "fe8" ? ".gif" : ".png";
  return (
    <>
    <form>
      <ProfileHead figureTitle={unitName} imgSrc={"/images/" + unitName + imgSuffix}>
        <table>
          <tbody>
          <ProfileLevelAndClass {...{unitClass, level}} />
          {/* OptionSelect */}
          </tbody>
        </table>
      </ProfileHead>
      <table>
        <tbody>
        <StatTable {...{stats, highlight: true}} />
        </tbody>
      </table>
      <button>Create!</button>
    </form>
    </>
  );
};

