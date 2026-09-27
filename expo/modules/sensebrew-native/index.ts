// The app's own native code. See android/.../NativeTextFieldView.kt.
//
// Expo Go cannot load it, so everything here is optional: callers get null and
// fall back to React Native's own components.
import { requireNativeView, requireOptionalNativeModule } from 'expo';
import type { ComponentType } from 'react';
import { Platform, type NativeSyntheticEvent, type ViewProps } from 'react-native';

export type NativeTextFieldProps = ViewProps & {
  value: string;
  /** The last onChangeText eventCount JS has seen; see NativeTextFieldView. */
  mostRecentEventCount: number;
  hint: string;
  keyboard: 'text' | 'number' | 'decimal' | 'password';
  secure: boolean;
  multiline: boolean;
  editable: boolean;
  returnKey: 'done' | 'send';
  textAlign: 'left' | 'center';
  fontSize: number;
  /** #RRGGBB */
  textColor: string;
  /** #RRGGBB */
  hintColor: string;
  onChangeText: (event: NativeSyntheticEvent<{ text: string; eventCount: number }>) => void;
  onSubmit: (event: NativeSyntheticEvent<{ text: string }>) => void;
  onFocusChange: (event: NativeSyntheticEvent<{ focused: boolean }>) => void;
};

const isAvailable =
  Platform.OS === 'android' && requireOptionalNativeModule('SensebrewNative') != null;

/** The native EditText, or null where this app's native code is not built in. */
export const NativeTextField: ComponentType<NativeTextFieldProps> | null = isAvailable
  ? requireNativeView<NativeTextFieldProps>('SensebrewNative')
  : null;
