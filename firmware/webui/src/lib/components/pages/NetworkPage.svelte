<script lang="ts">
	import NetworkItem from '../NetworkItem.svelte';

	export let block: boolean;

	let networks: Array<{ ssid: string; strength: number }> = [
		{ ssid: 'MyNetwork', strength: -70 },
		{ ssid: 'WLAN-Network', strength: -67 }
	];
</script>

<div class="flex flex-col gap-6 text-center">
	<div class="font-fancy text-4xl font-extrabold">Network</div>
	<div class="">First, let's connect your SmartPot to the internet</div>

	<div class="flex flex-1 flex-col gap-2 overflow-y-auto">
		{#each networks as network}
			<NetworkItem ssid={network.ssid} strength={network.strength} />
		{/each}
	</div>
</div>
