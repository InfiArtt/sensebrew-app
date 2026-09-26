// Text that is only for the eyes.
//
// Use it for the visible text inside any control that already carries an
// accessibilityLabel. Screen readers disagree about such controls: TalkBack
// reads the label and ignores the text inside it, but Jieshuo reads the label
// *and then* the text inside it, so every button came out twice ("Simpan,
// Simpan") — found in QA on the settings screen. Hiding the inner text makes the
// label the only thing either reader can find.
//
// scripts/check-a11y.js fails the build if a labelled control contains a plain
// <Text>, so this cannot quietly come back.
import { Text, TextProps } from 'react-native';

export default function VisualText(props: TextProps) {
  return (
    <Text
      {...props}
      accessible={false}
      accessibilityElementsHidden
      importantForAccessibility="no-hide-descendants"
    />
  );
}
