<script lang="ts">
	import Header from '$lib/components/Header.svelte';
	import PageContainer from '$lib/components/PageContainer.svelte';
</script>

<div class="bg-light flex h-[100vh] w-[100vw] items-center justify-center p-6">
	<div class="bg-secondary flex h-full w-full flex-col gap-6 rounded-xl p-6">
		<Header />

		<PageContainer />
	</div>
</div>
