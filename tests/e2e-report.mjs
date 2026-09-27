// One-off: prints the key E2E evidence numbers for the README / pitch tech doc.
import {
  startAssessment, nextItem, recordResponse, finishAssessment, responseMatches,
  groupClass, classHeatmap, nextBestAction, mdesCluster, quadraticWeightedKappa,
} from '../src/engine.js';
import { contentPack } from '../src/content-pack.js';
import { makeSyntheticClass, simulateAssessment, mulberry32 } from './simulator.mjs';

const ENGINE = { startAssessment, nextItem, recordResponse, finishAssessment, responseMatches };

function runClassroom({ n = 45, db = 50, seed = 42 } = {}) {
  const children = makeSyntheticClass(n, seed);
  const rand = mulberry32(7);
  const results = children.map((c) => simulateAssessment(c, contentPack, ENGINE, { db, rand, domain: 'literacy' }));
  return { children, results };
}

function metrics({ db, seed }) {
  const { children, results } = runClassroom({ n: 45, db, seed });
  const stable = results.filter((r) => r.finalLevel !== null).length;
  const totalItems = results.reduce((s, r) => s + r.nItems, 0);
  const overrides = results.reduce((s, r) => s + r.overrides, 0);
  const cats = ['pre_letter', 'letter', 'word', 'paragraph', 'story'];
  const kappa = quadraticWeightedKappa(
    results.map((r) => r.finalLevel ?? 'pre_letter'),
    children.map((c) => c.trueReadingLevel),
    cats
  );
  const medItems = [...results.map((r) => r.nItems)].sort((a, b) => a - b)[Math.floor(results.length / 2)];
  return {
    db,
    stablePct: ((stable / 45) * 100).toFixed(1),
    overridePct: ((overrides / totalItems) * 100).toFixed(1),
    kappa: kappa.toFixed(3),
    medItems,
  };
}

const m50 = metrics({ db: 50, seed: 42 });
const m60 = metrics({ db: 60, seed: 99 });
const mdes = mdesCluster({ nClustersPerArm: 2, clusterSize: 25, icc: 0.15 });

// Dashboard snapshot at 50 dB
const { children, results } = runClassroom({ db: 50, seed: 42 });
const kids = children.map((c, i) => ({
  childId: c.childId, domain: 'literacy', level: results[i].finalLevel,
  errorCodes: [{ code: 'LIT-WRD-01' }],
}));
const groups = groupClass(kids, { maxGroupSize: 8 });
const actions = nextBestAction(kids, groups, contentPack);

console.log('=== E2E evidence (45-kid simulated classroom) ===');
console.log(`50 dB : stable=${m50.stablePct}%  override=${m50.overridePct}%  κ=${m50.kappa}  median items/child=${m50.medItems}`);
console.log(`60 dB : stable=${m60.stablePct}%  override=${m60.overridePct}%  κ=${m60.kappa}  median items/child=${m60.medItems}`);
console.log(`MDES (2+2 clusters, 25 kids, ICC 0.15): ${mdes.mdes.toFixed(2)} SD  → learning-gain detection NOT credible at this scale`);
console.log(`Groups formed: ${groups.length} (max 8/child per group)`);
console.log(`Heatmap: ${JSON.stringify(classHeatmap(kids))}`);
console.log('Next best action (first 3):');
for (const a of actions.slice(0, 3)) console.log(`  - ${a.groupId} [${a.level}] n=${a.nChildren}: ${a.activity} (${a.ncertRef})`);
