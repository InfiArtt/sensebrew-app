// A decorative icon.
//
// Every icon in this app sits inside a control that already carries its own
// label, so no icon should ever be a screen-reader stop of its own. That is not
// the default: @expo/vector-icons renders a <Text> holding a glyph character, so
// Android happily focuses it and reads out nothing — the "kayak ada yang kosong"
// (feels like there's an empty one) that QA hit in the dropdown.
//
// Marking them here rather than at each of the ~30 call sites means a new icon
// cannot reintroduce the problem by being added without the prop.
import MaterialIcons from '@expo/vector-icons/MaterialIcons';

export type IconName = keyof typeof MaterialIcons.glyphMap;

interface Props {
  name: IconName;
  size: number;
  color: string;
}

export default function Icon({ name, size, color }: Props) {
  return (
    <MaterialIcons
      name={name}
      size={size}
      color={color}
      accessibilityElementsHidden
      importantForAccessibility="no-hide-descendants"
    />
  );
}
