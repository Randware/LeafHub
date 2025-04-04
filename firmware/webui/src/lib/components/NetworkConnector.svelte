<script lang="ts">
	import type { Network } from './NetworkItem.svelte';

	export let network: Network | null = null;
	export let connect: (ssid: string, password: string) => void;

	let networkName: string = network ? network.ssid : '';
	let networkPassword: string = '';

	function connectNetwork() {
		let ssid: string = networkName.trim();
		let password: string = networkPassword.trim();

		if (ssid != '' && password != '') {
			connect(ssid, password);
		}
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
				class="border-primary bg-secondary ring-primary w-50 rounded-xl border-2"
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
			class="border-primary bg-secondary ring-primary w-50 rounded-xl border-2"
		/>
	</div>

	<button
		class="text-dark bg-primary hover:bg-primary/70 rounded-xl px-4 py-2 text-xl font-semibold transition-colors"
		onclick={connectNetwork}>Connect</button
	>
</div>
