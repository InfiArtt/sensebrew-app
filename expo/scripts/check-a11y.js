// Fails when a screen reader would read the same control twice.
//
// TalkBack and Jieshuo disagree about a control that has an accessibilityLabel
// and also contains visible text: TalkBack reads the label only, Jieshuo reads
// the label and then the text inside it. QA heard every such control twice on
// Jieshuo ("Simpan, Simpan"). The rule this enforces:
//
//   * A <Pressable> or <View> that sets accessibilityLabel must not contain a
//     plain <Text>. Use components/VisualText for the visible text instead.
//   * A <Text> must not set accessibilityLabel. Its content is its name; if the
//     spoken form has to differ, make it a labelled <View> around VisualText.
//   * A readable caption must not repeat the name of the control right after it.
//     QA heard "Berapa ml...?" from the heading and again from the field's
//     hint. Hide the caption from the screen reader instead; the control says it.
//   * Screens use components/TextField, never <TextInput> directly: React
//     Native's EditText cannot take input focus from a screen reader, so the
//     cursor actions ("go to start", "go to end") did nothing on it.
//
// Run: npm run check (this runs after the brewing checks)

const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');

function sourceFiles() {
  const out = [path.join(ROOT, 'App.tsx')];
  const walk = (dir) => {
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      const full = path.join(dir, entry.name);
      if (entry.isDirectory()) walk(full);
      else if (entry.name.endsWith('.tsx')) out.push(full);
    }
  };
  walk(path.join(ROOT, 'src'));
  return out;
}

/** Index of the '>' ending the JSX opening tag that starts at `start`. */
function tagEnd(text, start) {
  let depth = 0;
  for (let i = start; i < text.length; i++) {
    const c = text[i];
    if (c === '{') depth++;
    else if (c === '}') depth--;
    else if (c === '>' && depth === 0) return i;
  }
  return -1;
}

/** Offsets of every opening tag named `name` (not a longer name like TextInput). */
function openings(text, name) {
  const re = new RegExp(`<${name}(?![A-Za-z0-9_])`, 'g');
  const found = [];
  let m;
  while ((m = re.exec(text))) found.push(m.index);
  return found;
}

/** End offset of the element whose opening tag starts at `start`, or -1. */
function elementEnd(text, name, start) {
  const firstEnd = tagEnd(text, start);
  if (firstEnd === -1) return -1;
  if (text[firstEnd - 1] === '/') return firstEnd + 1; // self-closing

  const tokens = new RegExp(`<${name}(?![A-Za-z0-9_])|</${name}>`, 'g');
  tokens.lastIndex = firstEnd + 1;
  let level = 1;
  let m;
  while ((m = tokens.exec(text))) {
    if (m[0].startsWith('</')) {
      level--;
      if (level === 0) return m.index + m[0].length;
    } else {
      const end = tagEnd(text, m.index);
      if (end !== -1 && text[end - 1] !== '/') level++;
    }
  }
  return -1;
}

const lineOf = (text, offset) => text.slice(0, offset).split('\n').length;

function audit() {
  const problems = [];

  for (const file of sourceFiles()) {
    const text = fs.readFileSync(file, 'utf8');
    const rel = path.relative(ROOT, file);

    for (const container of ['Pressable', 'View']) {
      for (const start of openings(text, container)) {
        const end = tagEnd(text, start);
        const tag = text.slice(start, end + 1);
        if (!/\baccessibilityLabel=/.test(tag) || tag.endsWith('/>')) continue;

        const close = elementEnd(text, container, start);
        const body = text.slice(end + 1, close);
        for (const inner of openings(body, 'Text')) {
          problems.push(
            `${rel}:${lineOf(text, end + 1 + inner)}  plain <Text> inside a labelled <${container}> ` +
              `(line ${lineOf(text, start)}) — use VisualText`
          );
        }
      }
    }

    for (const start of openings(text, 'Text')) {
      const end = tagEnd(text, start);
      const tag = text.slice(start, end + 1);
      if (/\baccessibilityLabel=/.test(tag)) {
        problems.push(`${rel}:${lineOf(text, start)}  <Text> with its own accessibilityLabel`);
      }

      const repeated = repeatedCaption(text, start, end, tag);
      if (repeated) {
        problems.push(
          `${rel}:${lineOf(text, start)}  caption '${repeated.key}' is read, then again by the ` +
            `<${repeated.control}> after it — hide the caption from the screen reader`
        );
      }
    }

    if (!rel.endsWith(path.join('components', 'TextField.tsx'))) {
      for (const start of openings(text, 'TextInput')) {
        if (inComment(text, start)) continue;
        problems.push(`${rel}:${lineOf(text, start)}  <TextInput> — use components/TextField`);
      }
    }
  }

  return problems;
}

/**
 * For a readable <Text>{str(lang, 'key')}</Text>, the next control if it is
 * named with the same key: { key, control }. Otherwise null.
 */
function repeatedCaption(text, start, end, tag) {
  if (tag.endsWith('/>') || /accessibilityElementsHidden|no-hide-descendants/.test(tag)) return null;

  const close = elementEnd(text, 'Text', start);
  const body = text.slice(end + 1, close - '</Text>'.length);
  const caption = /^\s*\{str\(lang, '([^']+)'\)\}\s*$/.exec(body);
  if (!caption) return null;
  const key = caption[1];

  // The next element, skipping whitespace and {/* comments */}, and every named
  // control in it: the element itself, or those inside a layout wrapper such as
  // the minus / field / plus row, where the field repeated the heading.
  const rest = text.slice(close).replace(/^(\s|\{\/\*[\s\S]*?\*\/\})*/, '');
  const next = /^<([A-Z][A-Za-z0-9_]*)/.exec(rest);
  if (!next) return null;
  const nextEnd = elementEnd(rest, next[1], 0);
  const element = nextEnd === -1 ? rest.slice(0, tagEnd(rest, 0) + 1) : rest.slice(0, nextEnd);

  const tags = /<([A-Z][A-Za-z0-9_]*)/g;
  let m;
  while ((m = tags.exec(element))) {
    const controlTag = element.slice(m.index, tagEnd(element, m.index) + 1);
    const isNamed = /\b(accessibilityLabel|hint|label|question|placeholder)=/.test(controlTag);
    if (isNamed && controlTag.includes(`'${key}'`)) return { key, control: m[1] };
  }
  return null;
}

/** Whether the offset sits on a // or /* comment line. */
function inComment(text, offset) {
  const lineStart = text.lastIndexOf('\n', offset) + 1;
  return /^\s*(\/\/|\/?\*)/.test(text.slice(lineStart, offset));
}

const problems = audit();
console.log('');
console.log('=== screen reader: nothing read twice ===');
if (problems.length === 0) {
  console.log('PASS  no labelled control exposes its visible text');
  console.log('PASS  no caption repeats the control after it');
  console.log('PASS  every text field is components/TextField');
} else {
  for (const p of problems) console.log(`FAIL  ${p}`);
  console.log(`\n${problems.length} screen-reader problem(s)`);
  process.exit(1);
}
