<script lang="ts">
	export let disabled: boolean = false;
	export let onclick: () => void;
	export let className: string = '';
</script>

<button
	class="text-dark {disabled
		? 'bg-gray-400/80'
		: 'bg-primary hover:bg-primary/70'} rounded-xl px-4 py-2 text-xl font-semibold transition-colors {className}"
	{onclick}
	{disabled}
>
	<slot />
</button>
