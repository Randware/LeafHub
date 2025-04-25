<script lang="ts">
	import FloatingWindow from '../FloatingWindow.svelte';
	import PageAnimator from '../PageAnimator.svelte';
	import ServerChecker, { type ServerCheckResult } from '../ServerChecker.svelte';
	import { CircleCheck } from '@lucide/svelte';

	export let block: boolean;

	let serverAddress: string = '';
	let showChecker: boolean = false;

	let lastCheck: ServerCheckResult = 'Failure';

	function onResult(result: ServerCheckResult) {
		lastCheck = result;
	}

	function onClose() {
		showChecker = false;

		if (lastCheck == 'Success') {
			block = false;
		} else {
			block = true;
		}
	}
</script>

<div class="flex flex-col gap-6 text-center">
	{#if showChecker}
		<FloatingWindow back={onClose}>
			<ServerChecker {serverAddress} {onResult} />
		</FloatingWindow>
	{/if}

	{#if block}
		<div class="font-fancy text-3xl font-extrabold">Server</div>
		<div class="text-bold">Now, let's tell your pot where it should send its data</div>

		<div class="flex flex-col items-center gap-2 font-semibold">
			<label for="ssid" class="text-dark text-lg">Server address</label>
			<input
				id="ssid"
				type="text"
				bind:value={serverAddress}
				placeholder="Enter server address"
				class="border-primary bg-secondary ring-primary w-full rounded-xl border-2"
			/>
		</div>

		<button
			class="text-dark bg-primary hover:bg-primary/70 rounded-xl px-4 py-2 text-xl font-semibold transition-colors"
			onclick={() => {
				showChecker = true;
			}}>Done</button
		>
	{:else}
		<PageAnimator>
			<div class="flex flex-col items-center gap-6">
				<div class="font-fancy text-3xl font-extrabold">Finished server configuration!</div>
				<CircleCheck size={48} class="text-primary" />
				<button
					class="text-dark bg-primary hover:bg-primary/70 rounded-xl px-4 py-2 text-xl font-semibold transition-colors"
					onclick={() => {
						block = true;
					}}
				>
					Reset
				</button>
			</div>
		</PageAnimator>
	{/if}
</div>
