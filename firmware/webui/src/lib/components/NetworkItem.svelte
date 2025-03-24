<script lang="ts">
	export let ssid: string;
	export let strength: number;
</script>

<div class="bg-secondary flex justify-between rounded rounded-xl p-4">
	<div class="font-fancy font-bold">{ssid}</div>
	<div class="">{strength}</div>
</div>
