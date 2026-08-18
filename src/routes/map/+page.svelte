<script lang="ts">
	import RiskMap from '$lib/components/RiskMap.svelte';
	import { byCode } from '$lib/data';
	import { goto } from '$app/navigation';
	import { resolve } from '$app/paths';

	let selected = $state<string | null>(null);

	function onselect(code: string) {
		selected = code;
	}

	const detail = $derived(selected ? (byCode.get(selected) ?? null) : null);
</script>

<svelte:head>
	<title>Risk map — FloodResilience Yangon</title>
</svelte:head>

<section class="mb-6">
	<h1 class="text-3xl font-bold tracking-tight">Interactive risk map</h1>
	<p class="mt-2 max-w-3xl text-slate-600">
		Choropleth of the composite flood-risk index across Yangon Region's 45 urban townships. Click
		any area to inspect its hazard, exposure and vulnerability components.
	</p>
</section>

<section class="mb-6 grid gap-6 lg:grid-cols-3">
	<div class="lg:col-span-2">
		<RiskMap {selected} {onselect} height="65vh" />
	</div>
	<aside class="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
		{#if detail}
			<div>
				<h2 class="text-xl font-semibold">{detail.township}</h2>
				<p class="text-sm text-slate-500">{detail.district}</p>
				<dl class="mt-4 space-y-3 text-sm">
					<div>
						<dt class="text-slate-500">Composite risk</dt>
						<dd class="text-2xl font-bold" style="color: {selected ? '' : ''}">
							{detail.risk_score.toFixed(1)}
							<span class="ml-1 align-middle text-xs font-medium text-slate-400">/ 100</span>
						</dd>
					</div>
					<div>
						<dt class="text-slate-500">Hazard</dt>
						<dd class="font-semibold">{(detail.hazard * 100).toFixed(1)}</dd>
					</div>
					<div>
						<dt class="text-slate-500">Exposure</dt>
						<dd class="font-semibold">{(detail.exposure * 100).toFixed(1)}</dd>
					</div>
					<div>
						<dt class="text-slate-500">Vulnerability</dt>
						<dd class="font-semibold">{(detail.vulnerability * 100).toFixed(1)}</dd>
					</div>
					<div class="border-t border-slate-100 pt-3">
						<dt class="text-slate-500">Population</dt>
						<dd class="font-semibold">
							{detail.pop_est.toLocaleString('en-US', { maximumFractionDigits: 0 })}
						</dd>
					</div>
					<div>
						<dt class="text-slate-500">Mean elevation</dt>
						<dd class="font-semibold">{detail.elev_mean_m.toFixed(1)} m</dd>
					</div>
					<div>
						<dt class="text-slate-500">Schools / Health facilities</dt>
						<dd class="font-semibold">{detail.schools} / {detail.health_facilities}</dd>
					</div>
				</dl>
				<button
					onclick={async () => {
						await goto(resolve(`/locations/${encodeURIComponent(detail.township)}`));
					}}
					class="mt-5 w-full rounded-lg bg-sky-600 px-4 py-2 text-sm font-medium text-white hover:bg-sky-700"
				>
					Full profile →
				</button>
			</div>
		{:else}
			<p class="text-sm text-slate-500">Select a township on the map to see its risk profile.</p>
		{/if}
	</aside>
</section>
