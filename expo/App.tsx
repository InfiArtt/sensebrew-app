// SenseBrew — Expo build. Ported from the Flutter app in ../lib.
//
// The Flutter build wired four ChangeNotifiers through MultiProvider; the Zustand
// stores here are module-level, so the tree only has to wait for them to read
// their persisted values before the first screen renders. Rendering earlier
// would show "not calibrated" for a moment to someone who is calibrated, and a
// screen reader would announce it.
import Icon from './src/components/Icon';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { StatusBar } from 'expo-status-bar';
import { useEffect, useState } from 'react';
import { ActivityIndicator, Pressable, StyleSheet, View } from 'react-native';
import { SafeAreaProvider } from 'react-native-safe-area-context';

import { str } from './src/core/appStrings';
import { prepareAudio } from './src/core/audio/metronome';
import { useCalibration } from './src/core/stores/calibrationStore';
import { useRecipes } from './src/core/stores/recipeStore';
import { useSettings } from './src/core/stores/settingsStore';
import type { RootStackParamList } from './src/navigation';
import AiChatScreen from './src/screens/AiChatScreen';
import BrewingScreen from './src/screens/BrewingScreen';
import CalibrationScreen from './src/screens/CalibrationScreen';
import CustomRecipeScreen from './src/screens/CustomRecipeScreen';
import HomeScreen from './src/screens/HomeScreen';
import MethodRecipeScreen from './src/screens/MethodRecipeScreen';
import PourCalculatorScreen from './src/screens/PourCalculatorScreen';
import SettingsScreen from './src/screens/SettingsScreen';
import { colors, fontSize } from './src/theme';

const Stack = createNativeStackNavigator<RootStackParamList>();

export default function App() {
  const [ready, setReady] = useState(false);
  const lang = useSettings((s) => s.appLanguage);

  useEffect(() => {
    let cancelled = false;

    (async () => {
      await Promise.all([
        useSettings.getState().hydrate(),
        useCalibration.getState().hydrate(),
        useRecipes.getState().load(),
        // Creating the audio players takes long enough that doing it when a pour
        // phase begins would cost the first beat.
        prepareAudio(),
      ]);
      if (!cancelled) setReady(true);
    })();

    return () => {
      cancelled = true;
    };
  }, []);

  if (!ready) {
    return (
      <View style={styles.splash}>
        <StatusBar style="light" />
        <ActivityIndicator size="large" color={colors.primary} />
      </View>
    );
  }

  return (
    <SafeAreaProvider>
      <StatusBar style="light" />
      <NavigationContainer>
        <Stack.Navigator
          screenOptions={{
            headerStyle: { backgroundColor: colors.primary },
            headerTintColor: colors.onPrimary,
            headerTitleStyle: { fontSize: fontSize.heading, fontWeight: 'bold' },
          }}
        >
          <Stack.Screen
            name="Home"
            component={HomeScreen}
            options={({ navigation }) => ({
              title: str(lang, 'app_title'),
              headerRight: () => (
                <Pressable
                  accessibilityRole="button"
                  accessibilityLabel={str(lang, 'settings_menu')}
                  onPress={() => navigation.navigate('Settings')}
                  hitSlop={12}
                >
                  <Icon name="settings" size={26} color={colors.onPrimary} />
                </Pressable>
              ),
            })}
          />
          <Stack.Screen name="MethodRecipes" component={MethodRecipeScreen} />
          <Stack.Screen name="Brewing" component={BrewingScreen} />
          <Stack.Screen name="Calibration" component={CalibrationScreen} />
          <Stack.Screen name="Settings" component={SettingsScreen} />
          <Stack.Screen name="PourCalculator" component={PourCalculatorScreen} />
          <Stack.Screen name="CustomRecipe" component={CustomRecipeScreen} />
          <Stack.Screen name="AiChat" component={AiChatScreen} />
        </Stack.Navigator>
      </NavigationContainer>
    </SafeAreaProvider>
  );
}

const styles = StyleSheet.create({
  splash: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: colors.background,
  },
});
