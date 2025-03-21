<script lang="ts">
	import PageContainer from '$lib/components/PageContainer.svelte';
	import { onMount } from 'svelte';

	let pageContainer: PageContainer;

	let firstPage: boolean;
	let lastPage: boolean;

	onMount(() => {
		pageContainer.pageState.subscribe((state) => {
			firstPage = state.firstPage;
			lastPage = state.lastPage;
		});
	});
</script>

<PageContainer bind:this={pageContainer} />

<div>
	<button onclick={pageContainer.prev} disabled={firstPage}>Back</button>
	<button onclick={pageContainer.next} disabled={lastPage}>Next</button>
</div>
