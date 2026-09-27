// Content pack v1 — Hindi pilot pack.
// Every item carries an NCERT page ref + CBSE FLN skill (CI-enforced by validatePack).
export const contentPack = {
  packVersion: '1.0.0',
  languages: ['hi'],
  items: [
    // ---------- LITERACY: pre_letter (K5 entry gate, 10s) ----------
    {
      itemId: 'LIT-PRE-001', domain: 'literacy', level: 'pre_letter',
      kind: 'audio_choice', prompt: 'अपने नाम का पहला अक्षर बताओ',
      accepts: ['म', 'स', 'र'], maxTimeMs: 10000,
      ncertRef: { book: 'Rimjhim-1', page: 4 }, cbseFln: 'FLN-L-0.1 Name/letter recognition',
      acceptsTapFallback: true,
    },
    {
      itemId: 'LIT-PRE-002', domain: 'literacy', level: 'pre_letter',
      kind: 'audio_choice', prompt: 'अपने नाम का पहला अक्षर बताओ',
      accepts: ['प', 'क', 'ट'], maxTimeMs: 10000,
      ncertRef: { book: 'Rimjhim-1', page: 4 }, cbseFln: 'FLN-L-0.1 Name/letter recognition',
      acceptsTapFallback: true,
    },
    {
      itemId: 'LIT-PRE-003', domain: 'literacy', level: 'pre_letter',
      kind: 'audio_choice', prompt: 'यह अक्षर कौन-सा है?',
      accepts: ['क', 'ख', 'ग'], maxTimeMs: 10000,
      ncertRef: { book: 'Rimjhim-1', page: 5 }, cbseFln: 'FLN-L-0.1 Name/letter recognition',
      acceptsTapFallback: true,
    },
    {
      itemId: 'LIT-PRE-004', domain: 'literacy', level: 'pre_letter',
      kind: 'audio_choice', prompt: 'यह अक्षर कौन-सा है?',
      accepts: ['ध', 'द', 'थ'], maxTimeMs: 10000,
      ncertRef: { book: 'Rimjhim-1', page: 5 }, cbseFln: 'FLN-L-0.1 Name/letter recognition',
      acceptsTapFallback: true,
    },
    {
      itemId: 'LIT-PRE-005', domain: 'literacy', level: 'pre_letter',
      kind: 'audio_choice', prompt: 'यह अक्षर कौन-सा है?',
      accepts: ['अ', 'इ', 'उ'], maxTimeMs: 10000,
      ncertRef: { book: 'Rimjhim-1', page: 6 }, cbseFln: 'FLN-L-0.1 Name/letter recognition',
      acceptsTapFallback: true,
    },

    // ---------- LITERACY: letter ----------
    {
      itemId: 'LIT-LET-001', domain: 'literacy', level: 'letter',
      kind: 'read_aloud', prompt: 'क', maxTimeMs: 15000,
      ncertRef: { book: 'Rimjhim-1', page: 12 }, cbseFln: 'FLN-L-1.1 Akshar identification',
      acceptsTapFallback: true,
    },
    {
      itemId: 'LIT-LET-002', domain: 'literacy', level: 'letter',
      kind: 'read_aloud', prompt: 'म', maxTimeMs: 15000,
      ncertRef: { book: 'Rimjhim-1', page: 12 }, cbseFln: 'FLN-L-1.1 Akshar identification',
      acceptsTapFallback: true,
    },
    {
      itemId: 'LIT-LET-003', domain: 'literacy', level: 'letter',
      kind: 'read_aloud', prompt: 'स', maxTimeMs: 15000,
      ncertRef: { book: 'Rimjhim-1', page: 13 }, cbseFln: 'FLN-L-1.1 Akshar identification',
      acceptsTapFallback: true,
    },
    {
      itemId: 'LIT-LET-004', domain: 'literacy', level: 'letter',
      kind: 'read_aloud', prompt: 'थ', maxTimeMs: 15000,
      ncertRef: { book: 'Rimjhim-1', page: 13 }, cbseFln: 'FLN-L-1.1 Akshar identification',
      acceptsTapFallback: true,
    },
    {
      itemId: 'LIT-LET-005', domain: 'literacy', level: 'letter',
      kind: 'read_aloud', prompt: 'झ', maxTimeMs: 15000,
      ncertRef: { book: 'Rimjhim-1', page: 14 }, cbseFln: 'FLN-L-1.1 Akshar identification',
      acceptsTapFallback: true,
    },

    // ---------- LITERACY: word ----------
    {
      itemId: 'LIT-WRD-001', domain: 'literacy', level: 'word',
      kind: 'read_aloud', prompt: 'किताब', maxTimeMs: 20000,
      ncertRef: { book: 'Rimjhim-1', page: 24 }, cbseFln: 'FLN-L-2.1 Blend akshars into words',
      acceptsTapFallback: true,
    },
    {
      itemId: 'LIT-WRD-002', domain: 'literacy', level: 'word',
      kind: 'read_aloud', prompt: 'रास्ता', maxTimeMs: 20000,
      ncertRef: { book: 'Rimjhim-1', page: 24 }, cbseFln: 'FLN-L-2.1 Blend akshars into words',
      acceptsTapFallback: true,
    },
    {
      itemId: 'LIT-WRD-003', domain: 'literacy', level: 'word',
      kind: 'read_aloud', prompt: 'सूरज', maxTimeMs: 20000,
      ncertRef: { book: 'Rimjhim-1', page: 25 }, cbseFln: 'FLN-L-2.1 Blend akshars into words',
      acceptsTapFallback: true,
    },
    {
      itemId: 'LIT-WRD-004', domain: 'literacy', level: 'word',
      kind: 'read_aloud', prompt: 'पानी', maxTimeMs: 20000,
      ncertRef: { book: 'Rimjhim-1', page: 25 }, cbseFln: 'FLN-L-2.1 Blend akshars into words',
      acceptsTapFallback: true,
    },
    {
      itemId: 'LIT-WRD-005', domain: 'literacy', level: 'word',
      kind: 'read_aloud', prompt: 'मेला', maxTimeMs: 20000,
      ncertRef: { book: 'Rimjhim-1', page: 26 }, cbseFln: 'FLN-L-2.1 Blend akshars into words',
      acceptsTapFallback: true,
    },

    // ---------- LITERACY: paragraph / story ----------
    {
      itemId: 'LIT-PAR-001', domain: 'literacy', level: 'paragraph',
      kind: 'read_aloud', prompt: 'राम के पास एक किताब थी। वह रोज़ पढ़ता था।', maxTimeMs: 40000,
      ncertRef: { book: 'Rimjhim-2', page: 10 }, cbseFln: 'FLN-L-3.1 Read a short paragraph',
      acceptsTapFallback: true,
    },
    {
      itemId: 'LIT-PAR-002', domain: 'literacy', level: 'paragraph',
      kind: 'read_aloud', prompt: 'सीता बाज़ार गई। उसने फल खरीदे।', maxTimeMs: 40000,
      ncertRef: { book: 'Rimjhim-2', page: 11 }, cbseFln: 'FLN-L-3.1 Read a short paragraph',
      acceptsTapFallback: true,
    },
    {
      itemId: 'LIT-PAR-003', domain: 'literacy', level: 'paragraph',
      kind: 'read_aloud', prompt: 'मोर सुंदर पक्षी है। वह नाचता है।', maxTimeMs: 40000,
      ncertRef: { book: 'Rimjhim-2', page: 12 }, cbseFln: 'FLN-L-3.1 Read a short paragraph',
      acceptsTapFallback: true,
    },
    {
      itemId: 'LIT-PAR-004', domain: 'literacy', level: 'paragraph',
      kind: 'read_aloud', prompt: 'नदी में पानी बहता है। बच्चे खेलते हैं।', maxTimeMs: 40000,
      ncertRef: { book: 'Rimjhim-2', page: 12 }, cbseFln: 'FLN-L-3.1 Read a short paragraph',
      acceptsTapFallback: true,
    },
    {
      itemId: 'LIT-PAR-005', domain: 'literacy', level: 'paragraph',
      kind: 'read_aloud', prompt: 'अमीर कुएँ से पानी लाया। उसने माँ को दिया।', maxTimeMs: 40000,
      ncertRef: { book: 'Rimjhim-2', page: 13 }, cbseFln: 'FLN-L-3.1 Read a short paragraph',
      acceptsTapFallback: true,
    },
    {
      itemId: 'LIT-STO-001', domain: 'literacy', level: 'story',
      kind: 'read_aloud', prompt: 'एक थी लोमड़ी। वह बहुत चालाक थी। एक दिन वह बगीचे में गई। वहाँ अंगूर की बेल थी।', maxTimeMs: 60000,
      ncertRef: { book: 'Rimjhim-2', page: 40 }, cbseFln: 'FLN-L-4.1 Read a story fluently',
      acceptsTapFallback: true,
    },
    {
      itemId: 'LIT-STO-002', domain: 'literacy', level: 'story',
      kind: 'read_aloud', prompt: 'चींटी ने अनाज ढूँढा। वह घर ले गई। उसने सारे मित्रों को बुलाया। सबने मिलकर भोजन किया।', maxTimeMs: 60000,
      ncertRef: { book: 'Rimjhim-2', page: 41 }, cbseFln: 'FLN-L-4.1 Read a story fluently',
      acceptsTapFallback: true,
    },

    // ---------- NUMERACY: concrete (C-P-A: start concrete) ----------
    {
      itemId: 'NUM-CON-001', domain: 'numeracy', level: 'num_concrete',
      kind: 'tap_answer', prompt: 'तीन तितलियाँ दिख रही हैं। एक और आई। अब कितनी?',
      choices: ['3', '4', '5'], correctIndex: 1, maxTimeMs: 20000,
      ncertRef: { book: 'Math-Magic-1', page: 22 }, cbseFln: 'FLN-N-1.1 Counting objects',
      acceptsTapFallback: false,
    },
    {
      itemId: 'NUM-CON-002', domain: 'numeracy', level: 'num_concrete',
      kind: 'tap_answer', prompt: '5 गेंदें हैं। 2 रख दो। कितनी बचीं?',
      choices: ['2', '3', '4'], correctIndex: 1, maxTimeMs: 20000,
      ncertRef: { book: 'Math-Magic-1', page: 30 }, cbseFln: 'FLN-N-1.2 Take-away subtraction',
      acceptsTapFallback: false,
    },
    {
      itemId: 'NUM-CON-003', domain: 'numeracy', level: 'num_concrete',
      kind: 'tap_answer', prompt: '2 टोकरियाँ, हर एक में 3 सेब। कुल कितने?',
      choices: ['5', '6', '7'], correctIndex: 1, maxTimeMs: 20000,
      ncertRef: { book: 'Math-Magic-1', page: 45 }, cbseFln: 'FLN-N-1.3 Equal groups',
      acceptsTapFallback: false,
    },
    {
      itemId: 'NUM-CON-004', domain: 'numeracy', level: 'num_concrete',
      kind: 'tap_answer', prompt: '7 पत्ते हैं। 3 मुड़ गए। कितने सीधे बचे?',
      choices: ['3', '4', '5'], correctIndex: 1, maxTimeMs: 20000,
      ncertRef: { book: 'Math-Magic-1', page: 30 }, cbseFln: 'FLN-N-1.2 Take-away subtraction',
      acceptsTapFallback: false,
    },
    {
      itemId: 'NUM-CON-005', domain: 'numeracy', level: 'num_concrete',
      kind: 'tap_answer', prompt: '9 गिलास हैं। 4 निकाल लो। कितने बचे?',
      choices: ['4', '5', '6'], correctIndex: 1, maxTimeMs: 20000,
      ncertRef: { book: 'Math-Magic-1', page: 30 }, cbseFln: 'FLN-N-1.2 Take-away subtraction',
      acceptsTapFallback: false,
    },

    // ---------- NUMERACY: representational ----------
    {
      itemId: 'NUM-REP-001', domain: 'numeracy', level: 'num_representation',
      kind: 'tap_answer', prompt: '23 = 2 दहाई + कितनी इकाई?',
      choices: ['2', '3', '23'], correctIndex: 1, maxTimeMs: 20000,
      ncertRef: { book: 'Math-Magic-2', page: 15 }, cbseFln: 'FLN-N-2.1 Place value',
      acceptsTapFallback: false,
    },
    {
      itemId: 'NUM-REP-002', domain: 'numeracy', level: 'num_representation',
      kind: 'tap_answer', prompt: '4 दहाई 2 इकाई = कितनी संख्या?',
      choices: ['24', '42', '44'], correctIndex: 1, maxTimeMs: 20000,
      ncertRef: { book: 'Math-Magic-2', page: 15 }, cbseFln: 'FLN-N-2.1 Place value',
      acceptsTapFallback: false,
    },
    {
      itemId: 'NUM-REP-003', domain: 'numeracy', level: 'num_representation',
      kind: 'tap_answer', prompt: '9 + 4 = ? (10 का बंडल बनाओ)',
      choices: ['11', '12', '13'], correctIndex: 2, maxTimeMs: 20000,
      ncertRef: { book: 'Math-Magic-2', page: 30 }, cbseFln: 'FLN-N-2.2 Composing to 10',
      acceptsTapFallback: false,
    },
    {
      itemId: 'NUM-REP-004', domain: 'numeracy', level: 'num_representation',
      kind: 'tap_answer', prompt: '15 − 7 = ? (दहाई-इकाई सोचो)',
      choices: ['6', '7', '8'], correctIndex: 2, maxTimeMs: 20000,
      ncertRef: { book: 'Math-Magic-2', page: 30 }, cbseFln: 'FLN-N-2.2 Composing to 10',
      acceptsTapFallback: true,
    },
    {
      itemId: 'NUM-REP-005', domain: 'numeracy', level: 'num_representation',
      kind: 'tap_answer', prompt: '10 + 7 = ?',
      choices: ['15', '16', '17'], correctIndex: 2, maxTimeMs: 20000,
      ncertRef: { book: 'Math-Magic-2', page: 30 }, cbseFln: 'FLN-N-2.2 Composing to 10',
      acceptsTapFallback: false,
    },

    // ---------- NUMERACY: abstract (incl. borrowing diagnostics) ----------
    {
      itemId: 'NUM-ABS-001', domain: 'numeracy', level: 'num_abstract',
      kind: 'tap_answer', prompt: '52 − 37 = ?', borrowRequired: true,
      choices: ['15', '25', '24'], correctIndex: 0, maxTimeMs: 30000,
      ncertRef: { book: 'Math-Magic-2', page: 45 }, cbseFln: 'FLN-N-3.1 Subtraction with regrouping',
      acceptsTapFallback: false,
    },
    {
      itemId: 'NUM-ABS-002', domain: 'numeracy', level: 'num_abstract',
      kind: 'tap_answer', prompt: '63 − 28 = ?', borrowRequired: true,
      choices: ['35', '45', '44'], correctIndex: 0, maxTimeMs: 30000,
      ncertRef: { book: 'Math-Magic-2', page: 45 }, cbseFln: 'FLN-N-3.1 Subtraction with regrouping',
      acceptsTapFallback: false,
    },
    {
      itemId: 'NUM-ABS-003', domain: 'numeracy', level: 'num_abstract',
      kind: 'tap_answer', prompt: '34 + 25 = ?', borrowRequired: false,
      choices: ['49', '59', '58'], correctIndex: 0, maxTimeMs: 30000,
      ncertRef: { book: 'Math-Magic-2', page: 45 }, cbseFln: 'FLN-N-3.1 Addition without regrouping',
      acceptsTapFallback: false,
    },
    {
      itemId: 'NUM-ABS-004', domain: 'numeracy', level: 'num_abstract',
      kind: 'tap_answer', prompt: '80 − 45 = ?', borrowRequired: true,
      choices: ['35', '45', '44'], correctIndex: 0, maxTimeMs: 30000,
      ncertRef: { book: 'Math-Magic-2', page: 45 }, cbseFln: 'FLN-N-3.1 Subtraction with regrouping',
      acceptsTapFallback: false,
    },
    {
      itemId: 'NUM-ABS-005', domain: 'numeracy', level: 'num_abstract',
      kind: 'tap_answer', prompt: '71 − 26 = ?', borrowRequired: true,
      choices: ['45', '46', '55'], correctIndex: 0, maxTimeMs: 30000,
      ncertRef: { book: 'Math-Magic-2', page: 45 }, cbseFln: 'FLN-N-3.1 Subtraction with regrouping',
      acceptsTapFallback: false,
    },
  ],
  errorCodes: [
    {
      code: 'LIT-PRE-01', label: 'Cannot identify first akshar of own name',
      detect: { domain: 'literacy', level: 'pre_letter', signal: { kind: 'exact_miss', value: 'LIT-PRE-001' } },
      remediations: [
        { ncertRef: 'Rimjhim-1 p.4', craStage: 'concrete', activity: 'Name-card game: match child name cards to first akshar' },
        { ncertRef: 'Rimjhim-1 p.5', craStage: 'representational', activity: 'Trace first akshar in sand tray' },
      ],
      taRL: '1:1, concrete, child name as anchor',
    },
    {
      code: 'LIT-LET-01', label: 'Confuses similar akshars (थ/द)',
      detect: { domain: 'literacy', level: 'letter', signal: { kind: 'exact_miss', value: 'LIT-LET-004' } },
      remediations: [
        { ncertRef: 'Rimjhim-1 p.13', craStage: 'concrete', activity: 'Sorting: two akshar cards into two hoops' },
        { ncertRef: 'Rimjhim-1 p.13', craStage: 'representational', activity: 'Circle the odd akshar in a row' },
      ],
      taRL: 'Small group of 4–6, sorting games',
    },
    {
      code: 'LIT-WRD-01', label: 'Akshar-by-akshar reading, cannot blend',
      detect: { domain: 'literacy', level: 'word', signal: { kind: 'exact_miss', value: 'LIT-WRD-001' } },
      remediations: [
        { ncertRef: 'Rimjhim-1 p.24', craStage: 'concrete', activity: 'Sound-box: slide beads as each sound is said' },
        { ncertRef: 'Rimjhim-1 p.24', craStage: 'representational', activity: 'Arrow under akshars, blend while sliding finger' },
        { ncertRef: 'Rimjhim-1 p.24', craStage: 'abstract', activity: 'Read 5 words with no supports' },
      ],
      taRL: 'Small group, sound games first, then word reading',
    },
    {
      code: 'LIT-WRD-02', label: 'Matra errors (की/कि)',
      detect: { domain: 'literacy', level: 'word', signal: { kind: 'exact_miss', value: 'LIT-WRD-002' } },
      remediations: [
        { ncertRef: 'Rimjhim-1 p.26', craStage: 'concrete', activity: 'Matra hoops: sort word cards by matra' },
        { ncertRef: 'Rimjhim-1 p.26', craStage: 'abstract', activity: 'Read 5 matra words unaided' },
      ],
      taRL: 'Small group, matra sorting before reading',
    },
    {
      code: 'NUM-CON-01', label: 'Cannot count objects 1:1',
      detect: { domain: 'numeracy', level: 'num_concrete', signal: { kind: 'no_response', value: 'NUM-CON-001' } },
      remediations: [
        { ncertRef: 'Math-Magic-1 p.22', craStage: 'concrete', activity: 'Count real objects: stones, bottle caps' },
        { ncertRef: 'Math-Magic-1 p.22', craStage: 'representational', activity: 'Count pictures in Math-Magic' },
      ],
      taRL: '1:1 with manipulatives, 5 min daily',
    },
    {
      code: 'NUM-CON-02', label: 'Take-away subtraction with objects fails',
      detect: { domain: 'numeracy', level: 'num_concrete', signal: { kind: 'no_response', value: 'NUM-CON-002' } },
      remediations: [
        { ncertRef: 'Math-Magic-1 p.30', craStage: 'concrete', activity: 'Hide 2 of 5 stones under a cloth: "how many hidden?"' },
        { ncertRef: 'Math-Magic-1 p.30', craStage: 'representational', activity: 'Cross out 2 of 5 drawn circles' },
      ],
      taRL: 'Small group, hiding game daily',
    },
    {
      code: 'NUM-REP-01', label: 'Place value not understood (42 read as 24)',
      detect: { domain: 'numeracy', level: 'num_representation', signal: { kind: 'exact_miss', value: 'NUM-REP-002' } },
      remediations: [
        { ncertRef: 'Math-Magic-2 p.15', craStage: 'concrete', activity: 'Bundle sticks: 4 bundles of 10 + 2 loose' },
        { ncertRef: 'Math-Magic-2 p.15', craStage: 'representational', activity: 'Draw bundles and loose sticks' },
      ],
      taRL: 'Small group, bundles before symbols',
    },
    {
      code: 'NUM-ABS-01', label: 'Forgets borrowing (52−37 → says 25)',
      detect: { domain: 'numeracy', level: 'num_abstract', signal: { kind: 'borrow_needed', value: '52−37' } },
      remediations: [
        { ncertRef: 'Math-Magic-2 p.45', craStage: 'concrete', activity: 'Base-10 blocks: cannot take 7 ones from 2, trade a ten' },
        { ncertRef: 'Math-Magic-2 p.45', craStage: 'representational', activity: 'Draw the trade on place-value chart' },
        { ncertRef: 'Math-Magic-2 p.45', craStage: 'abstract', activity: 'Solve 3 borrowing problems unaided' },
      ],
      taRL: 'Small group, concrete trade first, then symbols',
    },
    {
      code: 'NUM-ABS-02', label: 'Avoids borrowing (52−37 → 25 via 2−7 flip)',
      detect: { domain: 'numeracy', level: 'num_abstract', signal: { kind: 'borrow_avoided', value: '52−37' } },
      remediations: [
        { ncertRef: 'Math-Magic-2 p.45', craStage: 'concrete', activity: 'Trade game: "can I take 7 from 2? No — trade!"' },
        { ncertRef: 'Math-Magic-2 p.45', craStage: 'abstract', activity: 'Check by adding back: 25 + 37 ≠ 52' },
      ],
      taRL: 'Small group, trade game daily',
    },
    {
      code: 'NUM-ABS-03', label: 'Borrows when not needed (34+25 → 69)',
      detect: { domain: 'numeracy', level: 'num_abstract', signal: { kind: 'borrow_needed', value: '34+25' } },
      remediations: [
        { ncertRef: 'Math-Magic-2 p.45', craStage: 'concrete', activity: 'Sort cards: borrow / no-borrow piles' },
      ],
      taRL: 'Small group, sort-then-solve',
    },
  ],

  // ---------------------------------------------------------------------------
  // Plan blocks — input to the offline PlanAssembler (ARCHITECTURE_OFFLINE.md §7).
  // Openers and closers run whole-class; `blocks` are differentiated per TaRL
  // band. Every entry MUST cite an NCERT page + CBSE FLN code — this is a CI
  // rule enforced by validatePlanContent(), not by trust.
  // ---------------------------------------------------------------------------
  openers: [
    {
      blockId: 'OPN-MELA-01', chapterId: 'RIMJHIM-1-MELA', domain: 'literacy', audience: 'whole_class',
      activity: 'सब मिलकर मेले की तस्वीर देखो और 3 चीज़ों के नाम बोलो',
      talkLine: 'बच्चो, इस तस्वीर में क्या-क्या दिख रहा है? ज़ोर से बोलो।',
      ncertRef: { book: 'Rimjhim-1', page: 20 }, cbseFln: 'FLN-L-0.2 Oral language & picture talk',
    },
    {
      blockId: 'OPN-SUB-01', chapterId: 'MATH-MAGIC-2-SUB', domain: 'numeracy', audience: 'whole_class',
      activity: 'गिनती की ताली: 10-10 की जोड़ी बनाओ',
      talkLine: 'दस तक गिनो, फिर 10 और 10 मिलाकर बीस।',
      ncertRef: { book: 'Math-Magic-2', page: 28 }, cbseFln: 'FLN-N-1.1 Counting & place value',
    },
  ],
  blocks: [
    // ---- literacy: RIMJHIM-1 "मेला" (letter → word → paragraph → story) ----
    {
      blockId: 'BLK-MELA-LET-01', chapterId: 'RIMJHIM-1-MELA', domain: 'literacy', level: 'letter', craStage: 'concrete',
      activity: 'अक्षर कार्ड: जो अक्षर सुनो वह कार्ड उठाओ',
      talkLine: 'जो अक्षर मैं बोलूँ, वह कार्ड उठाओ।',
      ncertRef: { book: 'Rimjhim-1', page: 13 }, cbseFln: 'FLN-L-1.1 Akshar identification',
    },
    {
      blockId: 'BLK-MELA-LET-02', chapterId: 'RIMJHIM-1-MELA', domain: 'literacy', level: 'letter', craStage: 'representational',
      activity: 'रेत की ट्रे में अक्षर लिखो, फिर बोलकर पढ़ो',
      talkLine: 'पहले उँगली से लिखो, फिर बोलकर पढ़ो।',
      ncertRef: { book: 'Rimjhim-1', page: 14 }, cbseFln: 'FLN-L-1.1 Akshar identification',
    },
    {
      blockId: 'BLK-MELA-WRD-01', chapterId: 'RIMJHIM-1-MELA', domain: 'literacy', level: 'word', craStage: 'concrete',
      activity: 'शब्द-चित्र मिलाओ: मेला, गुब्बारा, खिलौना',
      talkLine: 'शब्द पढ़ो और उसका चित्र चुनो।',
      ncertRef: { book: 'Rimjhim-1', page: 25 }, cbseFln: 'FLN-L-2.1 Blend akshars into words',
    },
    {
      blockId: 'BLK-MELA-WRD-02', chapterId: 'RIMJHIM-1-MELA', domain: 'literacy', level: 'word', craStage: 'representational',
      activity: 'मात्रा-समूह: मेला / माला / मिला कार्ड छाँटो',
      talkLine: 'तीनों शब्द पढ़ो — कौन सा मिलता है?',
      ncertRef: { book: 'Rimjhim-1', page: 26 }, cbseFln: 'FLN-L-2.1 Blend akshars into words',
    },
    {
      blockId: 'BLK-MELA-PAR-01', chapterId: 'RIMJHIM-1-MELA', domain: 'literacy', level: 'paragraph', craStage: 'representational',
      activity: 'पेज चुपचाप पढ़ो, फिर 2 सवाल कॉपी में लिखो',
      talkLine: 'पहले चुपचाप पढ़ो, फिर सवाल पढ़कर जवाब लिखो।',
      ncertRef: { book: 'Rimjhim-2', page: 11 }, cbseFln: 'FLN-L-3.1 Read a short paragraph',
    },
    {
      blockId: 'BLK-MELA-PAR-02', chapterId: 'RIMJHIM-1-MELA', domain: 'literacy', level: 'paragraph', craStage: 'abstract',
      activity: 'अपने शब्दों में मेले की 2 पंक्तियाँ लिखो',
      talkLine: 'तुम्हारे मेले में क्या हुआ? दो पंक्तियाँ लिखो।',
      ncertRef: { book: 'Rimjhim-2', page: 12 }, cbseFln: 'FLN-L-3.2 Fluency & expression',
    },
    {
      blockId: 'BLK-MELA-STO-01', chapterId: 'RIMJHIM-1-MELA', domain: 'literacy', level: 'story', craStage: 'abstract',
      activity: 'कहानी पढ़ो और शुरू-मध्य-अंत बताओ',
      talkLine: 'कहानी कैसे शुरू हुई? अंत में क्या हुआ?',
      ncertRef: { book: 'Rimjhim-2', page: 18 }, cbseFln: 'FLN-L-4.1 Read a story fluently',
    },
    // ---- numeracy: MATH-MAGIC-2 subtraction (C → R → A) ----
    {
      blockId: 'BLK-SUB-CON-01', chapterId: 'MATH-MAGIC-2-SUB', domain: 'numeracy', level: 'num_concrete', craStage: 'concrete',
      activity: 'पत्थर/ढक्कन से 9 में से 4 हटाओ, बचे हुए गिनो',
      talkLine: 'नौ चीज़ें रखो, चार हटाओ, अब गिनो।',
      ncertRef: { book: 'Math-Magic-1', page: 30 }, cbseFln: 'FLN-N-1.2 Take-away subtraction',
    },
    {
      blockId: 'BLK-SUB-REP-01', chapterId: 'MATH-MAGIC-2-SUB', domain: 'numeracy', level: 'num_representation', craStage: 'representational',
      activity: 'संख्या रेखा पर 15 − 7 कूदकर दिखाओ',
      talkLine: '15 से शुरू करो, 7 कदम पीछे जाओ।',
      ncertRef: { book: 'Math-Magic-2', page: 30 }, cbseFln: 'FLN-N-2.2 Composing to 10',
    },
    {
      blockId: 'BLK-SUB-ABS-01', chapterId: 'MATH-MAGIC-2-SUB', domain: 'numeracy', level: 'num_abstract', craStage: 'abstract',
      activity: 'दहाई के डंडे बाँटकर 52 − 37 हल करो',
      talkLine: '2 में से 7 नहीं जा सकता — एक दहाई बदलो।',
      ncertRef: { book: 'Math-Magic-2', page: 45 }, cbseFln: 'FLN-N-3.1 Subtraction with regrouping',
    },
  ],
  closers: [
    {
      blockId: 'CLS-MELA-01', chapterId: 'RIMJHIM-1-MELA', domain: 'literacy', audience: 'whole_class',
      activity: 'दो बच्चे अपना वाक्य ज़ोर से पढ़ें',
      talkLine: 'आज कौन अपना वाक्य पढ़ेगा?',
      ncertRef: { book: 'Rimjhim-1', page: 20 }, cbseFln: 'FLN-L-3.2 Fluency & expression',
    },
    {
      blockId: 'CLS-SUB-01', chapterId: 'MATH-MAGIC-2-SUB', domain: 'numeracy', audience: 'whole_class',
      activity: 'एक उदाहरण बोर्ड पर हल करो, बच्चे चेक करें',
      talkLine: 'बोर्ड देखो — क्या जवाब सही है?',
      ncertRef: { book: 'Math-Magic-2', page: 45 }, cbseFln: 'FLN-N-3.1 Subtraction with regrouping',
    },
  ],
};
