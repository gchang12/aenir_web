import React from "react";
import type {
  Unit,
  Stats,
} from "../lib/_types";

function NonNumericalStats({ unit } : {unit: Unit}) : React.ReactElement {
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

function GlowingNumericalStats({ currentStats, maxStats } : { currentStats: Stats; maxStats: Stats }) : React.ReactElement {
  const stats: Array<[string, number, number]> = [];
  for (let i = 0; i < currentStats.length; i++) {
    stats.push([...currentStats[i], maxStats[i][1]]);
  };
  return (
    <>
    {stats.map(fieldStats => {
      const [field, currentStat, maxStat] = fieldStats;
      return (
        <tr key={field} className={currentStat === maxStat ? "maxed-stat" : undefined}>
          <th>{field}</th>
          <td>{currentStat / 100}</td>
        </tr>
      );
    })
    }
    </>
  );
};

function NumericalStats({ stats } : { stats: Stats }) : React.ReactElement {
  return (
    <>
    {stats.map(fieldValue => {
      const [field, value] = fieldValue;
      return (
        <tr key={field}>
          <th>{field}</th>
          <td>{value / 100}</td>
        </tr>
      );
    })
    }
    </>
  );
};

export function StatTable({unit, stats} : { unit: Unit; stats: Stats }) : React.ReactNode {
  return (
    <table className="StatTable">
      <thead>
      <NonNumericalStats {...{unit}} />
      </thead>
      <tbody>
      <NumericalStats {...{stats}} />
      </tbody>
    </table>
  );
};

export function GlowingStatTable({unit, currentStats, maxStats} : { unit: Unit; currentStats: Stats; maxStats: Stats }) : React.ReactNode {
  return (
    <table className="StatTable">
      <thead>
      <NonNumericalStats {...{unit}} />
      </thead>
      <tbody>
      <GlowingNumericalStats {...{currentStats, maxStats}} />
      </tbody>
    </table>
  );
};

