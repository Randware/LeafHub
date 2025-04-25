<script lang="ts" module>
	export type ServerCheckResult = 'Success' | 'Failure';
</script>

<script lang="ts">
	import { Loader, CircleCheck, Ban } from '@lucide/svelte';
	import { onMount } from 'svelte';
	import { fly } from 'svelte/transition';

	export let serverAddress: string;
	export let checkResult: ServerCheckResult | null = null;
	export let onResult: (result: ServerCheckResult) => void;

	function setResult(result: ServerCheckResult) {
		checkResult = result;

		onResult(result);
	}

	onMount(() => {
		// TODO: Implement proper pinging through microcontroller, this wouldn't work (no internet when connected to microcontroller access point)

		fetch(serverAddress, { mode: 'no-cors' })
			.then((_) => {
				setResult('Success');
			})
			.catch((_) => {
				setResult('Failure');
			});
	});
</script>

<div class="flex flex-col items-center justify-center gap-2">
	{#if checkResult}
		{#if checkResult == 'Success'}
			<div class="flex flex-col items-center gap-6">
				<div class="font-fancy text-2xl font-extrabold">Server is reachable!</div>
				<CircleCheck size={40} class="text-primary" />
			</div>
		{:else}
			<div class="flex flex-col items-center gap-6">
				<div class="font-fancy text-2xl font-extrabold">Server could not be reached</div>
				<Ban size={40} class="text-red-400" />
			</div>
		{/if}
	{:else}
		<div class="animate-spin">
			<Loader size={32} />
		</div>

		<div class="font-semibold">Checking server connection</div>
	{/if}
</div>
