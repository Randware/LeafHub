import { writable, type Writable } from "svelte/store";

// This is the address from which this website was served,
// so in our case, the microcontroller
export const host: string = window.location.hostname;

export const advancedSetup: Writable<boolean> = writable(false);
