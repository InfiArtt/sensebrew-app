// A bottom-sheet list picker, standing in for Flutter's
// showModalBottomSheet + DropdownButtonFormField.
//
// Both Flutter patterns are replaced by this one sheet on purpose: a list of
// plain buttons is navigable by swipe and states its own selection, whereas a
// dropdown is a single control whose options a screen reader only reaches after
// opening it.
import Icon from './Icon';
import { Modal, Pressable, ScrollView, StyleSheet, Text, View } from 'react-native';

import { colors, fontSize } from '../theme';

export interface SelectOption {
  value: string;
  label: string;
  /** Second line, e.g. "Manual" / "Electric" for grinders. */
  detail?: string;
}

interface Props {
  visible: boolean;
  title: string;
  options: SelectOption[];
  currentValue: string;
  onSelect: (value: string) => void;
  onClose: () => void;
  /** Shown as a separate play button per row, for voice previews. */
  onPreview?: (value: string) => void;
  previewLabel?: string;
  /** Announced on the selected row so the choice is audible, not just visual. */
  selectedSuffix: string;
}

export default function SelectSheet({
  visible,
  title,
  options,
  currentValue,
  onSelect,
  onClose,
  onPreview,
  previewLabel,
  selectedSuffix,
}: Props) {
  return (
    <Modal visible={visible} transparent animationType="slide" onRequestClose={onClose}>
      {/*
        The scrim is a tap-outside-to-dismiss convenience for sighted users. It is
        kept out of the accessibility tree: as a focusable element it is a
        full-screen control with nothing in it, and the sheet already closes via
        the back gesture.
      */}
      <Pressable
        style={styles.scrim}
        accessibilityElementsHidden
        importantForAccessibility="no-hide-descendants"
        onPress={onClose}
      />
      {/* Confines the screen reader to the sheet while it is open. */}
      <View accessibilityViewIsModal style={styles.sheet}>
        <Text accessibilityRole="header" style={styles.title}>
          {title}
        </Text>

        <ScrollView>
          {options.map((option) => {
            const selected = option.value === currentValue;
            const label = [option.label, option.detail, selected ? selectedSuffix : null]
              .filter(Boolean)
              .join('. ');

            return (
              <View key={option.value} style={styles.row}>
                <Pressable
                  accessible
                  // Not role="button": these are the choices in a list, and
                  // "button" on each one adds a word QA asked us to drop. The
                  // selected state is announced instead, which is the useful part.
                  accessibilityState={{ selected }}
                  accessibilityLabel={label}
                  onPress={() => onSelect(option.value)}
                  style={({ pressed }) => [styles.rowMain, pressed && styles.pressed]}
                >
                  <Text
                    importantForAccessibility="no-hide-descendants"
                    style={styles.rowLabel}
                  >
                    {option.label}
                  </Text>
                  {option.detail !== undefined && (
                    <Text
                      importantForAccessibility="no-hide-descendants"
                      style={styles.rowDetail}
                    >
                      {option.detail}
                    </Text>
                  )}
                </Pressable>

                {onPreview && previewLabel && (
                  <Pressable
                    accessibilityRole="button"
                    accessibilityLabel={`${previewLabel}. ${option.label}`}
                    onPress={() => onPreview(option.value)}
                    hitSlop={8}
                    style={({ pressed }) => [styles.iconButton, pressed && styles.pressed]}
                  >
                    <Icon name="play-circle-fill" size={28} color={colors.blue} />
                  </Pressable>
                )}

                {/*
                  Purely visual: the row itself already says "selected", so this
                  tick must not become a stop of its own.
                */}
                {selected && (
                  <View
                    accessibilityElementsHidden
                    importantForAccessibility="no-hide-descendants"
                    style={styles.iconButton}
                  >
                    <Icon name="check" size={26} color={colors.blue} />
                  </View>
                )}
              </View>
            );
          })}
        </ScrollView>
      </View>
    </Modal>
  );
}

const styles = StyleSheet.create({
  scrim: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
  },
  sheet: {
    maxHeight: '70%',
    backgroundColor: colors.card,
    borderTopLeftRadius: 8,
    borderTopRightRadius: 8,
    paddingBottom: 16,
  },
  title: {
    fontSize: fontSize.heading,
    fontWeight: 'bold',
    color: colors.text,
    padding: 16,
  },
  row: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  rowMain: {
    flex: 1,
    paddingVertical: 14,
    paddingHorizontal: 16,
  },
  rowLabel: {
    fontSize: fontSize.subheading,
    color: colors.text,
  },
  rowDetail: {
    fontSize: 14,
    color: colors.textSecondary,
    marginTop: 2,
  },
  iconButton: {
    width: 52,
    height: 52,
    alignItems: 'center',
    justifyContent: 'center',
  },
  pressed: {
    opacity: 0.75,
  },
});
