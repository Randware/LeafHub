<script lang="ts">
	import { advancedSetup } from '$lib/store/settings';

	export let block: boolean;
</script>

<div class="flex flex-col gap-6 text-center">
	<div class="font-fancy text-3xl font-extrabold">Welcome!</div>

	<div class="text-bold">
		This page will help you set up your new <strong>LeafHub SmartPot</strong>
	</div>

	<div class="text-bold">
		Click <strong>Next</strong> to get started
	</div>

	<div class="flex items-center justify-center gap-2 font-semibold">
		<label for="advanced" class="text-dark text-lg">Advanced setup</label>

		<input
			id="advanced"
			type="checkbox"
			bind:checked={$advancedSetup}
			class="text-primary h-6 w-6 rounded-lg ring-0 ring-offset-0 transition-[background-color,border-color]"
		/>
	</div>
</div>
