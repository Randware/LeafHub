<script lang="ts">
	import { X } from '@lucide/svelte';
	import { fade, scale } from 'svelte/transition';
	import Button from './Button.svelte';

	export let back: (() => void) | null = null;
</script>

<div
	class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-6"
	onclick={(e) => e.stopPropagation()}
	in:fade={{ duration: 300 }}
>
	<div
		class="bg-medium relative max-h-full w-full max-w-lg
         overflow-x-hidden overflow-y-auto rounded-xl p-12
         text-wrap"
		in:scale={{ duration: 300 }}
	>
		{#if back}
			<!-- The "!" is required to override the internal padding -->
			<Button onclick={back} className="absolute top-3 right-3 !p-2">
				<X size={24} />
			</Button>
		{/if}

		<slot />
	</div>
</div>
