// Ported from lib/screens/method_recipe_screen.dart.
import Icon from '../components/Icon';
import type { NativeStackScreenProps } from '@react-navigation/native-stack';
import { useLayoutEffect, useState } from 'react';
import {
  AccessibilityInfo,
  Alert,
  Modal,
  Platform,
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  ToastAndroid,
  View,
} from 'react-native';

import { str } from '../core/appStrings';
import { Recipe, trimNumber } from '../core/recipe';
import { useCalibration } from '../core/stores/calibrationStore';
import { useRecipes } from '../core/stores/recipeStore';
import { useSettings } from '../core/stores/settingsStore';
import type { RootStackParamList } from '../navigation';
import { colors, fontSize } from '../theme';

type Props = NativeStackScreenProps<RootStackParamList, 'MethodRecipes'>;

/** A section header row, or a recipe row. */
type ListItem = { kind: 'header'; key: string } | { kind: 'recipe'; recipe: Recipe };

function notify(message: string) {
  // The Flutter build paired a SnackBar with an explicit announce() so the
  // message reached TalkBack too; a toast alone is not announced reliably.
  AccessibilityInfo.announceForAccessibility(message);
  if (Platform.OS === 'android') ToastAndroid.show(message, ToastAndroid.LONG);
}

/** Groups the sorted list into Favourites / Yours / Built-in, as in Dart. */
function buildListItems(recipes: Recipe[]): ListItem[] {
  const items: ListItem[] = [];
  let hasFav = false;
  let hasCustom = false;
  let hasBuiltIn = false;

  recipes.forEach((recipe) => {
    if (recipe.isFavorite) {
      if (!hasFav) {
        items.push({ kind: 'header', key: 'header_favorites' });
        hasFav = true;
      }
    } else if (!recipe.isBuiltIn) {
      if (!hasCustom) {
        items.push({ kind: 'header', key: 'header_custom' });
        hasCustom = true;
      }
    } else if (!hasBuiltIn) {
      items.push({ kind: 'header', key: 'header_builtin' });
      hasBuiltIn = true;
    }
    items.push({ kind: 'recipe', recipe });
  });

  return items;
}

export default function MethodRecipeScreen({ navigation, route }: Props) {
  const { method, methodName } = route.params;
  const lang = useSettings((s) => s.appLanguage);
  const isCalibrated = useCalibration((s) => s.isCalibrated);
  const recipes = useRecipes((s) => s.recipes);
  const getRecipesByMethod = useRecipes((s) => s.getRecipesByMethod);
  const toggleFavorite = useRecipes((s) => s.toggleFavorite);
  const deleteRecipe = useRecipes((s) => s.deleteRecipe);

  const [sheetRecipe, setSheetRecipe] = useState<Recipe | null>(null);

  useLayoutEffect(() => {
    navigation.setOptions({ title: methodName });
  }, [navigation, methodName]);

  // `recipes` is read so this recomputes whenever the store changes.
  const items = buildListItems(getRecipesByMethod(method));
  void recipes;

  const startBrew = (recipe: Recipe) => {
    setSheetRecipe(null);
    if (!isCalibrated) {
      // Every pour duration is derived from the measured flow rate, so brewing
      // before calibrating would divide by zero.
      notify(str(lang, 'uncalibrated_status'));
      return;
    }
    navigation.navigate('Brewing', { recipe });
  };

  const confirmDelete = (recipe: Recipe) => {
    setSheetRecipe(null);
    Alert.alert(
      str(lang, 'delete_confirm_title'),
      str(lang, 'delete_confirm_desc').replace('{0}', str(lang, recipe.name)),
      [
        { text: str(lang, 'cancel_brew_btn'), style: 'cancel' },
        {
          text: str(lang, 'delete_btn'),
          style: 'destructive',
          onPress: () => void deleteRecipe(recipe.id),
        },
      ]
    );
  };

  return (
    <View style={styles.screen}>
      <View style={styles.headerArea}>
        <Pressable
          accessible
          accessibilityRole="button"
          accessibilityLabel={str(lang, 'custom_recipe_label')}
          onPress={() => navigation.navigate('CustomRecipe', { targetMethod: method })}
          style={({ pressed }) => [styles.newRecipeButton, pressed && styles.pressed]}
        >
          <Icon name="add" size={24} color={colors.purple900} />
          <Text style={styles.newRecipeText}>{str(lang, 'custom_recipe_btn')}</Text>
        </Pressable>
      </View>

      <ScrollView contentContainerStyle={styles.list}>
        {items.map((item) => {
          if (item.kind === 'header') {
            return (
              <Text key={item.key} accessibilityRole="header" style={styles.sectionHeader}>
                {str(lang, item.key)}
              </Text>
            );
          }

          const { recipe } = item;
          const dose = trimNumber(recipe.coffeeGrams);
          const water = trimNumber(recipe.totalWaterMl);
          const favLabel = str(lang, recipe.isFavorite ? 'remove_favorite' : 'mark_favorite');

          return (
            <View key={recipe.id} style={styles.recipeCard}>
              <Pressable
                accessible
                // No role="button": this is a recipe in a list of recipes.
                accessibilityState={{ selected: recipe.isFavorite }}
                accessibilityLabel={str(lang, 'recipe_label', [
                  str(lang, recipe.name),
                  dose,
                  water,
                ])}
                onPress={() => setSheetRecipe(recipe)}
                style={({ pressed }) => [styles.recipeMain, pressed && styles.pressed]}
              >
                {/*
                  Hidden from the reader: the row's own label already says
                  "<name>, N grams of coffee, N millilitres of water". Leaving
                  these visible added a second stop that just said "13g | 200ml".
                */}
                <Text
                  importantForAccessibility="no-hide-descendants"
                  style={styles.recipeTitle}
                >
                  {str(lang, recipe.name)}
                </Text>
                <Text
                  importantForAccessibility="no-hide-descendants"
                  style={styles.recipeMeta}
                >
                  {`${dose}g | ${water}ml`}
                </Text>
              </Pressable>

              <Pressable
                accessibilityRole="button"
                accessibilityLabel={favLabel}
                onPress={() => void toggleFavorite(recipe.id)}
                hitSlop={8}
                style={({ pressed }) => [styles.favButton, pressed && styles.pressed]}
              >
                <Icon
                  name={recipe.isFavorite ? 'star' : 'star-border'}
                  size={28}
                  color={recipe.isFavorite ? colors.amber : colors.textDisabled}
                />
              </Pressable>
            </View>
          );
        })}
      </ScrollView>

      <Modal
        visible={sheetRecipe !== null}
        transparent
        animationType="slide"
        onRequestClose={() => setSheetRecipe(null)}
      >
        <Pressable
          style={styles.scrim}
          accessibilityRole="button"
          accessibilityLabel={str(lang, 'cancel_brew_btn')}
          onPress={() => setSheetRecipe(null)}
        />
        {sheetRecipe && (
          <View style={styles.sheet}>
            <Text accessibilityRole="header" style={styles.sheetTitle}>
              {str(lang, sheetRecipe.name)}
            </Text>

            <Pressable
              accessibilityRole="button"
              accessibilityLabel={str(lang, 'brew_btn')}
              onPress={() => startBrew(sheetRecipe)}
              style={({ pressed }) => [styles.sheetPrimary, pressed && styles.pressed]}
            >
              <Icon name="play-arrow" size={24} color={colors.onPrimary} />
              <Text style={styles.sheetPrimaryText}>{str(lang, 'brew_btn')}</Text>
            </Pressable>

            <Pressable
              accessibilityRole="button"
              accessibilityLabel={str(lang, 'edit_btn')}
              onPress={() => {
                setSheetRecipe(null);
                navigation.navigate('CustomRecipe', {
                  targetMethod: sheetRecipe.method,
                  initialRecipe: sheetRecipe,
                });
              }}
              style={({ pressed }) => [styles.sheetOutlined, pressed && styles.pressed]}
            >
              <Icon name="edit" size={24} color={colors.primary} />
              <Text style={styles.sheetOutlinedText}>{str(lang, 'edit_btn')}</Text>
            </Pressable>

            <Pressable
              accessibilityRole="button"
              accessibilityLabel={str(lang, 'delete_btn')}
              onPress={() => confirmDelete(sheetRecipe)}
              style={({ pressed }) => [styles.sheetOutlined, pressed && styles.pressed]}
            >
              <Icon name="delete" size={24} color={colors.red} />
              <Text style={[styles.sheetOutlinedText, { color: colors.red }]}>
                {str(lang, 'delete_btn')}
              </Text>
            </Pressable>
          </View>
        )}
      </Modal>
    </View>
  );
}

const styles = StyleSheet.create({
  screen: {
    flex: 1,
    backgroundColor: colors.background,
  },
  headerArea: {
    paddingHorizontal: 16,
    paddingVertical: 16,
  },
  newRecipeButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
    paddingVertical: 16,
    paddingHorizontal: 8,
    borderRadius: 4,
    backgroundColor: colors.purple50,
  },
  newRecipeText: {
    color: colors.purple900,
    fontSize: fontSize.body,
    fontWeight: '500',
    textAlign: 'center',
  },
  list: {
    paddingBottom: 24,
  },
  sectionHeader: {
    fontSize: fontSize.body,
    fontWeight: 'bold',
    color: colors.blueGrey,
    paddingLeft: 20,
    paddingTop: 16,
    paddingBottom: 8,
  },
  recipeCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: colors.card,
    borderRadius: 4,
    marginHorizontal: 16,
    marginBottom: 8,
    elevation: 1,
  },
  recipeMain: {
    flex: 1,
    paddingVertical: 12,
    paddingHorizontal: 16,
  },
  recipeTitle: {
    fontSize: fontSize.body,
    fontWeight: 'bold',
    color: colors.text,
  },
  recipeMeta: {
    marginTop: 4,
    fontSize: 14,
    color: colors.textSecondary,
  },
  favButton: {
    width: 56,
    height: 56,
    alignItems: 'center',
    justifyContent: 'center',
  },
  scrim: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
  },
  sheet: {
    backgroundColor: colors.card,
    padding: 16,
    paddingBottom: 32,
    borderTopLeftRadius: 8,
    borderTopRightRadius: 8,
    gap: 8,
  },
  sheetTitle: {
    fontSize: fontSize.heading,
    fontWeight: 'bold',
    color: colors.text,
    marginBottom: 8,
  },
  sheetPrimary: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
    paddingVertical: 16,
    borderRadius: 4,
    backgroundColor: colors.primary,
  },
  sheetPrimaryText: {
    color: colors.onPrimary,
    fontSize: fontSize.body,
    fontWeight: '500',
  },
  sheetOutlined: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
    paddingVertical: 14,
    borderRadius: 4,
    borderWidth: 1,
    borderColor: colors.divider,
  },
  sheetOutlinedText: {
    color: colors.primary,
    fontSize: fontSize.body,
    fontWeight: '500',
  },
  pressed: {
    opacity: 0.75,
  },
});
