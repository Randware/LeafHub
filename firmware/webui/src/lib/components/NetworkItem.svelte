<script lang="ts" module>
	export interface Network {
		ssid: string;
		strength: number;
		type: 'OPEN' | 'WEP' | 'WPA-PSK' | 'WPA2-PSK' | 'WPA/WPA2-PSK' | 'UNKNOWN';
	}
</script>

<script lang="ts">
	import {
		CircleHelp,
		Lock,
		LockOpen,
		Signal,
		SignalHigh,
		SignalLow,
		SignalMedium
	} from '@lucide/svelte';

	export let network: Network;
	export let click: (network: Network) => void;
</script>

<div
	class="bg-primary hover:bg-primary/70 flex items-center justify-between gap-4 rounded-xl p-4 text-left transition-colors"
	onclick={() => {
		click(network);
	}}
>
	<div class="font-fancy text-lg font-bold">{network.ssid}</div>

	<div class="flex items-center gap-2">
		{#if network.type == 'OPEN'}
			<LockOpen size={24} />
		{:else if network.type == 'UNKNOWN'}
			<div class="">
				<CircleHelp size={24} />
			</div>
		{:else}
			<Lock size={24} />
		{/if}

		<div class="grid">
			<div class="text-light" style="grid-row: 1; grid-column: 1;">
				<Signal size={24} />
			</div>

			<div class="text-dark" style="grid-row: 1; grid-column: 1;">
				{#if network.strength >= -55}
					<Signal size={24} />
				{:else if network.strength >= -66}
					<SignalHigh size={24} />
				{:else if network.strength >= -77}
					<SignalMedium size={24} />
				{:else}
					<SignalLow size={24} />
				{/if}
			</div>
		</div>
	</div>
</div>
