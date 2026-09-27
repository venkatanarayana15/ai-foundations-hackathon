// Classroom simulator (plam.md v2 §4 Phase 2).
// Synthetic class of 45 children with realistic ability distribution; a noisy
// ASR channel (45–60 dB) with confidence drop + character errors; teacher
// behaviours: 1-tap override, tap-fallback, interruption, child silence.

export function mulberry32(seed) {
  let a = seed >>> 0;
  return function () {
    a |= 0; a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) | 0;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

const LIT_LEVELS = ['pre_letter', 'letter', 'word', 'paragraph', 'story'];
const NUM_LEVELS = ['num_concrete', 'num_representation', 'num_abstract'];

export function makeSyntheticClass(n = 45, seed = 42) {
  const rand = mulberry32(seed);
  const children = [];
  for (let i = 0; i < n; i++) {
    const grade = 1 + Math.floor(rand() * 3); // Grades 1–3
    // Reading ability latent 0..1 — right-skewed like ASER (many at bottom).
    const latent = rand() ** 1.8;
    const trueReadingIdx = Math.min(4, Math.floor(latent * 5));
    const trueNumeracyIdx = Math.min(2, Math.floor((rand() ** 1.5) * 3));
    children.push({
      childId: `SCH01-CL${grade}-${String(i + 1).padStart(3, '0')}`,
      grade,
      gender: rand() < 0.48 ? 'F' : 'M',
      trueReadingIdx,
      trueNumeracyIdx,
      trueReadingLevel: LIT_LEVELS[trueReadingIdx],
      trueNumeracyLevel: NUM_LEVELS[trueNumeracyIdx],
      // 12% of kids go quiet / no-response on some items (real classroom).
      silentP: 0.12,
      // ASR accuracy for this child's voice (varies).
      voiceQuality: 0.6 + rand() * 0.4,
    });
  }
  return children;
}

// Noisy ASR channel: real classroom noise is BURSTY per utterance — either the
// utterance comes through (mostly clean, confidence dips with dB) or it is
// largely lost. Per-char independent drops badly model real IndicASR, which
// stays near-clean on most utterances even at 60 dB.
export function asrChannel(text, { db = 50, voiceQuality = 0.8, rand = Math.random } = {}) {
  const noise = Math.max(0, (db - 40) / 20); // 0 @40dB → 1 @60dB
  const pFail = Math.min(0.45, 0.04 + noise * 0.25 * (1.15 - voiceQuality));
  const chars = [...String(text)];
  let transcript;
  if (rand() < pFail) {
    transcript = chars.filter(() => rand() > 0.55).join(''); // utterance lost
  } else {
    transcript = chars.filter(() => rand() > 0.02).join(''); // near-clean
  }
  const clean = transcript.length >= Math.ceil(chars.length * 0.9);
  const confidence = Math.max(0.15, Math.min(1, (clean ? 0.85 : 0.25) * voiceQuality + (rand() - 0.5) * 0.08));
  return { transcript, confidence };
}

// Runs one full assessment for one child, simulating the teacher + ASR.
// domain: 'literacy' | 'numeracy'
export function simulateAssessment(child, pack, engine, { db = 50, rand = mulberry32(7), domain = 'literacy', interruptions = 0 } = {}) {
  let state = engine.startAssessment(domain);
  const ladderIdxKey = domain === 'literacy' ? 'trueReadingIdx' : 'trueNumeracyIdx';
  let timeBudget = 5 * 60 * 1000;
  const responses = [];

  while (!state.finished) {
    const item = engine.nextItem(state, pack);
    if (!item) { state = engine.finishAssessment(state); break; }

    // Child silence?
    if (rand() < child.silentP) {
      timeBudget -= item.maxTimeMs;
      state = engine.recordResponse(state, item, { correct: false, timeMs: item.maxTimeMs, transcript: '', chosenAnswer: null }, pack);
      continue;
    }

    if (item.kind === 'tap_answer') {
      // Does the child know it? Latent ability decides (domain-correct index).
      const ownIdx = domain === 'literacy' ? child.trueReadingIdx : child.trueNumeracyIdx;
      const knowsIt = rand() < Math.max(0.08, 1 - Math.abs(ownIdx - ladderLevelIndex(item.level, domain)) * 0.34);
      const chosen = knowsIt ? item.correctIndex : Math.floor(rand() * item.choices.length);
      const correct = chosen === item.correctIndex;
      timeBudget -= Math.min(item.maxTimeMs, 4000 + rand() * 6000);
      state = engine.recordResponse(state, item, { correct, timeMs: 4000 + rand() * 6000, chosenAnswer: item.choices[chosen] }, pack);
      continue;
    }

    // read_aloud / audio_choice → through the noisy ASR channel.
    // The child's knowledge is drawn ONCE per item: the teacher can only
    // override what the child actually said (no second-chance knowing).
    const knows = childKnowsText(child, item, rand);
    // Speak the ANSWER in the item's modality — audio_choice children say the
    // akshar, not the instruction sentence (modality bug otherwise floods
    // pre_letter with spurious overrides).
    const spoken = spokenFor(item, knows, rand);
    let { transcript, confidence } = asrChannel(spoken, { db, voiceQuality: child.voiceQuality, rand });
    if (confidence < 0.45) {
      const second = asrChannel(spoken, { db, voiceQuality: child.voiceQuality, rand });
      if (second.confidence > confidence) { transcript = second.transcript; confidence = second.confidence; }
    }
    let correct = engine.responseMatches(item, transcript, confidence);
    let override = false;

    // Teacher 1-tap override when ASR is wrong but teacher heard it right.
    if (!correct && knows) {
      correct = true; override = true;
    }

    timeBudget -= Math.min(item.maxTimeMs, 3000 + rand() * 5000);
    state = engine.recordResponse(state, item, { correct, timeMs: 3000 + rand() * 5000, transcript, asrConfidence: confidence, teacherOverride: override }, pack);
  }

  return {
    childId: child.childId,
    domain,
    finalLevel: state.finalLevel,
    timedOut: state.timedOut,
    nItems: state.results.length,
    overrides: state.results.filter((r) => r.teacherOverride).length,
    elapsedMs: 5 * 60 * 1000 - Math.max(0, timeBudget),
  };
}

function ladderLevelIndex(level, domain) {
  return (domain === 'literacy' ? LIT_LEVELS : NUM_LEVELS).indexOf(level);
}

function childKnowsText(child, item, rand) {
  const target = ladderLevelIndex(item.level, item.domain);
  const own = item.domain === 'literacy' ? child.trueReadingIdx : child.trueNumeracyIdx;
  if (own > target) return true;
  if (own === target) return rand() < 0.75; // shaky at own level
  return rand() < 0.06; // lucky guess below level
}

function spokenFor(item, knows, rand) {
  if (item.kind === 'audio_choice') {
    const accepts = item.accepts ?? [];
    if (knows && accepts.length) return accepts[Math.floor(rand() * accepts.length)];
    const others = ['क', 'ख', 'ग', 'घ', 'च', 'ज', 'ट', 'ण', 'प', 'ब', 'म', 'ल', 'व'].filter((c) => !accepts.includes(c));
    return others[Math.floor(rand() * others.length)];
  }
  return knows ? item.prompt : corruptAttempt(item.prompt, rand);
}

function corruptAttempt(text, rand) {
  // A child who can't read it yet — a REALISTIC misread: keeps some chars,
  // swaps others for wrong ones (kids misread; they don't just stop midway).
  // A clean prefix would be trivially accepted by substring matching.
  const chars = [...String(text)];
  const keepN = Math.max(1, Math.floor(chars.length * (0.4 + rand() * 0.4)));
  const others = ['क', 'ख', 'ग', 'घ', 'च', 'ज', 'ट', 'ण', 'प', 'ब', 'म', 'ल', 'व'];
  return chars
    .map((ch, i) => {
      if (i >= keepN) return '';
      return rand() < 0.45 ? others[Math.floor(rand() * others.length)] : ch;
    })
    .join('');
}
