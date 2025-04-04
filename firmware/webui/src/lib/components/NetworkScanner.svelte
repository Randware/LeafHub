<script lang="ts">
	import NetworkItem from '$lib/components/NetworkItem.svelte';
	import { type Network } from '$lib/components/NetworkItem.svelte';
	import { host } from '$lib/store/settings';
	import { Loader, WifiOff } from '@lucide/svelte';
	import { onDestroy, onMount } from 'svelte';

	export let onSelect: (network: Network) => void;

	let scanning: boolean = false;
	let currentNetworks: Network[] = [];
	let networks: Promise<Network[]> = Promise.resolve(currentNetworks);

	async function fetchNetworks(): Promise<Network[]> {
		const response: Response = await fetch(`http://${host}/device/networks/`);

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

<div class="flex flex-col gap-2 overflow-y-auto">
	{#await networks then nets}
		{#each nets as network}
			<NetworkItem {network} click={onSelect} />
		{/each}
	{:catch error}
		<div class="flex flex-col items-center justify-center gap-2 sm:flex-row">
			<WifiOff size={32} />
			<div class="font-semibold">Failed scanning for networks</div>
		</div>
		<div>{error.message}</div>
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
