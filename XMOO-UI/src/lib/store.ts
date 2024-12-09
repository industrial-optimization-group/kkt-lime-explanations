import { writable } from 'svelte/store';

// Define the store state type
interface StoreState {
  numObjectives: number;
  referencePoint: number[];
  potentialReferencePoint: number[];
  lagrangeMultipliers: number[];
  partialTradeoffs: number[][];
  fx: number[]| undefined;
  ideal:number[] | undefined;
  nadir:number[] | undefined;
  objective_names: string[];
  short_names: string[];
  decimal_places: number;
  approximated_solution: number[];
  history_solutions: number[][];
}

// Define the number of objectives
const numObjectives = 4;

// Create a store with the defined state type
export const store = writable<StoreState>({
  numObjectives,
  referencePoint: [],
  potentialReferencePoint: [],
  lagrangeMultipliers: Array(numObjectives).fill(0),
  partialTradeoffs: Array(numObjectives).fill(Array(numObjectives).fill(0)),
  fx: undefined,
  ideal: undefined,
  nadir: undefined,
  objective_names: Array(numObjectives).fill("Objective"),
  short_names: [],
  decimal_places: 0,
  approximated_solution: [],
  history_solutions: [],
});
