<script lang="ts">
	let {
		label,
		value,
		sub,
		icon = '#'
	}: { label: string; value: string; sub?: string; icon?: string } = $props();
</script>

<div class="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
	<div class="flex items-center justify-between gap-2">
		<p class="text-sm font-medium text-slate-500">{label}</p>
		{#if icon !== '#'}<span class="text-slate-300">{icon}</span>{/if}
	</div>
	<p class="mt-2 text-3xl font-bold tracking-tight text-slate-900">{value}</p>
	{#if sub}<p class="mt-1 text-sm text-slate-500">{sub}</p>{/if}
</div>
