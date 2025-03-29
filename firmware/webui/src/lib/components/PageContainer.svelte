<script lang="ts">
	import type { Component } from 'svelte';
	import { fly } from 'svelte/transition';
	import AuthPage from './pages/AuthPage.svelte';
	import FinishPage from './pages/FinishPage.svelte';
	import NetworkPage from './pages/NetworkPage.svelte';
	import ServerPage from './pages/ServerPage.svelte';
	import WelcomePage from './pages/WelcomePage.svelte';

	type Step = {
		component: Component<{ block: boolean }>;
		block: boolean;
	};

	const steps: Step[] = [
		{ component: WelcomePage, block: false },
		{ component: NetworkPage, block: true },
		{ component: ServerPage, block: false },
		{ component: AuthPage, block: false },
		{ component: FinishPage, block: false }
	];

	let currentStep: Step = steps[0];
	let currentIndex = 0;

	let direction = 1;
	let slideDistance = 10;

	$: firstPage = currentStep === steps[0];
	$: lastPage = currentStep === steps[steps.length - 1];

	export function next() {
		const idx = steps.indexOf(currentStep);

		if (idx < steps.length - 1) {
			direction = 1;
			currentIndex = idx + 1;
			currentStep = steps[currentIndex];
		}
	}

	export function prev() {
		const idx = steps.indexOf(currentStep);

		if (idx > 0) {
			direction = -1;
			currentIndex = idx - 1;
			currentStep = steps[currentIndex];
		}
	}
</script>

<main class="bg-light text-dark h-full overflow-hidden rounded-xl p-6 text-xl">
	{#key currentIndex}
		<div
			in:fly={{ x: direction * slideDistance, duration: 500, opacity: 0 }}
			class="flex h-full flex-col items-center justify-center"
		>
			<svelte:component this={currentStep.component} bind:block={currentStep.block} />
		</div>
	{/key}
</main>

<footer class="flex w-full justify-between">
	<button
		class="text-dark bg-primary hover:bg-primary/70 rounded-xl px-4 py-2 text-xl font-semibold transition-colors"
		on:click={prev}
		disabled={firstPage}
	>
		Back
	</button>
	<button
		class="text-dark bg-primary hover:bg-primary/70 rounded-xl px-4 py-2 text-xl font-semibold transition-colors"
		on:click={next}
		disabled={currentStep.block || lastPage}
	>
		Next
	</button>
</footer>
