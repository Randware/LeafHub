<script lang="ts">
	import { writable } from 'svelte/store';
	import AuthPage from './pages/AuthPage.svelte';
	import FinishPage from './pages/FinishPage.svelte';
	import NetworkPage from './pages/NetworkPage.svelte';
	import ServerPage from './pages/ServerPage.svelte';
	import WelcomePage from './pages/WelcomePage.svelte';

	type Page = 'welcome' | 'network' | 'server' | 'auth' | 'finish';

	const stepOrder: Page[] = ['welcome', 'network', 'server', 'auth', 'finish'];
	let currentStep: Page = 'welcome';

	export function next() {
		const currentIndex = stepOrder.indexOf(currentStep);
		if (currentIndex < stepOrder.length - 1) {
			currentStep = stepOrder[currentIndex + 1];
			updateState();
		}
	}

	export function prev() {
		const currentIndex = stepOrder.indexOf(currentStep);

		if (currentIndex > 0) {
			currentStep = stepOrder[currentIndex - 1];
			updateState();
		}
	}

	export const pageState = writable({
		firstPage: currentStep === stepOrder[0],
		lastPage: currentStep === stepOrder[stepOrder.length - 1]
	});

	function updateState() {
		pageState.set({
			firstPage: currentStep === stepOrder[0],
			lastPage: currentStep === stepOrder[stepOrder.length - 1]
		});
	}
</script>

{#if currentStep === 'welcome'}
	<WelcomePage />
{:else if currentStep === 'network'}
	<NetworkPage />
{:else if currentStep === 'server'}
	<ServerPage />
{:else if currentStep === 'auth'}
	<AuthPage />
{:else if currentStep === 'finish'}
	<FinishPage />
{/if}
