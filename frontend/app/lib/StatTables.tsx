import type {
  Unit,
  Stats,
} from "../lib/_types";

function NonNumericalStats(unit: Unit) {
  return (
    <>
      <tr>
        <th>Class</th>
        <td>{unit.class}</td>
      </tr>
      <tr>
        <th>Lv</th>
        <td>{unit.lv}</td>
      </tr>
    </>
  );
};

function NumericalStats(stats: Stats) {
  return (
    <>
    {stats.map(fieldValue => {
      const [field, value] = fieldValue;
      return (
        <tr key={field}>
          <th>{field}</th>
          <td>{value}</td>
        </tr>
      );
    })
    }
    </>
  );
};

export function StatTable({unit, stats} : { unit: Unit; stats: Stats }) {
  return (
    <table className="StatTable">
      <thead>
      <NonNumericalStats unit={unit} />
      </thead>
      <tbody>
      <NumericalStats stats={stats} />
      </tbody>
    </table>
  );
};

