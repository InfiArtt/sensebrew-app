// Ported from lib/screens/custom_recipe_screen.dart.
//
// Two differences from the Dart, both fixing issues listed in
// MIGRATION_HANDOVER.md:
//
//   * The brewing method arrives as a required route param rather than an
//     optional constructor argument, so a recipe started from the Cupping list
//     can no longer be saved as a V60 one (issue 3).
//   * Saving writes to the recipe store here instead of returning a value
//     through the navigator, because React Navigation has no equivalent of
//     `Navigator.pop(context, result)` — and that removes the step where the
//     method used to get reattached by the caller.
import Icon from '../components/Icon';
import VisualText from '../components/VisualText';
import type { NativeStackScreenProps } from '@react-navigation/native-stack';
import { useFocusEffect } from '@react-navigation/native';
import { useCallback, useLayoutEffect, useState } from 'react';
import {
  AccessibilityInfo,
  Platform,
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  ToastAndroid,
  View,
} from 'react-native';

import LabeledInput from '../components/LabeledInput';
import SelectSheet, { SelectOption } from '../components/SelectSheet';
import { str } from '../core/appStrings';
import {
  PHASE_ACTIONS,
  PhaseAction,
  Recipe,
  RecipePhase,
  makeRecipe,
  newRecipeId,
} from '../core/recipe';
import { useAiDraft } from '../core/stores/aiDraftStore';
import { useRecipes } from '../core/stores/recipeStore';
import { useSettings } from '../core/stores/settingsStore';
import type { RootStackParamList } from '../navigation';
import { colors, fontSize } from '../theme';

type Props = NativeStackScreenProps<RootStackParamList, 'CustomRecipe'>;

const GRIND_SIZES = [400, 600, 800, 1000, 1200, 1400];
const BEAN_TYPES = ['Arabica', 'Robusta', 'Blend', 'Liberica', 'Excelsa', 'Bebas', 'Custom'];

/** A phase while it is being edited: amounts and times are still free text. */
interface PhaseDraft {
  startTimeSeconds: number;
  pourAmountMl: number;
  action: PhaseAction;
}

type Sheet = { kind: 'bean' } | { kind: 'grind' } | { kind: 'action'; index: number } | null;

function notify(message: string) {
  AccessibilityInfo.announceForAccessibility(message);
  if (Platform.OS === 'android') ToastAndroid.show(message, ToastAndroid.SHORT);
}

function isPourAction(action: PhaseAction): boolean {
  return action === 'pourCircle' || action === 'pourCenter';
}

/** The Dart table spells the two pour actions with underscores. */
const ACTION_STRING_KEY: Record<PhaseAction, string> = {
  pourCircle: 'action_pour_circle',
  pourCenter: 'action_pour_center',
  wait: 'action_wait',
  stir: 'action_stir',
  swirl: 'action_swirl',
  cap: 'action_cap',
  flip: 'action_flip',
  press: 'action_press',
  openValve: 'action_openValve',
  closeValve: 'action_closeValve',
};

function actionLabel(lang: string, action: PhaseAction): string {
  return str(lang, ACTION_STRING_KEY[action]);
}

function beanLabel(lang: string, bean: string): string {
  if (bean === 'Blend') return str(lang, 'custom_bean_blend');
  if (bean === 'Bebas') return str(lang, 'custom_bean_bebas');
  if (bean === 'Custom') return str(lang, 'custom_bean_custom');
  return bean;
}

/** Snaps an arbitrary micron value onto the six offered grind steps. */
function snapGrind(microns: number): number {
  return GRIND_SIZES.reduce((a, b) =>
    Math.abs(a - microns) < Math.abs(b - microns) ? a : b
  );
}

export default function CustomRecipeScreen({ navigation, route }: Props) {
  const { targetMethod, initialRecipe } = route.params;
  const lang = useSettings((s) => s.appLanguage);
  const addRecipe = useRecipes((s) => s.addRecipe);
  const updateRecipe = useRecipes((s) => s.updateRecipe);
  const takeDraft = useAiDraft((s) => s.take);

  const [name, setName] = useState(() =>
    initialRecipe ? str(lang, initialRecipe.name) : ''
  );
  const [note, setNote] = useState(() =>
    initialRecipe ? str(lang, initialRecipe.description) : ''
  );
  const [extra, setExtra] = useState(() =>
    initialRecipe ? str(lang, initialRecipe.extraIngredients) : ''
  );
  const [coffee, setCoffee] = useState(() =>
    initialRecipe ? String(initialRecipe.coffeeGrams) : ''
  );
  const [water, setWater] = useState(() =>
    initialRecipe ? String(initialRecipe.totalWaterMl) : ''
  );
  const [time, setTime] = useState(() =>
    initialRecipe ? String(initialRecipe.totalDurationSeconds) : ''
  );
  const [customBean, setCustomBean] = useState(() =>
    initialRecipe && !BEAN_TYPES.includes(initialRecipe.beanType) ? initialRecipe.beanType : ''
  );
  const [beanType, setBeanType] = useState(() => {
    if (!initialRecipe) return 'Arabica';
    return BEAN_TYPES.includes(initialRecipe.beanType) ? initialRecipe.beanType : 'Custom';
  });
  const [grindMicrons, setGrindMicrons] = useState(() =>
    initialRecipe ? snapGrind(initialRecipe.targetGrindSizeMicrons) : 800
  );
  const [phases, setPhases] = useState<PhaseDraft[]>(() =>
    initialRecipe
      ? initialRecipe.phases.map((p) => ({
          startTimeSeconds: p.startTimeSeconds,
          pourAmountMl: p.pourAmountMl,
          action: p.action,
        }))
      : []
  );
  const [sheet, setSheet] = useState<Sheet>(null);

  // The AI returns bilingual "ID: ... || EN: ..." payloads while the form shows
  // one language. These hold the payload so that a field the user did not touch
  // keeps both languages on save.
  const [aiName, setAiName] = useState<string | null>(initialRecipe?.name ?? null);
  const [aiDesc, setAiDesc] = useState<string | null>(initialRecipe?.description ?? null);
  const [aiExtra, setAiExtra] = useState<string | null>(
    initialRecipe?.extraIngredients ?? null
  );

  useLayoutEffect(() => {
    navigation.setOptions({ title: str(lang, 'custom_title') });
  }, [navigation, lang]);

  /** Fills every field from a recipe, localising the bilingual ones. */
  const applyRecipe = useCallback(
    (recipe: Recipe) => {
      setAiName(recipe.name);
      setAiDesc(recipe.description);
      setAiExtra(recipe.extraIngredients);

      setName(str(lang, recipe.name));
      setNote(str(lang, recipe.description));
      setExtra(str(lang, recipe.extraIngredients));
      setCoffee(String(recipe.coffeeGrams));
      setWater(String(recipe.totalWaterMl));
      setTime(String(recipe.totalDurationSeconds));
      setGrindMicrons(snapGrind(recipe.targetGrindSizeMicrons));

      if (BEAN_TYPES.includes(recipe.beanType)) {
        setBeanType(recipe.beanType);
        setCustomBean('');
      } else {
        setBeanType('Custom');
        setCustomBean(recipe.beanType);
      }

      setPhases(
        recipe.phases.map((p) => ({
          startTimeSeconds: p.startTimeSeconds,
          pourAmountMl: p.pourAmountMl,
          action: p.action,
        }))
      );
    },
    [lang]
  );

  // Pick up whatever the AI chat left behind on the way back to this screen.
  useFocusEffect(
    useCallback(() => {
      const draft = takeDraft();
      if (draft) applyRecipe(draft);
    }, [takeDraft, applyRecipe])
  );

  /** The form's current contents as a Recipe, for the AI to work from. */
  const collectDraft = (): Recipe => {
    const resolvedBean =
      beanType === 'Custom' ? (customBean.length === 0 ? 'Custom' : customBean) : beanType;

    const recipePhases: RecipePhase[] = phases.map((p) => ({
      startTimeSeconds: p.startTimeSeconds,
      pourAmountMl: isPourAction(p.action) ? p.pourAmountMl : 0,
      instructionText: '',
      action: p.action,
    }));

    return makeRecipe({
      id: initialRecipe?.id,
      method: initialRecipe?.method ?? targetMethod,
      // Prefer the bilingual payload when the visible text still matches it, so
      // handing the draft back to the AI does not lose the other language.
      name: aiName && str(lang, aiName) === name ? aiName : name.length === 0 ? 'Custom' : name,
      description: aiDesc && str(lang, aiDesc) === note ? aiDesc : note,
      extraIngredients: aiExtra && str(lang, aiExtra) === extra ? aiExtra : extra,
      coffeeGrams: Number.parseFloat(coffee) || 15,
      totalWaterMl: Number.parseFloat(water) || 250,
      totalDurationSeconds: Number.parseInt(time, 10) || 150,
      phases: recipePhases,
      targetGrindSizeMicrons: grindMicrons,
      beanType: resolvedBean,
    });
  };

  const save = async (saveAsNew: boolean) => {
    const draft = collectDraft();
    const recipe: Recipe = saveAsNew
      ? { ...draft, id: newRecipeId(draft.name), isBuiltIn: false, isFavorite: false }
      : { ...draft, id: initialRecipe?.id ?? newRecipeId(draft.name) };

    if (saveAsNew || !initialRecipe) {
      await addRecipe(recipe);
    } else {
      await updateRecipe(recipe);
    }

    notify(str(lang, 'save_recipe_success'));
    navigation.goBack();
  };

  const addPhase = () => {
    setPhases((current) => {
      const lastStart = current.length > 0 ? current[current.length - 1].startTimeSeconds : 0;
      return [
        ...current,
        { startTimeSeconds: lastStart + 30, pourAmountMl: 50, action: 'pourCircle' },
      ];
    });
  };

  const updatePhase = (index: number, patch: Partial<PhaseDraft>) => {
    setPhases((current) =>
      current.map((phase, i) => (i === index ? { ...phase, ...patch } : phase))
    );
  };

  const beanOptions: SelectOption[] = BEAN_TYPES.map((value) => ({
    value,
    label: beanLabel(lang, value),
  }));

  const grindOptions: SelectOption[] = GRIND_SIZES.map((microns) => ({
    value: String(microns),
    label: str(lang, `custom_grind_${microns}`),
  }));

  const actionOptions: SelectOption[] = PHASE_ACTIONS.map((action) => ({
    value: action,
    label: actionLabel(lang, action),
  }));

  const sheetProps = {
    selectedSuffix: str(lang, 'selected_suffix'),
  };

  return (
    <View style={styles.screen}>
      <ScrollView contentContainerStyle={styles.body} keyboardShouldPersistTaps="handled">
        <View style={styles.aiBox}>
          <Text accessibilityRole="header" style={styles.aiTitle}>
            {str(lang, 'ai_title')}
          </Text>
          <Pressable
            accessibilityRole="button"
            accessibilityLabel={str(lang, 'ai_chat_title')}
            onPress={() =>
              navigation.navigate('AiChat', {
                targetMethod: initialRecipe?.method ?? targetMethod,
                initialRecipe: collectDraft(),
              })
            }
            style={({ pressed }) => [styles.aiButton, pressed && styles.pressed]}
          >
            <Icon name="chat-bubble-outline" size={22} color={colors.onPrimary} />
            <VisualText style={styles.aiButtonText}>{str(lang, 'ai_chat_title')}</VisualText>
          </Pressable>
        </View>

        <View style={styles.divider} />

        <LabeledInput
          label={str(lang, 'recipe_name')}
          value={name}
          onChangeText={setName}
        />
        <LabeledInput
          label={str(lang, 'custom_recipe_desc')}
          value={note}
          onChangeText={setNote}
          multiline
        />

        <Text accessibilityElementsHidden importantForAccessibility="no-hide-descendants" style={styles.caption}>
          {str(lang, 'brew_bean')}
        </Text>
        <Pressable
          accessibilityRole="button"
          accessibilityLabel={`${str(lang, 'brew_bean')}. ${beanLabel(lang, beanType)}`}
          onPress={() => setSheet({ kind: 'bean' })}
          style={({ pressed }) => [styles.selectButton, pressed && styles.pressed]}
        >
          <VisualText style={styles.selectButtonText}>{beanLabel(lang, beanType)}</VisualText>
          <Icon name="arrow-drop-down" size={28} color={colors.text} />
        </Pressable>

        {beanType === 'Custom' && (
          <LabeledInput
            label={str(lang, 'brew_bean')}
            value={customBean}
            onChangeText={setCustomBean}
          />
        )}

        <Text accessibilityElementsHidden importantForAccessibility="no-hide-descendants" style={styles.caption}>
          {str(lang, 'brew_grind')}
        </Text>
        <Pressable
          accessibilityRole="button"
          accessibilityLabel={`${str(lang, 'brew_grind')}. ${str(
            lang,
            `custom_grind_${grindMicrons}`
          )}`}
          onPress={() => setSheet({ kind: 'grind' })}
          style={({ pressed }) => [styles.selectButton, pressed && styles.pressed]}
        >
          <VisualText style={styles.selectButtonText}>{str(lang, `custom_grind_${grindMicrons}`)}</VisualText>
          <Icon name="arrow-drop-down" size={28} color={colors.text} />
        </Pressable>

        <LabeledInput
          label={str(lang, 'brew_extra')}
          value={extra}
          onChangeText={setExtra}
        />
        <LabeledInput
          label={str(lang, 'coffee_grams')}
          value={coffee}
          onChangeText={setCoffee}
          keyboardType="decimal-pad"
        />
        <LabeledInput
          label={str(lang, 'total_water')}
          value={water}
          onChangeText={setWater}
          keyboardType="decimal-pad"
        />
        <LabeledInput
          label={str(lang, 'total_time')}
          value={time}
          onChangeText={setTime}
          keyboardType="number-pad"
        />

        <Text accessibilityRole="header" style={styles.sectionHeading}>
          {str(lang, 'phases_title')}
        </Text>

        {phases.map((phase, index) => (
          <View key={index} style={styles.phaseCard}>
            <LabeledInput
              label={str(lang, 'start_sec')}
              value={String(phase.startTimeSeconds)}
              onChangeText={(v) =>
                updatePhase(index, { startTimeSeconds: Number.parseInt(v, 10) || 0 })
              }
              keyboardType="number-pad"
            />

            <Pressable
              accessibilityRole="button"
              accessibilityLabel={`${str(lang, 'phases_title')} ${index + 1}. ${actionLabel(
                lang,
                phase.action
              )}`}
              onPress={() => setSheet({ kind: 'action', index })}
              style={({ pressed }) => [styles.selectButton, pressed && styles.pressed]}
            >
              <VisualText style={styles.selectButtonText}>{actionLabel(lang, phase.action)}</VisualText>
              <Icon name="arrow-drop-down" size={28} color={colors.text} />
            </Pressable>

            {isPourAction(phase.action) && (
              <View style={styles.phaseAmount}>
                <LabeledInput
                  label={str(lang, 'water_ml')}
                  value={String(phase.pourAmountMl)}
                  onChangeText={(v) =>
                    updatePhase(index, { pourAmountMl: Number.parseFloat(v) || 0 })
                  }
                  keyboardType="decimal-pad"
                />
              </View>
            )}

            <Pressable
              accessibilityRole="button"
              accessibilityLabel={`${str(lang, 'delete_phase')} ${index + 1}`}
              onPress={() => setPhases((current) => current.filter((_, i) => i !== index))}
              style={({ pressed }) => [styles.deletePhase, pressed && styles.pressed]}
            >
              <Icon name="delete" size={26} color={colors.red} />
              <VisualText style={styles.deletePhaseText}>{str(lang, 'delete_phase')}</VisualText>
            </Pressable>
          </View>
        ))}

        <Pressable
          accessibilityRole="button"
          accessibilityLabel={str(lang, 'add_phase')}
          onPress={addPhase}
          style={({ pressed }) => [styles.addPhaseButton, pressed && styles.pressed]}
        >
          <Icon name="add" size={24} color={colors.onPrimary} />
          <VisualText style={styles.addPhaseText}>{str(lang, 'add_phase')}</VisualText>
        </Pressable>

        <View style={styles.saveBlock}>
          {initialRecipe ? (
            <>
              <Pressable
                accessibilityRole="button"
                accessibilityLabel={str(lang, 'save_overwrite')}
                onPress={() => void save(false)}
                style={({ pressed }) => [styles.savePrimary, pressed && styles.pressed]}
              >
                <VisualText style={styles.savePrimaryText}>{str(lang, 'save_overwrite')}</VisualText>
              </Pressable>
              <Pressable
                accessibilityRole="button"
                accessibilityLabel={str(lang, 'save_as_new')}
                onPress={() => void save(true)}
                style={({ pressed }) => [styles.saveOutlined, pressed && styles.pressed]}
              >
                <VisualText style={styles.saveOutlinedText}>{str(lang, 'save_as_new')}</VisualText>
              </Pressable>
            </>
          ) : (
            <Pressable
              accessibilityRole="button"
              accessibilityLabel={str(lang, 'save_recipe')}
              onPress={() => void save(true)}
              style={({ pressed }) => [styles.savePrimary, pressed && styles.pressed]}
            >
              <VisualText style={styles.savePrimaryText}>{str(lang, 'save_recipe')}</VisualText>
            </Pressable>
          )}
        </View>
      </ScrollView>

      <SelectSheet
        {...sheetProps}
        visible={sheet?.kind === 'bean'}
        title={str(lang, 'brew_bean')}
        options={beanOptions}
        currentValue={beanType}
        onClose={() => setSheet(null)}
        onSelect={(value) => {
          setBeanType(value);
          setSheet(null);
        }}
      />

      <SelectSheet
        {...sheetProps}
        visible={sheet?.kind === 'grind'}
        title={str(lang, 'brew_grind')}
        options={grindOptions}
        currentValue={String(grindMicrons)}
        onClose={() => setSheet(null)}
        onSelect={(value) => {
          setGrindMicrons(Number.parseInt(value, 10));
          setSheet(null);
        }}
      />

      <SelectSheet
        {...sheetProps}
        visible={sheet?.kind === 'action'}
        title={str(lang, 'phases_title')}
        options={actionOptions}
        currentValue={
          sheet?.kind === 'action' ? phases[sheet.index]?.action ?? 'pourCircle' : 'pourCircle'
        }
        onClose={() => setSheet(null)}
        onSelect={(value) => {
          if (sheet?.kind === 'action') {
            updatePhase(sheet.index, { action: value as PhaseAction });
          }
          setSheet(null);
        }}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  screen: {
    flex: 1,
    backgroundColor: colors.background,
  },
  body: {
    padding: 16,
    paddingBottom: 48,
  },
  aiBox: {
    padding: 16,
    borderRadius: 12,
    backgroundColor: colors.purple50,
    borderWidth: 1,
    borderColor: '#CE93D8', // purple.200
  },
  aiTitle: {
    fontSize: fontSize.subheading,
    fontWeight: 'bold',
    color: '#9C27B0', // purple
    marginBottom: 12,
  },
  aiButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
    paddingVertical: 16,
    borderRadius: 4,
    backgroundColor: '#9C27B0',
  },
  aiButtonText: {
    color: colors.onPrimary,
    fontSize: fontSize.body,
    fontWeight: 'bold',
  },
  divider: {
    height: 1,
    backgroundColor: colors.divider,
    marginVertical: 24,
  },
  caption: {
    fontSize: 14,
    fontWeight: 'bold',
    color: colors.text,
    marginBottom: 6,
  },
  selectButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    backgroundColor: colors.card,
    borderWidth: 1,
    borderColor: colors.divider,
    borderRadius: 4,
    paddingHorizontal: 12,
    minHeight: 52,
    marginBottom: 16,
  },
  selectButtonText: {
    flex: 1,
    fontSize: fontSize.body,
    color: colors.text,
  },
  sectionHeading: {
    marginTop: 8,
    marginBottom: 12,
    fontSize: fontSize.subheading,
    fontWeight: 'bold',
    color: colors.text,
  },
  phaseCard: {
    backgroundColor: colors.card,
    borderRadius: 4,
    padding: 12,
    marginBottom: 16,
    elevation: 1,
  },
  phaseAmount: {
    marginTop: 4,
  },
  deletePhase: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'flex-end',
    gap: 6,
    paddingVertical: 10,
  },
  deletePhaseText: {
    fontSize: fontSize.body,
    color: colors.red,
    fontWeight: '500',
  },
  addPhaseButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
    paddingVertical: 16,
    borderRadius: 4,
    backgroundColor: colors.primary,
  },
  addPhaseText: {
    color: colors.onPrimary,
    fontSize: fontSize.body,
    fontWeight: '500',
  },
  saveBlock: {
    marginTop: 32,
    gap: 12,
  },
  savePrimary: {
    backgroundColor: colors.primary,
    paddingVertical: 18,
    borderRadius: 4,
    alignItems: 'center',
  },
  savePrimaryText: {
    color: colors.onPrimary,
    fontSize: fontSize.subheading,
    fontWeight: '500',
  },
  saveOutlined: {
    borderWidth: 1,
    borderColor: colors.primary,
    paddingVertical: 18,
    borderRadius: 4,
    alignItems: 'center',
  },
  saveOutlinedText: {
    color: colors.primary,
    fontSize: fontSize.subheading,
    fontWeight: '500',
  },
  pressed: {
    opacity: 0.75,
  },
});
