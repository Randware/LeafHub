<script lang="ts">
	import { CircleCheck } from '@lucide/svelte';
	import FloatingWindow from '../FloatingWindow.svelte';
	import NetworkConnector from '../NetworkConnector.svelte';
	import type { Network } from '../NetworkItem.svelte';
	import NetworkScanner from '../NetworkScanner.svelte';
	import PageAnimator from '../PageAnimator.svelte';
	import Button from '../Button.svelte';

	export let block: boolean;

	let selectedNetwork: Network | null = null;
	let showConnector: boolean = false;

	function connectNetwork(ssid: string, password: string | null) {
		// TODO: Send network to controller

		selectedNetwork = null;
		block = false;
	}

	function selectNetwork(network: Network) {
		selectedNetwork = network;

		if (network.type == 'OPEN') {
			connectNetwork(network.ssid, null);
		} else {
			showConnector = true;
		}
	}

	function unselectNetwork() {
		selectedNetwork = null;
		showConnector = false;
	}
</script>

<div class="flex h-full flex-col justify-center gap-6 text-center">
	{#if block}
		<div class="font-fancy text-3xl font-extrabold">Network</div>
		<div>Let's connect your SmartPot to the internet</div>

		<Button onclick={() => (showConnector = true)}>Add network</Button>

		<NetworkScanner onSelect={selectNetwork} />

		{#if showConnector}
			<FloatingWindow back={unselectNetwork}>
				<NetworkConnector network={selectedNetwork} connect={connectNetwork} />
			</FloatingWindow>
		{/if}
	{:else}
		<PageAnimator>
			<div class="flex flex-col items-center gap-6">
				<div class="font-fancy text-3xl font-extrabold">Finished network configuration!</div>
				<CircleCheck size={48} class="text-primary" />

				<Button onclick={() => (block = true)}>Reset</Button>
			</div>
		</PageAnimator>
	{/if}
</div>
