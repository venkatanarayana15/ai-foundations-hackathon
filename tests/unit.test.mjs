import { test, describe } from 'node:test';
import assert from 'node:assert/strict';
import {
  normalizeDevanagari, levenshtein, responseMatches,
  startAssessment, nextItem, recordResponse, finishAssessment,
  classifyErrors, remediationFor, groupClass, classHeatmap, nextBestAction,
  createEventStore, stratifiedAssign, mdesCluster, quadraticWeightedKappa,
  tostEquivalent, toCsv,
} from '../src/engine.js';
import { contentPack } from '../src/content-pack.js';

describe('ASR matching (Devanagari-tolerant)', () => {
  test('exact match passes', () => {
    const item = { kind: 'read_aloud', prompt: 'किताब' };
    assert.equal(responseMatches(item, 'किताब'), true);
  });
  test('matra slip still matches (normalized)', () => {
    const item = { kind: 'read_aloud', prompt: 'किताब' };
    assert.equal(responseMatches(item, 'किताब्'), true);
    assert.equal(responseMatches(item, 'कताब'), true); // 1 char off
  });
  test('wrong word rejected', () => {
    const item = { kind: 'read_aloud', prompt: 'किताब' };
    assert.equal(responseMatches(item, 'रास्ता'), false);
  });
  test('low ASR confidence tightens tolerance', () => {
    const item = { kind: 'read_aloud', prompt: 'किताब' };
    assert.equal(responseMatches(item, 'कताब', 0.2), false);
    assert.equal(responseMatches(item, 'कताब', 1.0), true);
  });
  test('audio_choice accepts any listed akshar', () => {
    const item = { kind: 'audio_choice', accepts: ['म', 'स', 'र'] };
    assert.equal(responseMatches(item, 'स'), true);
    assert.equal(responseMatches(item, 'त'), false);
  });
  test('empty transcript fails safely', () => {
    const item = { kind: 'read_aloud', prompt: 'किताब' };
    assert.equal(responseMatches(item, ''), false);
    assert.equal(responseMatches(item, null), false);
  });
  test('levenshtein correctness', () => {
    assert.equal(levenshtein('kitten', 'sitting'), 3);
    assert.equal(levenshtein('क', 'ख'), 1);
  });
  test('normalize strips matras and nukta', () => {
    assert.equal(normalizeDevanagari('किताब'), normalizeDevanagari('क ि ता ब'));
  });
});

describe('Adaptive ladder & stop rules', () => {
  const pack = contentPack;
  test('child who fails everything ends at pre_letter floor (ASER semantics)', () => {
    let s = startAssessment('literacy');
    for (let i = 0; i < 3; i++) {
      const it = nextItem(s, pack);
      s = recordResponse(s, it, { correct: false, timeMs: 5000 }, pack);
    }
    assert.equal(s.finished, true);
    assert.equal(s.finalLevel, 'pre_letter');
  });
  test('child who passes everything reaches story', () => {
    let s = startAssessment('literacy');
    while (!s.finished) {
      const it = nextItem(s, pack);
      s = recordResponse(s, it, { correct: true, timeMs: 3000 }, pack);
    }
    assert.equal(s.finalLevel, 'story');
    assert.equal(s.results.length <= 15, true, `should stay lean, got ${s.results.length}`);
  });
  test('level with 2 items (story) terminates correctly', () => {
    let s = startAssessment('literacy');
    // Push through all levels up to story
    const seq = ['letter', 'letter', 'letter', 'word', 'word', 'word', 'paragraph', 'paragraph', 'paragraph', 'story', 'story'];
    let guard = 0;
    while (!s.finished && guard++ < 20) {
      const it = nextItem(s, pack);
      s = recordResponse(s, it, { correct: true, timeMs: 2000 }, pack);
    }
    assert.equal(s.finalLevel, 'story');
  });
  test('timeout caps at 5 minutes and assigns last passed level', () => {
    let s = startAssessment('literacy');
    let i = 0;
    while (!s.finished && i < 40) {
      const it = nextItem(s, pack);
      s = recordResponse(s, it, { correct: true, timeMs: 26000 }, pack); // slow classroom
      i++;
    }
    assert.equal(s.timedOut, true);
    assert.ok(s.finalLevel);
  });
});

describe('Error taxonomy & remediation', () => {
  const pack = contentPack;
  test('borrowing error classified as NUM-ABS-01', () => {
    const item = pack.items.find((i) => i.itemId === 'NUM-ABS-001');
    let s = startAssessment('numeracy');
    // Force reaching abstract level: pass 3 concrete, 3 representational
    const conItems = pack.items.filter((i) => i.level === 'num_concrete');
    for (const it of conItems.slice(0, 3)) s = recordResponse(s, it, { correct: true, timeMs: 2000 }, pack);
    const repItems = pack.items.filter((i) => i.level === 'num_representation');
    for (const it of repItems.slice(0, 3)) s = recordResponse(s, it, { correct: true, timeMs: 2000 }, pack);
    const absItems = pack.items.filter((i) => i.level === 'num_abstract');
    s = recordResponse(s, absItems[0], { correct: false, timeMs: 2000, chosenAnswer: '25' }, pack);
    s = recordResponse(s, absItems[1], { correct: false, timeMs: 2000, chosenAnswer: '45' }, pack);
    s = recordResponse(s, absItems[2], { correct: true, timeMs: 2000 }, pack);
    const errs = classifyErrors(s, pack);
    const codes = errs.map((e) => e.code);
    assert.ok(codes.includes('NUM-ABS-01') || codes.includes('NUM-ABS-02'), `got ${codes}`);
  });
  test('remediation lookup returns NCERT ref for concrete stage', () => {
    const r = remediationFor('NUM-ABS-01', contentPack, { craStage: 'concrete' });
    assert.ok(r);
    assert.match(r.ncertRef, /Math-Magic-2/);
    assert.equal(r.craStage, 'concrete');
  });
  test('every pack item has NCERT ref + CBSE FLN (CI rule)', () => {
    for (const it of contentPack.items) {
      assert.ok(it.ncertRef && it.ncertRef.book && it.ncertRef.page, `missing ncertRef on ${it.itemId}`);
      assert.ok(it.cbseFln && it.cbseFln.length >= 3, `missing cbseFln on ${it.itemId}`);
    }
    for (const ec of contentPack.errorCodes) {
      assert.ok(ec.remediations.length >= 1, `no remediation for ${ec.code}`);
      for (const rem of ec.remediations) {
        assert.ok(rem.ncertRef && rem.craStage && rem.activity);
      }
    }
  });
});

describe('TaRL grouping', () => {
  test('groups by level band, respects max size 8', () => {
    const children = [];
    for (let i = 0; i < 20; i++) {
      children.push({ childId: `C${i}`, domain: 'literacy', level: i < 12 ? 'letter' : 'word', errorCodes: [] });
    }
    const groups = groupClass(children, { maxGroupSize: 8 });
    assert.equal(groups.length, 3); // 12 letters → 2 groups; 8 words → 1
    for (const g of groups) assert.ok(g.childIds.length <= 8);
  });
  test('unassessed children land in their own band', () => {
    const groups = groupClass([{ childId: 'X', domain: 'literacy', level: null }]);
    assert.equal(groups[0].level, 'unassessed');
  });
});

describe('Dashboard aggregation', () => {
  test('heatmap counts by level', () => {
    const dist = classHeatmap([
      { childId: 'A', domain: 'literacy', level: 'word' },
      { childId: 'B', domain: 'literacy', level: 'word' },
      { childId: 'C', domain: 'literacy', level: 'letter' },
    ]);
    assert.equal(dist['literacy:word'], 2);
    assert.equal(dist['literacy:letter'], 1);
  });
  test('next best action cites NCERT page', () => {
    const children = [
      { childId: 'A', domain: 'literacy', level: 'word', errorCodes: [{ code: 'LIT-WRD-01' }] },
    ];
    const groups = groupClass(children);
    const actions = nextBestAction(children, groups, contentPack);
    assert.match(actions[0].ncertRef, /Rimjhim/);
  });
});

describe('Event store (offline-first contract)', () => {
  test('append is ordered and replayable', () => {
    const es = createEventStore('DEV-9');
    es.append('assessment_started', { childId: 'C1' });
    es.append('item_response', { childId: 'C1', itemId: 'LIT-LET-001', correct: true });
    es.append('assessment_completed', { childId: 'C1', finalLevel: 'letter' });
    assert.equal(es.events.length, 3);
    assert.equal(es.events[2].type, 'assessment_completed');
  });
  test('sync batches respect cursor and batch size', () => {
    const es = createEventStore('DEV-9');
    for (let i = 0; i < 1200; i++) es.append('item_response', { i });
    let cursor = 0, batches = 0;
    while (true) {
      const { batch, nextCursor } = es.exportBatch(cursor, 500);
      if (batch.length === 0) break;
      batches++;
      cursor = nextCursor;
      if (batches > 10) break;
    }
    assert.equal(batches, 3);
    assert.equal(cursor, 1200);
  });
  test('crash-resume: replay yields same state', () => {
    const es = createEventStore('DEV-9');
    es.append('a', { v: 1 });
    es.append('b', { v: 2 });
    const replayed = es.replay();
    assert.deepEqual(replayed.map((e) => e.type), ['a', 'b']);
  });
});

describe('Pilot statistics', () => {
  test('stratified assignment splits within strata', () => {
    const kids = Array.from({ length: 20 }, (_, i) => ({ childId: `C${i}`, grade: i % 2 ? 2 : 1 }));
    const assign = stratifiedAssign(kids, (c) => c.grade, 0.5, () => 0.42);
    const g1 = kids.filter((k) => k.grade === 1);
    const t1 = g1.filter((k) => assign.get(k.childId) === 'treatment').length;
    assert.equal(t1, 5); // half of grade-1 stratum
  });
  test('MDES at 2+2 clusters admits no learning-gain detection (>0.8 SD) — pilot pivots to fidelity endpoints', () => {
    const { mdes } = mdesCluster({ nClustersPerArm: 2, clusterSize: 25, icc: 0.15 });
    assert.ok(mdes > 0.8, `mdes=${mdes} — would imply the pilot could detect gains it cannot`);
  });
  test('more classrooms shrink MDES', () => {
    const a = mdesCluster({ nClustersPerArm: 2, clusterSize: 25, icc: 0.15 });
    const b = mdesCluster({ nClustersPerArm: 4, clusterSize: 25, icc: 0.15 });
    assert.ok(b.mdes < a.mdes);
  });
  test('kappa = 1 for perfect agreement', () => {
    const cats = ['letter', 'word', 'paragraph'];
    const a = ['letter', 'word', 'paragraph', 'word'];
    assert.equal(quadraticWeightedKappa(a, [...a], cats), 1);
  });
  test('kappa < 1 for noisy agreement', () => {
    const cats = ['letter', 'word', 'paragraph'];
    const a = ['letter', 'word', 'paragraph', 'word', 'letter'];
    const b = ['letter', 'word', 'paragraph', 'letter', 'word'];
    const k = quadraticWeightedKappa(a, b, cats);
    assert.ok(k > 0.4 && k < 1, `kappa=${k}`);
  });
  test('TOST passes when diff well inside ±0.2 SD margin', () => {
    const r = tostEquivalent(0.05, 0.05);
    assert.equal(r.pass, true);
  });
  test('TOST fails when diff outside margin', () => {
    const r = tostEquivalent(0.5, 0.05);
    assert.equal(r.pass, false);
  });
});

describe('CSV export', () => {
  test('quotes fields with commas', () => {
    const csv = toCsv([{ a: 'x,y', b: 1 }, { a: 'plain', b: 2 }]);
    const lines = csv.split('\n');
    assert.equal(lines[0], 'a,b');
    assert.equal(lines[1], '"x,y",1');
  });
});
