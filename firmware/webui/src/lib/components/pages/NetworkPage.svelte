<script lang="ts">
	// TODO: Add hidden network support

	import NetworkItem from '../NetworkItem.svelte';
	import { type Network } from '../NetworkItem.svelte';
	import { host } from '$lib/store/settings';
	import { Loader, WifiOff } from '@lucide/svelte';
	import { onDestroy, onMount } from 'svelte';

	export let block: boolean;

	let scanning: boolean = false;
	let currentNetworks: Network[] = [];
	let networks: Promise<Network[]> = Promise.resolve(currentNetworks);

	function connectNetwork(network: Network) {
		// TODO: Accept password input and connect to network
	}

	async function fetchNetworks(): Promise<Network[]> {
		const response = await fetch(`http://${host}/device/networks/`);

		if (!response.ok) {
			throw new Error(`Failed to fetch networks: ${response.status}`);
		}

		return await response.json();
	}

	async function startScanning() {
		scanning = true;

		while (scanning) {
			try {
				const newNets = await fetchNetworks();

				newNets.forEach((newNetwork) => {
					const existingNetworkIndex = currentNetworks.findIndex(
						(existing) => existing.ssid === newNetwork.ssid
					);

					if (existingNetworkIndex >= 0) {
						currentNetworks[existingNetworkIndex].strength = newNetwork.strength;
					} else {
						currentNetworks.push(newNetwork);
					}
				});

				currentNetworks.sort((a, b) => b.strength - a.strength);

				networks = Promise.resolve([...currentNetworks]);
			} catch (error) {
				networks = Promise.reject(error);
				scanning = false;
			}
		}
	}

	onMount(async () => {
		await startScanning();
	});

	onDestroy(() => {
		scanning = false;
	});
</script>

<div class="flex h-full flex-col flex-col justify-center gap-6 text-center">
	<div class="font-fancy text-3xl font-extrabold">Network</div>
	<div>First, let's connect your SmartPot to the internet</div>

	<div class="flex min-h-0 flex-col gap-2 overflow-y-auto">
		{#await networks then nets}
			{#each nets as network}
				<NetworkItem {network} click={connectNetwork} />
			{/each}
		{:catch error}
			<div class="flex flex-col items-center justify-center gap-2 sm:flex-row">
				<WifiOff size={32} />
				<div class="font-semibold">Failed scanning for networks</div>
			</div>

			<div class="">{error.message}</div>
		{/await}
	</div>

	{#if scanning}
		<div class="flex flex-col items-center justify-center gap-2 sm:flex-row">
			<div class="animate-spin">
				<Loader size={32} />
			</div>
			<div class="font-semibold">Scanning networks...</div>
		</div>
	{/if}
</div>
