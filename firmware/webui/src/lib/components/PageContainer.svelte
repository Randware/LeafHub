<script lang="ts">
	import type { Component } from 'svelte';
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

	$: firstPage = currentStep === steps[0];
	$: lastPage = currentStep === steps[steps.length - 1];

	export function next() {
		const idx = steps.indexOf(currentStep);

		if (idx < steps.length - 1) {
			currentStep = steps[idx + 1];
		}
	}

	export function prev() {
		const idx = steps.indexOf(currentStep);

		if (idx > 0) {
			currentStep = steps[idx - 1];
		}
	}
</script>

<main class="flex h-full flex-col items-center justify-center">
	<svelte:component this={currentStep.component} bind:block={currentStep.block} />
</main>

<footer class="flex w-full justify-between">
	<button
		class="text-dark bg-primary hover:bg-primary/70 rounded-xl px-4 py-2 text-lg font-semibold transition-colors"
		onclick={prev}
		disabled={firstPage}
	>
		Back
	</button>
	<button
		class="text-dark bg-primary hover:bg-primary/70 rounded-xl px-4 py-2 text-lg font-semibold transition-colors"
		onclick={next}
		disabled={currentStep.block || lastPage}
	>
		Next
	</button>
</footer>
