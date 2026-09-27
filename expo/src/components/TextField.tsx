// The one text field every screen uses.
//
// In the APK this is a plain Android EditText from modules/sensebrew-native,
// because React Native's own TextInput cannot take input focus from a screen
// reader: ReactEditText is not focusable in touch mode, so TalkBack and
// Jieshuo's cursor actions ("go to start", "go to end", selection) did nothing
// on it, while they work on every other app's fields. See
// NativeTextFieldView.kt for the details.
//
// Expo Go cannot load the app's own native code, so there it falls back to
// TextInput. Everything still works in Expo Go except those cursor actions;
// test screen-reader editing on the APK.
//
// The field is named by its hint and never by accessibilityLabel: on Android
// that becomes the EditText's contentDescription, and a contentDescription
// makes the screen reader treat the field as a label instead of editable text.
// scripts/check-a11y.js keeps screens from using TextInput directly.
import { useRef } from 'react';
import {
  TextInput,
  View,
  type KeyboardTypeOptions,
  type StyleProp,
  type ViewStyle,
} from 'react-native';

import { NativeTextField } from '../../modules/sensebrew-native';
import { colors, fontSize as fontSizes } from '../theme';

interface Props {
  value: string;
  onChangeText: (value: string) => void;
  /** The field's name for the screen reader, and the placeholder on screen. */
  hint: string;
  keyboardType?: Extract<KeyboardTypeOptions, 'default' | 'number-pad' | 'decimal-pad'>;
  /** A password-style field; `revealed` shows the characters. */
  secret?: boolean;
  revealed?: boolean;
  multiline?: boolean;
  editable?: boolean;
  /**
   * Select the whole value on focus, so typing replaces it. Use this instead of
   * clearing the field on focus: an emptied field is announced by its hint
   * alone, and the user never hears the value they came to change.
   */
  selectAllOnFocus?: boolean;
  returnKey?: 'done' | 'send';
  onSubmitEditing?: () => void;
  onFocus?: () => void;
  onBlur?: () => void;
  fontSize?: number;
  textAlign?: 'left' | 'center';
  /** The box: size, margins, border and fill. Text styling is via props. */
  style?: StyleProp<ViewStyle>;
}

export default function TextField({
  value,
  onChangeText,
  hint,
  keyboardType = 'default',
  secret = false,
  revealed = false,
  multiline = false,
  editable = true,
  selectAllOnFocus = false,
  returnKey = 'done',
  onSubmitEditing,
  onFocus,
  onBlur,
  fontSize = fontSizes.body,
  textAlign = 'left',
  style,
}: Props) {
  // The last change the native field reported. It goes back with every render
  // so the field knows whether `value` already includes the user's latest
  // keystroke; see NativeTextFieldView.applyProps.
  const eventCount = useRef(0);

  // A native view has no text of its own for Yoga to measure, so the box gets a
  // height that fits one line of this font size (or a few, for multiline).
  const minHeight = multiline ? 96 : Math.max(52, Math.round(fontSize * 1.4 + 20));

  if (NativeTextField) {
    return (
      <View style={[{ minHeight }, style]}>
        <NativeTextField
          style={{ flex: 1 }}
          value={value}
          mostRecentEventCount={eventCount.current}
          hint={hint}
          keyboard={
            secret
              ? 'password'
              : keyboardType === 'number-pad'
                ? 'number'
                : keyboardType === 'decimal-pad'
                  ? 'decimal'
                  : 'text'
          }
          secure={secret && !revealed}
          multiline={multiline}
          editable={editable}
          selectAllOnFocus={selectAllOnFocus}
          returnKey={returnKey}
          textAlign={textAlign}
          fontSize={fontSize}
          textColor={colors.text}
          hintColor={colors.textDisabled}
          onChangeText={(e) => {
            eventCount.current = e.nativeEvent.eventCount;
            onChangeText(e.nativeEvent.text);
          }}
          onSubmit={() => onSubmitEditing?.()}
          onFocusChange={(e) => (e.nativeEvent.focused ? onFocus?.() : onBlur?.())}
        />
      </View>
    );
  }

  return (
    <TextInput
      placeholder={hint}
      placeholderTextColor={colors.textDisabled}
      value={value}
      onChangeText={onChangeText}
      keyboardType={keyboardType}
      secureTextEntry={secret && !revealed}
      multiline={multiline}
      editable={editable}
      selectTextOnFocus={selectAllOnFocus}
      returnKeyType={returnKey}
      onSubmitEditing={onSubmitEditing}
      onFocus={onFocus}
      onBlur={onBlur}
      style={[
        {
          minHeight,
          fontSize,
          textAlign,
          color: colors.text,
          paddingHorizontal: 12,
          paddingVertical: 8,
          textAlignVertical: multiline ? 'top' : 'center',
        },
        style,
      ]}
    />
  );
}
