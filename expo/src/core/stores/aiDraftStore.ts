// A one-slot handover for the recipe the AI chat produces.
//
// In Flutter, AiChatScreen returned its draft through `Navigator.pop(context,
// recipe)` and CustomRecipeScreen awaited it. React Navigation has no return
// value, and a callback in route params is not serialisable, so the draft is
// parked here: the chat puts it down, the form picks it up once on focus.
import { create } from 'zustand';

import type { Recipe } from '../recipe';

interface AiDraftState {
  pending: Recipe | null;
  /** Called by the AI chat when the user taps "apply to form". */
  put: (recipe: Recipe) => void;
  /** Returns the draft and clears it, so it is applied exactly once. */
  take: () => Recipe | null;
}

export const useAiDraft = create<AiDraftState>((set, get) => ({
  pending: null,

  put: (recipe) => set({ pending: recipe }),

  take: () => {
    const { pending } = get();
    if (pending) set({ pending: null });
    return pending;
  },
}));
