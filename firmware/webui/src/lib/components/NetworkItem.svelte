<script lang="ts" module>
	export interface Network {
		ssid: string;
		strength: number;
	}
</script>

<script lang="ts">
	import { Tally1, Tally2, Tally3, Tally4 } from '@lucide/svelte';

	export let network: Network;
	export let click: (network: Network) => void;
</script>

<div
	class="bg-secondary bg-primary flex items-center justify-between gap-4 rounded rounded-xl p-4 text-left transition-colors"
	onclick={() => {
		click(network);
	}}
>
	<div class="font-fancy text-lg font-bold">{network.ssid}</div>
	<div class="grid">
		<div class="text-light" style="grid-row: 1; grid-column: 1;">
			<Tally4 size={32} />
		</div>

		<div class="text-dark" style="grid-row: 1; grid-column: 1;">
			{#if network.strength >= -55}
				<Tally4 size={32} />
			{:else if network.strength >= -66}
				<Tally3 size={32} />
			{:else if network.strength >= -77}
				<Tally2 size={32} />
			{:else}
				<Tally1 size={32} />
			{/if}
		</div>
	</div>
</div>
