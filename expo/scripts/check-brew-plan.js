// Cross-checks the ported brewing arithmetic and data tables against values
// worked out by hand from lib/ in the Flutter build.
//
// These are the numbers a blind user pours to, so a silent drift here is worse
// than a crash. The project has no test runner yet; this script compiles the
// pure core modules (no React Native imports) and asserts against them.
//
// Run: npm run check

const { execFileSync } = require('child_process');
const crypto = require('crypto');
const fs = require('fs');
const os = require('os');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const CORE = [
  'src/core/brewPlan.ts',
  'src/core/recipe.ts',
  'src/core/appStrings.ts',
  'src/core/generatedStrings.ts',
  'src/core/recipeDatabase.ts',
  'src/core/grinderDatabase.ts',
  'src/core/aiService.ts',
  'src/core/audio/clickTrack.ts',
];

// SHA-256 of assets/audio/click_60bpm.wav as it shipped and was verified in the
// 39 MB build, before the track moved to on-device generation. The generator
// must keep reproducing these exact bytes: this is the metronome a blind user
// pours to, so "sounds about right" is not good enough.
const KNOWN_GOOD_TRACK_SHA256 =
  '16cf1ab5c3206acd11e6bdb2bbed606b002d027f46c664eabc8596dafff3d7fd';
const KNOWN_GOOD_TRACK_BYTES = 5380244;

function compileCore() {
  const outDir = fs.mkdtempSync(path.join(os.tmpdir(), 'sensebrew-check-'));
  // Run tsc's own entry point through node rather than through npx, which needs
  // a shell on Windows.
  execFileSync(
    process.execPath,
    [
      path.join(ROOT, 'node_modules', 'typescript', 'bin', 'tsc'),
      '--ignoreConfig',
      ...CORE,
      '--outDir',
      outDir,
      '--module',
      'commonjs',
      '--target',
      'es2020',
      '--esModuleInterop',
      '--skipLibCheck',
    ],
    { cwd: ROOT, stdio: 'inherit' }
  );
  return outDir;
}

let failures = 0;

function eq(label, actual, expected) {
  const a = JSON.stringify(actual);
  const e = JSON.stringify(expected);
  const ok = a === e;
  if (!ok) failures += 1;
  console.log(`${ok ? 'PASS' : 'FAIL'}  ${label}`);
  if (!ok) console.log(`        expected ${e}\n        actual   ${a}`);
}

function main() {
  const outDir = compileCore();
  const plan = require(path.join(outDir, 'brewPlan.js'));
  const { recipeDatabase, formatClock, trimNumber } = require(path.join(outDir, 'recipe.js'));
  const { str } = require(path.join(outDir, 'appStrings.js'));
  const { grinderDatabase, getGrindCategoryName } = require(
    path.join(outDir, 'grinderDatabase.js')
  );
  const { parseI18n } = require(path.join(outDir, 'aiService.js'));
  const clickTrack = require(path.join(outDir, 'audio', 'clickTrack.js'));

  console.log('\n=== database ===');
  eq('recipe count', recipeDatabase.length, 58);
  eq('total phases', recipeDatabase.reduce((n, r) => n + r.phases.length, 0), 230);

  const hoffmann = recipeDatabase.find((r) => r.name === 'James Hoffmann Ultimate V60');
  eq('hoffmann dose/water', [hoffmann.coffeeGrams, hoffmann.totalWaterMl], [15, 250]);
  eq(
    'hoffmann phase starts',
    hoffmann.phases.map((p) => p.startTimeSeconds),
    [0, 10, 15, 45, 75, 105, 110]
  );
  eq(
    'hoffmann phase actions',
    hoffmann.phases.map((p) => p.action),
    ['pourCenter', 'swirl', 'wait', 'pourCircle', 'pourCircle', 'swirl', 'wait']
  );
  eq('constructor default applied (beanType)', hoffmann.beanType, 'Arabica');
  eq('constructor default applied (isFavorite)', hoffmann.isFavorite, false);
  eq('isBuiltIn carried from seed', hoffmann.isBuiltIn, true);

  // This name contains parentheses, which a regex-based Dart-to-TS conversion
  // would have unbalanced.
  const phin = recipeDatabase.find((r) => r.name === 'Phin Coconut (Bac Xiu)');
  eq('name with parentheses survived conversion', phin !== undefined, true);
  eq('phin beanType override', phin.beanType, 'Robusta');
  eq('phin extraIngredients key', phin.extraIngredients, 'extra_key_15');

  console.log('\n=== buildDynamicRecipe: fast pourer, nothing to move (10 ml/s) ===');
  const fast = plan.buildDynamicRecipe(hoffmann, 10);
  eq('phase starts unchanged', fast.phases.map((p) => p.startTimeSeconds), [0, 10, 15, 45, 75, 105, 110]);
  eq('duration unchanged', fast.totalDurationSeconds, 210);

  console.log('\n=== buildDynamicRecipe: slow pourer, phases pushed apart (2 ml/s) ===');
  const slow = plan.buildDynamicRecipe(hoffmann, 2);
  eq('phase starts shifted', slow.phases.map((p) => p.startTimeSeconds), [0, 26, 31, 61, 112, 163, 168]);
  eq('duration extended by the total shift', slow.totalDurationSeconds, 268);

  console.log('\n=== pour duration ===');
  eq('50 ml at 10 ml/s', plan.pourDuration({ pourAmountMl: 50 }, 10), 5);
  eq('100 ml at 7.5 ml/s rounds to 13', plan.pourDuration({ pourAmountMl: 100 }, 7.5), 13);

  console.log('\n=== rotation wording ===');
  eq('whole rotations (id)', plan.rotationsValueText(50, 2, 'id'), '25');
  eq('half rotations spelled out (id)', plan.rotationsValueText(5, 2, 'id'), '2 setengah');
  eq('half rotations spelled out (en)', plan.rotationsValueText(5, 2, 'en'), '2 and a half');
  eq('with unit (id)', plan.rotationsText(5, 2, 'id'), '2 setengah putaran');
  eq('with unit (en)', plan.rotationsText(5, 2, 'en'), '2 and a half rotations');
  eq('rounds to the nearest half', plan.rotationsValueText(7, 2, 'id'), '3 setengah');
  eq('13 / 2 = 6.5', plan.rotationsValueText(13, 2, 'id'), '6 setengah');

  console.log('\n=== spoken cues ===');
  const circle = { action: 'pourCircle', pourAmountMl: 100, startTimeSeconds: 45 };
  const center = { action: 'pourCenter', pourAmountMl: 50, startTimeSeconds: 0 };
  const id = { lang: 'id', mlPerSecond: 10, secondsPerRotation: 2 };
  const en = { lang: 'en', mlPerSecond: 10, secondsPerRotation: 2 };

  eq('opening cue, circle', plan.openingCue({ phase: circle, ...id }), 'Siap-siap, tuang 5 putaran.');
  eq('prepare cue, circle', plan.prepareCue({ phase: circle, ...id }), 'Siap, tuang 5 putaran.');
  eq('continuation cue, circle', plan.continuationCue({ phase: circle, ...id }), 'Lanjut tuang 5 putaran.');
  eq('opening cue, centre', plan.openingCue({ phase: center, ...id }), 'Siap-siap, tuang tengah 5 detik.');
  eq('prepare cue, centre (en)', plan.prepareCue({ phase: center, ...en }), 'Prepare for center pour, 5 seconds.');

  console.log('\n=== on-screen text ===');
  eq('active pour, circle', plan.activePhaseText({ phase: circle, ...id }), 'Tuang 100 mili, 5 putaran.');
  eq('active pour, centre', plan.activePhaseText({ phase: center, ...id }), 'Tuang di tengah 50 mili selama 5 detik.');
  eq('phase row, circle', plan.phaseListText({ phase: circle, ...id }), 'Tuang 100 ml (5 putaran)');
  eq('phase row, centre (en)', plan.phaseListText({ phase: center, ...en }), 'Center pour 50 ml (5 sec)');
  eq('phase row, wait', plan.phaseListText({ phase: { action: 'wait', pourAmountMl: 0 }, ...id }), 'Tunggu...');

  console.log('\n=== active phase index ===');
  eq('during the 4-second lead-in', plan.activePhaseIndex(fast.phases, -4), -1);
  eq('at second 0', plan.activePhaseIndex(fast.phases, 0), 0);
  eq('at second 44, still waiting', plan.activePhaseIndex(fast.phases, 44), 2);
  eq('at second 45, the pour starts', plan.activePhaseIndex(fast.phases, 45), 3);
  eq('past the last phase', plan.activePhaseIndex(fast.phases, 999), 6);

  console.log('\n=== strings and formatting ===');
  eq(
    'placeholder substitution (id)',
    str('id', 'recipe_label', ['Kalita', '15', '250']),
    'Resep Kalita. 15 gram kopi. 250 mililiter air.'
  );
  eq(
    'english table used',
    str('en', 'recipe_label', ['Kalita', '15', '250']),
    'Kalita recipe. 15 grams of coffee. 250 milliliters of water.'
  );
  eq('unknown key returns itself', str('id', 'James Hoffmann Ultimate V60'), 'James Hoffmann Ultimate V60');
  eq('brew_sec is two lines', str('id', 'brew_sec', ['12', 'Tunggu...']), 'Detik: 12\nTunggu...');
  eq('clock format', [formatClock(0), formatClock(45), formatClock(110), formatClock(605)], ['00:00', '00:45', '01:50', '10:05']);
  eq('trailing .0 dropped', [trimNumber(15), trimNumber(12.5), trimNumber(20.0)], ['15', '12.5', '20']);

  console.log('\n=== grinders ===');
  eq('grinder count', grinderDatabase.length, 20);
  eq('default grinder present', grinderDatabase.some((g) => g.id === 'timemore_c2'), true);
  eq('timemore at 800 microns', grinderDatabase.find((g) => g.id === 'timemore_c2').getSetting(800), '15 - 18 ');
  eq('ek43 at 1400 microns', grinderDatabase.find((g) => g.id === 'mahlkonig_ek43').getSetting(1400), '15.0 - 16.0');
  eq('grind category is translated, not a raw key', getGrindCategoryName(800, 'id') !== 'custom_grind_800', true);

  console.log('');
  console.log('=== bilingual payloads from the assistant ===');
  eq('object becomes a payload', parseI18n({ id: 'Tuang', en: 'Pour' }), 'ID: Tuang || EN: Pour');
  eq('plain string is duplicated', parseI18n('Tuang'), 'ID: Tuang || EN: Tuang');
  eq('existing payload untouched', parseI18n('ID: a || EN: b'), 'ID: a || EN: b');
  eq('empty object is empty', parseI18n({ id: '', en: '' }), '');
  eq('null is empty', parseI18n(null), '');
  eq('payload reads back as id', str('id', parseI18n({ id: 'Tuang', en: 'Pour' })), 'Tuang');
  eq('payload reads back as en', str('en', parseI18n({ id: 'Tuang', en: 'Pour' })), 'Pour');

  console.log('');
  console.log('=== hand-written strings merged over the generated table ===');
  [
    'audio_metronome_title',
    'visual_metronome_desc',
    'haptic_metronome_title',
    'groq_network_warning',
    'groq_api_key_label',
    'tts_voice_none',
    'tts_voice_sample',
    'preview_voice',
    'pour_calc_uncalibrated',
    'selected_suffix',
  ].forEach((key) => {
    eq(`${key} in both languages`, [str('id', key) !== key, str('en', key) !== key], [true, true]);
  });
  eq('id and en actually differ', str('id', 'audio_metronome_title') !== str('en', 'audio_metronome_title'), true);

  console.log('');
  console.log('=== keys the ported screens look up ===');
  [
    'action_pour_circle', 'action_pour_center', 'action_wait', 'action_stir',
    'action_swirl', 'action_cap', 'action_flip', 'action_press',
    'action_openValve', 'action_closeValve',
    'custom_grind_400', 'custom_grind_600', 'custom_grind_800',
    'custom_grind_1000', 'custom_grind_1200', 'custom_grind_1400',
    'custom_bean_blend', 'custom_bean_bebas', 'custom_bean_custom',
    'save_overwrite', 'save_as_new', 'save_recipe', 'save_recipe_success',
    'add_phase', 'delete_phase', 'phases_title', 'start_sec', 'water_ml',
    'coffee_grams', 'total_water', 'total_time', 'recipe_name',
    'custom_recipe_desc', 'custom_title',
    'ai_greet_new', 'ai_greet_edit', 'ai_hint', 'ai_send_label',
    'ai_record_start_label', 'ai_record_stop_label', 'ai_apply_btn',
    'ai_voice_note', 'ai_error_general', 'ai_error_no_key', 'ai_generating',
    'ai_coffee', 'ai_water', 'ai_time', 'ai_title', 'ai_chat_title',
    'pour_calc_title', 'pour_calc_desc', 'pour_calc_target', 'pour_calc_est',
    'pour_calc_start', 'pour_calc_ready', 'pour_calc_stop',
    'settings_title', 'app_lang', 'app_lang_desc', 'app_lang_label',
    'gemini_title', 'gemini_desc', 'gemini_api_key_label', 'gemini_help_title',
    'gemini_help_content', 'show_api_key', 'tts_title', 'tts_enable',
    'tts_enable_desc', 'tts_channel', 'tts_channel_desc', 'tts_channel_app',
    'tts_channel_sr', 'tts_channel_changed', 'tts_speed', 'tts_speed_changed',
    'tts_pitch', 'tts_pitch_changed', 'tts_voice', 'tts_voice_desc',
    'tts_voice_changed', 'default', 'close', 'restore_success',
    'settings_restore_title', 'settings_restore_sub', 'stop_metronome',
    'reduce', 'add', 'calib_header', 'calib_guide', 'calib_sim_btn',
    'calib_grinder_select', 'calib_grinder_title', 'calib_grinder_manual',
    'calib_grinder_electric', 'calib_spoon_q', 'calib_q1', 'calib_q2',
    'calib_q3', 'save_calib_label', 'save_success',
  ].forEach((key) => {
    const idOk = str('id', key) !== key;
    const enOk = str('en', key) !== key;
    if (!idOk || !enOk) eq(`${key} resolves in both languages`, [idOk, enOk], [true, true]);
  });
  console.log('PASS  every screen key resolves in both languages');

  console.log('');
  console.log('=== click track generated on the device ===');
  const tickWav = new Uint8Array(
    fs.readFileSync(path.join(ROOT, 'assets', 'audio', 'tick.wav'))
  );

  const tick = clickTrack.readWavPcm(tickWav);
  eq('tick sample rate', tick.sampleRate, 44100);
  eq('tick is mono 16-bit', [tick.channels, tick.bitsPerSample], [1, 16]);
  eq('tick lead-in silence, in samples', clickTrack.findAttack(tick.samples), 2660);

  const built = clickTrack.buildClickTrack(tickWav);
  eq('total bytes', built.wav.length, KNOWN_GOOD_TRACK_BYTES);
  eq('trimmed the lead-in', built.trimmedSamples, 2660);

  const sha = crypto.createHash('sha256').update(built.wav).digest('hex');
  eq('byte-identical to the verified 5.1 MB asset', sha, KNOWN_GOOD_TRACK_SHA256);

  // Header, read back independently of the writer.
  const parsed = clickTrack.readWavPcm(built.wav);
  eq(
    'header says 44100 Hz mono 16-bit',
    [parsed.sampleRate, parsed.channels, parsed.bitsPerSample],
    [44100, 1, 16]
  );
  eq(
    'duration is beats + 1 seconds',
    parsed.samples.length / 2 / parsed.sampleRate,
    clickTrack.CLICK_TRACK_BEATS + 1
  );

  // The whole design rests on this: every click must attack on an exact second.
  const view = new DataView(
    parsed.samples.buffer,
    parsed.samples.byteOffset,
    parsed.samples.byteLength
  );
  const attackAtOrAfter = (startSample) => {
    for (let i = Math.max(0, startSample) * 2; i + 1 < parsed.samples.length; i += 2) {
      if (Math.abs(view.getInt16(i, true)) > 100) return i / 2;
    }
    return -1;
  };

  const offBeat = [];
  for (let beat = 1; beat <= clickTrack.CLICK_TRACK_BEATS; beat++) {
    const expected = clickTrack.expectedAttackSample(beat, parsed.sampleRate);
    const actual = attackAtOrAfter(expected - parsed.sampleRate / 2);
    if (actual !== expected) offBeat.push({ beat, expected, actual });
  }
  eq(`all ${clickTrack.CLICK_TRACK_BEATS} clicks attack on an exact second`, offBeat, []);
  eq('the first second is silent', attackAtOrAfter(0), parsed.sampleRate);

  fs.rmSync(outDir, { recursive: true, force: true });

  console.log(`\n${failures === 0 ? 'ALL CHECKS PASSED' : `${failures} CHECK(S) FAILED`}`);
  process.exit(failures === 0 ? 0 : 1);
}

main();
