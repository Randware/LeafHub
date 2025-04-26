<script lang="ts">
	import type { Component } from 'svelte';
	import { fly } from 'svelte/transition';
	import AuthPage from './pages/AuthPage.svelte';
	import FinishPage from './pages/FinishPage.svelte';
	import NetworkPage from './pages/NetworkPage.svelte';
	import ServerPage from './pages/ServerPage.svelte';
	import WelcomePage from './pages/WelcomePage.svelte';
	import { advancedSetup } from '$lib/store/settings';

	type Step = {
		component: Component<{ block: boolean }>;
		block: boolean;
		advanced: boolean;
	};

	const steps: Step[] = [
		{ component: WelcomePage, block: false, advanced: false },
		{ component: NetworkPage, block: true, advanced: false },
		{ component: ServerPage, block: true, advanced: true },
		{ component: AuthPage, block: false, advanced: false },
		{ component: FinishPage, block: false, advanced: false }
	];

	let currentStep: Step = steps[0];

	let direction = 1;
	let slideDistance = 10;

	$: firstPage = currentStep === steps[0];
	$: lastPage = currentStep === steps[steps.length - 1];

	export function next() {
		const idx = steps.indexOf(currentStep);

		if (idx < steps.length - 1) {
			direction = 1;

			let nextStep: Step | undefined = steps.find(
				(step) => steps.indexOf(step) > idx && (!step.advanced || step.advanced === $advancedSetup)
			);

			if (nextStep) {
				currentStep = steps[steps.indexOf(nextStep)];
			}
		}
	}

	export function prev() {
		const idx = steps.indexOf(currentStep);

		if (idx > 0) {
			direction = -1;

			let prevStep: Step | undefined = steps.findLast(
				(step) => steps.indexOf(step) < idx && (!step.advanced || step.advanced === $advancedSetup)
			);

			if (prevStep) {
				currentStep = steps[steps.indexOf(prevStep)];
			}
		}
	}
</script>

<main class="bg-light text-dark h-full overflow-hidden rounded-xl p-6 text-xl">
	{#key currentStep}
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
		class="text-dark {firstPage
			? 'bg-gray-400/80'
			: 'bg-primary hover:bg-primary/70'} rounded-xl px-4 py-2 text-xl font-semibold transition-colors"
		onclick={prev}
		disabled={firstPage}
	>
		Back
	</button>

	<button
		class="text-dark {currentStep.block || lastPage
			? 'bg-gray-400/80'
			: 'bg-primary hover:bg-primary/70 '} rounded-xl px-4 py-2 text-xl font-semibold transition-colors"
		onclick={next}
		disabled={currentStep.block || lastPage}
	>
		Next
	</button>
</footer>
