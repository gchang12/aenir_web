
function ProfileHead({figureTitle, imgSrc, children}) {
  return (
    <>
    <figure>
      <img src={imgSrc} alt={imgSrc} />
      <figcaption>
        <h2>{figureTitle}</h2>
        <div className="ProfileHead-children">{children}</div>
      </figcaption>
    </figure>
    </>
  );
};

function ProfileLevelAndClass({unitClass, level}) {
  const [currentLv, maxLv] = level;
  return (
    <>
    <tr>
      <th>Class</th>
      <td>{unitClass}</td>
    </tr>
    <tr>
      <th>Lv</th>
      <td>{currentLv} / {maxLv}</td>
    </tr>
    </>
  );
};

function StatTable({stats, highlight}) {
  const className = highlight === true ? "maxed-stat" : undefined;
  return (
    <>
    {stats.map(([stat, currentValue, localMax, absMax]) => {
      return (
        <tr key={stat} className={currentValue === localMax ? className : undefined}>
          <td>{currentValue}</td>
          <td>
            <meter min="0" value={currentValue} max={absMax} high={localMax}></meter>
          </td>
        </tr>
      );
    })
    }
    </>
  );
};

export {
  StatTable,
};
