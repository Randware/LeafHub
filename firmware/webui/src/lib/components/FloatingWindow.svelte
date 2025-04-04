<script lang="ts">
	import { X } from '@lucide/svelte';
	import { fade, scale } from 'svelte/transition';

	export let back: (() => void) | null = null;
</script>

<div
	class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-6"
	onclick={(e) => e.stopPropagation()}
	in:fade={{ duration: 300 }}
>
	<div
		class="bg-medium relative h-min max-h-full w-min max-w-full overflow-x-clip overflow-y-auto rounded-xl p-12"
		in:scale={{ duration: 300 }}
	>
		{#if back}
			<button
				class="text-dark bg-primary hover:bg-primary/70 absolute top-3 right-3 rounded-xl p-2 text-xl font-semibold transition-colors"
				onclick={back}
				aria-label="Close modal"
			>
				<X size={24} />
			</button>
		{/if}

		<slot />
	</div>
</div>
