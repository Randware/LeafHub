<script lang="ts">
	import { fly } from 'svelte/transition';
</script>

<div in:fly={{ x: 10, duration: 500, opacity: 0 }}>
	<slot />
</div>
