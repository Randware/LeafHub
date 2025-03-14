<script lang="ts">
	import Welcome from '$lib/components/Welcome.svelte';

	const names: string[] = ['Darius', 'Lukas'];
</script>

<div class="m-12 flex flex-col gap-12">
	{#each names as name}
		<Welcome {name} />
	{/each}
</div>
