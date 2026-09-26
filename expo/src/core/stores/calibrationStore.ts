// Ported from lib/core/calibration_state.dart.
import { create } from 'zustand';

import * as storage from '../storage';

interface CalibrationState {
  hydrated: boolean;

  /** Measured pour rate. Every pour phase's duration is derived from this. */
  mlPerSecond: number;
  secondsPerRotation: number;
  isCalibrated: boolean;

  lastVolume: number;
  lastSeconds: number;

  spoonCapacityGrams: number;
  grinderId: string;

  hydrate: () => Promise<void>;
  save: (params: {
    targetVolumeMl: number;
    totalSeconds: number;
    secondsPerRotation: number;
    spoonCapacity: number;
    grinderId: string;
  }) => Promise<void>;
}

export const useCalibration = create<CalibrationState>((set, get) => ({
  hydrated: false,

  mlPerSecond: 0,
  secondsPerRotation: 2,
  isCalibrated: false,
  lastVolume: 150,
  lastSeconds: 20,
  spoonCapacityGrams: 10,
  grinderId: 'timemore_c2',

  hydrate: async () => {
    if (get().hydrated) return;

    const [
      mlPerSecond,
      secondsPerRotation,
      isCalibrated,
      lastVolume,
      lastSeconds,
      spoonCapacityGrams,
      grinderId,
    ] = await Promise.all([
      storage.getNumber('ml_per_second', 0),
      storage.getNumber('seconds_per_rotation', 2),
      storage.getBool('is_calibrated', false),
      storage.getNumber('last_volume', 150),
      storage.getNumber('last_seconds', 20),
      storage.getNumber('spoon_capacity', 10),
      storage.getString('grinder_id', 'timemore_c2'),
    ]);

    set({
      hydrated: true,
      mlPerSecond,
      secondsPerRotation,
      isCalibrated,
      lastVolume,
      lastSeconds,
      spoonCapacityGrams,
      grinderId,
    });
  },

  save: async ({ targetVolumeMl, totalSeconds, secondsPerRotation, spoonCapacity, grinderId }) => {
    const mlPerSecond = targetVolumeMl / totalSeconds;

    set({
      mlPerSecond,
      secondsPerRotation,
      lastVolume: Math.trunc(targetVolumeMl),
      lastSeconds: totalSeconds,
      spoonCapacityGrams: spoonCapacity,
      grinderId,
      isCalibrated: true,
    });

    await Promise.all([
      storage.setNumber('ml_per_second', mlPerSecond),
      storage.setNumber('seconds_per_rotation', secondsPerRotation),
      storage.setBool('is_calibrated', true),
      storage.setNumber('last_volume', Math.trunc(targetVolumeMl)),
      storage.setNumber('last_seconds', totalSeconds),
      storage.setNumber('spoon_capacity', spoonCapacity),
      storage.setString('grinder_id', grinderId),
    ]);
  },
}));
