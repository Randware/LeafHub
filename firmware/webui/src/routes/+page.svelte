<script lang="ts">
	import { host } from '$lib/store/settings';

	interface Network {
		ssid: string;
		strength: number;
	}

	let networks: Promise<Network[]> | null = null;

	async function fetchNetworks(): Promise<Network[]> {
		const response = await fetch(`http://${host}/device/networks/`);

		if (!response.ok) {
			throw new Error(`Failed to fetch networks: ${response.status}`);
		}

		return response.json();
	}

	function scanNetworks() {
		networks = fetchNetworks();
	}
</script>

<div class="m-12 flex flex-col gap-12">
	<button onclick={scanNetworks} class="rounded bg-blue-500 px-4 py-2 text-white">
		Scan for Networks
	</button>

	{#if networks}
		{#await networks}
			<p>Loading...</p>
		{:then networks}
			{#if networks.length > 0}
				{#each networks as network (network.ssid)}
					<div>
						<strong>{network.ssid}</strong> - Signal Strength: {network.strength}
					</div>
				{/each}
			{:else}
				<p>No networks found.</p>
			{/if}
		{:catch error}
			<p>Error: {error.message}</p>
		{/await}
	{/if}
</div>
