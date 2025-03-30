<script lang="ts">
	// TODO: Add hidden network support
	import NetworkConnector from '../NetworkConnector.svelte';
	import type { Network } from '../NetworkItem.svelte';
	import NetworkScanner from '../NetworkScanner.svelte';

	export let block: boolean;

	let selectedNetwork: Network | null = null;

	function selectNetwork(network: Network) {
		selectedNetwork = network;
	}
</script>

<div class="flex h-full flex-col flex-col justify-center gap-6 text-center">
	{#if !selectedNetwork}
		<div class="font-fancy text-3xl font-extrabold">Network</div>
		<div>Let's connect your SmartPot to the internet</div>
		<NetworkScanner onSelect={selectNetwork} />
	{:else}
		<NetworkConnector ssid={selectedNetwork.ssid} />
	{/if}
</div>
