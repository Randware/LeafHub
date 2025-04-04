<script lang="ts">
	// TODO: Add hidden network support
	// FIX: Change NetworkConnector to pop up window
	import NetworkConnector from '../NetworkConnector.svelte';
	import type { Network } from '../NetworkItem.svelte';
	import NetworkScanner from '../NetworkScanner.svelte';
	import { ArrowBigLeft } from '@lucide/svelte';

	export let block: boolean;

	let selectedNetwork: Network | null = null;

	function selectNetwork(network: Network) {
		selectedNetwork = network;
	}

	function unselectNetwork() {
		selectedNetwork = null;
	}
</script>

<div class="flex h-full flex-col justify-center gap-6 text-center">
	{#if !selectedNetwork}
		<div class="font-fancy text-3xl font-extrabold">Network</div>
		<div>Let's connect your SmartPot to the internet</div>
		<NetworkScanner onSelect={selectNetwork} />
	{:else}
		<div class="flex gap-4">
			<!-- FIX: This is ugly, fix it -->
			<button class="bg-primary rounded-xl p-4" onclick={unselectNetwork}>
				<ArrowBigLeft />
			</button>

			<NetworkConnector />
		</div>
	{/if}
</div>
