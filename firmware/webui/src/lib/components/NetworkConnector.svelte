<script lang="ts">
	export let ssid: string | null = null;
	let networkName: string = ssid ?? '';
	let networkPassword: string;
</script>

<div class="flex flex-col items-center justify-center gap-8">
	{#if ssid}
		<div class="font-fancy text-3xl font-extrabold">Connect to "{ssid}"</div>
	{:else}
		<div class="font-fancy text-3xl font-extrabold">Connect to a network</div>

		<div class="flex flex-col items-center gap-2 font-semibold">
			<label for="ssid" class="text-lg">Name</label>
			<input
				id="ssid"
				type="text"
				bind:value={networkName}
				placeholder="Enter network name"
				class="border-primary bg-secondary text-dark focus:border-primary rounded-xl border-2"
			/>
		</div>
	{/if}

	<div class="flex flex-col items-center gap-2 font-semibold">
		<label for="password" class="text-lg">Password</label>
		<input
			id="password"
			type="text"
			bind:value={networkPassword}
			placeholder="Enter network password"
			class="border-primary bg-secondary rounded-xl border-2"
		/>
	</div>
</div>
