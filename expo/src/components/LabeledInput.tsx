// A labelled text field.
//
// Two requirements, both from QA:
//
//   1. One swipe stop per field. The label belongs to the field, so five fields
//      are five swipes, not ten.
//   2. The field stays a plain EditText, so the screen reader offers its editing
//      actions on it (select all, paste, move to start/end...) the way it does on
//      WhatsApp's message box. That is what components/TextField provides.
//
// The label therefore goes in the field's *hint*, and the visible caption is
// hidden from the screen reader. That is exactly what the Flutter build's
// NativeTextFieldView.kt did — "Only use hint for EditText to avoid confusing
// TalkBack with double descriptions" — with the caption wrapped in
// ExcludeSemantics on the Dart side.
//
// Two approaches that were tried here first and must not come back:
//
//   * `accessibilityLabel` on the field. On Android that becomes the
//     EditText's contentDescription, and a contentDescription makes the screen
//     reader read that string instead of treating the view as editable text: the
//     editing actions disappear (breaks requirement 2).
//   * `accessibilityLabelledBy` pointing at a visible caption (Android labelFor).
//     labelFor links the caption to the field but does not merge them, so the
//     caption stays a stop of its own (breaks requirement 1).
import { useState } from 'react';
import { Pressable, StyleSheet, Text, View, type KeyboardTypeOptions } from 'react-native';

import Icon from './Icon';
import TextField from './TextField';

import { colors } from '../theme';

interface Props {
  label: string;
  value: string;
  onChangeText: (value: string) => void;
  keyboardType?: Extract<KeyboardTypeOptions, 'default' | 'number-pad' | 'decimal-pad'>;
  /** Renders as a password field with a reveal toggle. */
  secret?: boolean;
  /** Name for the reveal toggle while the value is hidden ("show API key"). */
  revealLabel?: string;
  /** Name for the same toggle once the value is showing ("hide API key"). */
  hideLabel?: string;
  multiline?: boolean;
  onSubmitEditing?: () => void;
  placeholder?: string;
}

export default function LabeledInput({
  label,
  value,
  onChangeText,
  keyboardType,
  secret = false,
  revealLabel,
  hideLabel,
  multiline = false,
  onSubmitEditing,
  placeholder,
}: Props) {
  const [revealed, setRevealed] = useState(false);

  return (
    <View style={styles.wrapper}>
      {/* For sighted users only; the field carries the same text as its hint. */}
      <Text
        accessibilityElementsHidden
        importantForAccessibility="no-hide-descendants"
        style={styles.caption}
      >
        {label}
      </Text>

      <View style={styles.fieldRow}>
        <TextField
          hint={placeholder ?? label}
          value={value}
          onChangeText={onChangeText}
          keyboardType={keyboardType}
          secret={secret}
          revealed={revealed}
          multiline={multiline}
          onSubmitEditing={onSubmitEditing}
          style={styles.input}
        />

        {secret && (
          <Pressable
            accessibilityRole="button"
            // The name has to follow the state, or the button still says "show"
            // after it has switched to hiding.
            accessibilityLabel={revealed ? (hideLabel ?? label) : (revealLabel ?? label)}
            onPress={() => setRevealed((r) => !r)}
            hitSlop={8}
            style={({ pressed }) => [styles.revealButton, pressed && styles.pressed]}
          >
            <Icon
              name={revealed ? 'visibility-off' : 'visibility'}
              size={24}
              color={colors.primary}
            />
          </Pressable>
        )}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  wrapper: {
    marginBottom: 16,
  },
  caption: {
    fontSize: 14,
    fontWeight: 'bold',
    color: colors.text,
    marginBottom: 6,
  },
  fieldRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
  },
  input: {
    flex: 1,
    backgroundColor: colors.card,
    borderWidth: 1,
    borderColor: colors.divider,
    borderRadius: 4,
  },
  revealButton: {
    width: 48,
    height: 48,
    alignItems: 'center',
    justifyContent: 'center',
  },
  pressed: {
    opacity: 0.75,
  },
});
