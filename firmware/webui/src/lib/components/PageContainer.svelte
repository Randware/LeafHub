<script lang="ts">
	import type { Component } from 'svelte';
	import { fly } from 'svelte/transition';
	import AuthPage from './pages/AuthPage.svelte';
	import FinishPage from './pages/FinishPage.svelte';
	import NetworkPage from './pages/NetworkPage.svelte';
	import ServerPage from './pages/ServerPage.svelte';
	import WelcomePage from './pages/WelcomePage.svelte';
	import { advancedSetup } from '$lib/store/settings';
	import Button from './Button.svelte';

	type Step = {
		component: Component<{ block: boolean }>;
		block: boolean;
		advanced: boolean;
	};

	const stepConfig: Step[] = [
		{ component: WelcomePage, block: false, advanced: false },
		{ component: NetworkPage, block: true, advanced: false },
		{ component: ServerPage, block: true, advanced: true },
		{ component: AuthPage, block: false, advanced: false },
		{ component: FinishPage, block: false, advanced: false }
	];

	$: steps = stepConfig.filter((step) => !step.advanced || step.advanced === $advancedSetup);

	$: currentStep = steps[0];

	const slideDistance = 10;
	let direction = 1;

	$: progress = ((steps.indexOf(currentStep) + 1) / steps.length) * 100;

	$: firstPage = currentStep === steps[0];
	$: lastPage = currentStep === steps[steps.length - 1];

	export function next() {
		const idx = steps.indexOf(currentStep);

		if (idx < steps.length - 1) {
			direction = 1;

			let nextStep: Step | undefined = steps.find((step) => steps.indexOf(step) > idx);

			if (nextStep) {
				currentStep = steps[steps.indexOf(nextStep)];
			}
		}
	}

	export function prev() {
		const idx = steps.indexOf(currentStep);

		if (idx > 0) {
			direction = -1;

			let prevStep: Step | undefined = steps.findLast((step) => steps.indexOf(step) < idx);

			if (prevStep) {
				currentStep = steps[steps.indexOf(prevStep)];
			}
		}
	}
</script>

<main class="bg-light text-dark h-full overflow-hidden rounded-xl p-6 text-xl">
	<div class="bg-secondary h-2 w-full rounded-full">
		<div
			class="bg-primary h-2 rounded-full transition-[width] duration-500"
			style="width: {progress}%"
		></div>
	</div>

	{#key steps.indexOf(currentStep)}
		<div
			in:fly={{ x: direction * slideDistance, duration: 500, opacity: 0 }}
			class="flex h-full flex-col items-center justify-center"
		>
			<svelte:component this={currentStep.component} bind:block={currentStep.block} />
		</div>
	{/key}
</main>

<footer class="flex w-full justify-between">
	<Button onclick={prev} disabled={firstPage}>Back</Button>

	<Button onclick={next} disabled={currentStep.block || lastPage}>Next</Button>
</footer>
