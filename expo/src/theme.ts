// The Flutter build uses ThemeData(primarySwatch: Colors.brown) with a few
// palette colours referenced directly in the screens. The hex values below are
// those exact Material colours so the Expo build looks the same rather than
// approximately the same.
export const colors = {
  primary: '#795548', // Colors.brown
  primaryDark: '#5D4037', // Colors.brown.shade700
  onPrimary: '#FFFFFF',

  background: '#FAFAFA', // default scaffoldBackgroundColor
  beatFlash: '#D7CCC8', // Colors.brown.shade100, the visual metronome

  text: '#000000',
  textSecondary: 'rgba(0, 0, 0, 0.54)', // Theme.textTheme.bodySmall
  textDisabled: '#9E9E9E', // Colors.grey

  blue: '#2196F3',
  blue50: '#E3F2FD',
  blue200: '#90CAF9',
  blueGrey: '#607D8B',

  red: '#F44336',
  green: '#4CAF50',
  teal: '#009688',
  amber: '#FFC107',
  yellow100: '#FFF9C4',

  purple50: '#F3E5F5',
  purple900: '#4A148C',

  card: '#FFFFFF',
  divider: '#E0E0E0',
};

export const fontSize = {
  timer: 120,
  phase: 32,
  button: 24,
  title: 24,
  heading: 20,
  subheading: 18,
  body: 16,
  clock: 22,
};

/**
 * Minimum touch target. The Flutter build leaned on Material's 48dp default;
 * stating it here keeps the ported buttons from shrinking below it, which
 * matters most for users who cannot aim precisely.
 */
export const MIN_TOUCH_SIZE = 48;
