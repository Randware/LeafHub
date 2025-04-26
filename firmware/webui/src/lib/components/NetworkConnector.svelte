<script lang="ts">
	import Button from './Button.svelte';
	import type { Network } from './NetworkItem.svelte';

	export let network: Network | null = null;
	export let connect: (ssid: string, password: string) => void;

	let networkName: string = network ? network.ssid : '';
	let networkPassword: string = '';

	$: validInput = /^[\x20-\x7E]{8,63}$/.test(networkPassword) && /^[\s\S]{1,32}$/.test(networkName);

	function connectNetwork() {
		connect(networkName, networkPassword);
	}
</script>

<div class="flex flex-col items-center justify-center gap-8">
	{#if network}
		<div class="font-fancy text-3xl font-extrabold">Connect to "{network.ssid}"</div>
	{:else}
		<div class="font-fancy text-3xl font-extrabold">Add a network</div>

		<div class="flex flex-col items-center gap-2 font-semibold">
			<label for="ssid" class="text-dark text-lg">Name</label>
			<input
				id="ssid"
				type="text"
				bind:value={networkName}
				placeholder="Enter network name"
				class="border-primary bg-secondary ring-primary w-full rounded-xl border-2"
			/>
		</div>
	{/if}
	<div class="flex flex-col items-center gap-2 font-semibold">
		<label for="password" class="text-dark text-lg">Password</label>
		<input
			id="password"
			type="password"
			bind:value={networkPassword}
			placeholder="Enter network password"
			class="border-primary bg-secondary ring-primary w-full rounded-xl border-2"
		/>
	</div>

	<Button onclick={connectNetwork} disabled={!validInput}>Connect</Button>
</div>
