<script lang="ts">
	import { features, formatDec, formatInt, riskColor, riskLabel, riskSummary } from '$lib/data';
	import type { FeatureRow } from '$lib/types';
	import { goto } from '$app/navigation';
	import { resolve } from '$app/paths';

	let selected = $state(riskSummary[0]?.kec_code ?? '');
	const selectedRow = $derived(riskSummary.find((r) => r.kec_code === selected) ?? null);
	const feat = $derived(
		selectedRow
			? (features.find((f: FeatureRow) => f.kec_code === selectedRow.kec_code) ?? null)
			: null
	);

	function band(value: number): { color: string; label: string } {
		if (value >= 0.6) return { color: '#ef4444', label: 'High' };
		if (value >= 0.4) return { color: '#f59e0b', label: 'Moderate' };
		return { color: '#10b981', label: 'Low' };
	}

	const contributing = $derived.by(() => {
		if (!feat) return [];
		const items: { name: string; value: number; direction: string; unit: string }[] = [];
		items.push({
			name: 'Annual rainfall',
			value: feat.rain_annual_mean_mm,
			direction: 'higher',
			unit: ' mm/yr'
		});
		items.push({
			name: 'Extreme-rainfall months',
			value: feat.rain_extreme_months,
			direction: 'more',
			unit: ' months'
		});
		items.push({ name: 'Mean elevation', value: feat.elev_mean_m, direction: 'lower', unit: ' m' });
		items.push({ name: 'Population', value: feat.pop_est, direction: 'larger', unit: ' persons' });
		items.push({
			name: 'Population density',
			value: feat.pop_density,
			direction: 'higher',
			unit: ' /km²'
		});
		items.push({ name: 'Schools', value: feat.schools, direction: 'more', unit: '' });
		items.push({
			name: 'Health facilities',
			value: feat.health_facilities,
			direction: 'more',
			unit: ''
		});
		items.push({
			name: 'Children share',
			value: feat.child_share * 100,
			direction: 'higher',
			unit: ' %'
		});
		items.push({
			name: 'Elderly share',
			value: feat.elderly_share * 100,
			direction: 'higher',
			unit: ' %'
		});
		items.push({
			name: 'Recent rainfall-flood index',
			value: feat.rfh_mean,
			direction: 'higher',
			unit: ''
		});
		return items.sort((a, b) => b.value - a.value).slice(0, 5);
	});
</script>

<svelte:head>
	<title>Risk explorer — FloodResilience Jakarta</title>
</svelte:head>

<section class="mb-6">
	<h1 class="text-3xl font-bold tracking-tight">Risk explorer</h1>
	<p class="mt-2 max-w-3xl text-slate-600">
		Select a kecamatan to decompose its flood risk into hazard, exposure and vulnerability, and see
		which indicators drive the score.
	</p>
</section>

<section class="mb-6 rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
	<label for="kecamatan-select" class="mb-1 block text-sm font-medium text-slate-600"
		>Kecamatan</label
	>
	<select
		id="kecamatan-select"
		bind:value={selected}
		class="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm sm:max-w-sm"
	>
		{#each riskSummary as r (r.kec_code)}
			<option value={r.kec_code}>{r.kecamatan} — {r.kota}</option>
		{/each}
	</select>
</section>

{#if selectedRow}
	<section class="mb-6 rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
		<div class="flex flex-wrap items-start justify-between gap-4">
			<div>
				<h2 class="text-2xl font-bold">{selectedRow.kecamatan}</h2>
				<p class="text-sm text-slate-500">{selectedRow.kota} · {selectedRow.kec_code}</p>
			</div>
			<div class="text-right">
				<p class="text-sm text-slate-500">Overall risk</p>
				<p class="text-4xl font-bold" style="color: {riskColor(selectedRow.risk_class)}">
					{selectedRow.risk_score.toFixed(1)}
					<span class="text-base font-normal text-slate-400">/ 100</span>
				</p>
				<span
					class="mt-1 inline-block rounded-full px-3 py-1 text-xs font-semibold"
					style="background-color: {riskColor(selectedRow.risk_class)}22; color: {riskColor(
						selectedRow.risk_class
					)}"
				>
					{riskLabel(selectedRow.risk_class)} (class {selectedRow.risk_class})
				</span>
			</div>
		</div>

		<div class="mt-6 grid gap-4 md:grid-cols-3">
			{#each [{ name: 'Hazard', value: selectedRow.hazard, hint: 'Rainfall, terrain and recent rainfall-flood conditions' }, { name: 'Exposure', value: selectedRow.exposure, hint: 'People, density and critical facilities present' }, { name: 'Vulnerability', value: selectedRow.vulnerability, hint: 'Age composition (children & elderly share)' }] as c (c.name)}
				<div class="rounded-lg border border-slate-100 p-4">
					<div class="mb-1 flex items-baseline justify-between">
						<span class="text-sm font-semibold">{c.name}</span>
						<span class="text-lg font-bold" style="color: {band(c.value).color}"
							>{(c.value * 100).toFixed(0)}</span
						>
					</div>
					<div class="h-2 w-full overflow-hidden rounded-full bg-slate-100">
						<div
							class="h-full rounded-full"
							style="width: {c.value * 100}%; background-color: {band(c.value).color}"
						></div>
					</div>
					<p class="mt-2 text-xs text-slate-500">{c.hint}</p>
				</div>
			{/each}
		</div>
	</section>

	<section class="mb-6 grid grid-cols-2 gap-4 lg:grid-cols-4">
		<div class="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
			<p class="text-sm text-slate-500">Population</p>
			<p class="mt-1 text-2xl font-bold">{formatInt(selectedRow.pop_est)}</p>
			<p class="text-xs text-slate-400">modelled (Kontur 2023)</p>
		</div>
		<div class="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
			<p class="text-sm text-slate-500">Mean elevation</p>
			<p class="mt-1 text-2xl font-bold">{selectedRow.elev_mean_m.toFixed(1)} m</p>
			<p class="text-xs text-slate-400">Copernicus DEM 30m</p>
		</div>
		<div class="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
			<p class="text-sm text-slate-500">Schools / health</p>
			<p class="mt-1 text-2xl font-bold">{selectedRow.schools} / {selectedRow.health_facilities}</p>
			<p class="text-xs text-slate-400">point facilities (HDX/OSM)</p>
		</div>
		<div class="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
			<p class="text-sm text-slate-500">Annual rainfall</p>
			<p class="mt-1 text-2xl font-bold">{feat ? formatInt(feat.rain_annual_mean_mm) : '—'} mm</p>
			<p class="text-xs text-slate-400">CHIRPS 1981-2026 mean</p>
		</div>
	</section>

	<section class="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
		<h2 class="mb-2 text-lg font-semibold">Why is this area at this risk level?</h2>
		<p class="mb-4 text-sm text-slate-600">
			The five indicators with the highest observed values for this kecamatan, compared across all
			42 areas:
		</p>
		<ul class="divide-y divide-slate-100">
			{#each contributing as c (c.name)}
				<li class="flex items-center justify-between gap-4 py-2.5 text-sm">
					<span class="text-slate-600">{c.name}</span>
					<span class="font-semibold text-slate-800">{formatDec(c.value)}{c.unit}</span>
				</li>
			{/each}
		</ul>
		<p class="mt-4 text-xs text-slate-400">
			Higher values of these indicators raise the corresponding risk component. This list is
			descriptive, not a claim that any single factor causes flooding.
		</p>
	</section>

	<section class="mt-6">
		<button
			onclick={async () => {
				await goto(resolve(`/locations/${encodeURIComponent(selectedRow.kecamatan)}`));
			}}
			class="rounded-lg bg-sky-600 px-4 py-2 text-sm font-medium text-white hover:bg-sky-700"
		>
			Full profile →
		</button>
	</section>
{/if}
