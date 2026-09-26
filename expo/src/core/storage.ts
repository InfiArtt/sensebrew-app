// Typed AsyncStorage helpers.
//
// Keys are the same strings lib/core/*.dart passes to SharedPreferences, so a
// device that has run either build stores its settings under the same names and
// the two versions stay diffable while the migration is in progress.
import AsyncStorage from '@react-native-async-storage/async-storage';

export async function getString(key: string, fallback: string): Promise<string> {
  const raw = await AsyncStorage.getItem(key);
  return raw ?? fallback;
}

export async function getStringOrNull(key: string): Promise<string | null> {
  return AsyncStorage.getItem(key);
}

export async function getNumber(key: string, fallback: number): Promise<number> {
  const raw = await AsyncStorage.getItem(key);
  if (raw === null) return fallback;
  const parsed = Number(raw);
  return Number.isFinite(parsed) ? parsed : fallback;
}

export async function getBool(key: string, fallback: boolean): Promise<boolean> {
  const raw = await AsyncStorage.getItem(key);
  if (raw === null) return fallback;
  return raw === 'true';
}

export async function getStringList(key: string): Promise<string[]> {
  const raw = await AsyncStorage.getItem(key);
  if (!raw) return [];
  try {
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed.map(String) : [];
  } catch {
    return [];
  }
}

export const setString = (key: string, value: string) => AsyncStorage.setItem(key, value);
export const setNumber = (key: string, value: number) =>
  AsyncStorage.setItem(key, String(value));
export const setBool = (key: string, value: boolean) =>
  AsyncStorage.setItem(key, value ? 'true' : 'false');
export const setStringList = (key: string, value: string[]) =>
  AsyncStorage.setItem(key, JSON.stringify(value));
export const remove = (key: string) => AsyncStorage.removeItem(key);
