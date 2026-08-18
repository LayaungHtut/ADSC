<script lang="ts">
	import { page } from '$app/state';
	import KpiCard from '$lib/components/KpiCard.svelte';
	import { features, formatDec, formatInt, riskColor, riskLabel, riskSummary } from '$lib/data';
	import { goto } from '$app/navigation';
	import { resolve } from '$app/paths';

	const slug = $derived(String(page.params.slug));
	const row = $derived(riskSummary.find((r) => r.kecamatan === slug) ?? null);
	const feat = $derived(row ? (features.find((f) => f.kec_code === row.kec_code) ?? null) : null);

	const comps = $derived(
		row
			? [
					{ name: 'Hazard', value: row.hazard, color: 'var(--color-red-500)' },
					{ name: 'Exposure', value: row.exposure, color: 'var(--color-amber-500)' },
					{ name: 'Vulnerability', value: row.vulnerability, color: 'var(--color-sky-500)' }
				]
			: []
	);

	async function back() {
		await goto(resolve('/locations'));
	}
</script>

<svelte:head>
	<title>{row ? `${row.kecamatan} — FloodResilience Jakarta` : 'Not found'}</title>
</svelte:head>

{#if !row}
	<div class="rounded-xl border border-slate-200 bg-white p-8 text-center">
		<p class="text-lg font-semibold text-slate-700">Kecamatan not found</p>
		<p class="mt-1 text-sm text-slate-500">The area "{slug}" is not in the dataset.</p>
		<button
			onclick={back}
			class="mt-4 rounded-lg bg-sky-600 px-4 py-2 text-sm font-medium text-white"
			>Back to list</button
		>
	</div>
{:else}
	<button onclick={back} class="mb-4 text-sm font-medium text-sky-600 hover:text-sky-700"
		>← All kecamatan</button
	>

	<section class="mb-6 rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
		<div class="flex flex-wrap items-start justify-between gap-4">
			<div>
				<h1 class="text-3xl font-bold tracking-tight">{row.kecamatan}</h1>
				<p class="text-slate-500">{row.kota} · {row.kec_code}</p>
			</div>
			<div class="text-right">
				<p class="text-sm text-slate-500">Composite risk</p>
				<p class="text-4xl font-bold" style="color: {riskColor(row.risk_class)}">
					{row.risk_score.toFixed(1)}
				</p>
				<span
					class="mt-1 inline-block rounded-full px-3 py-1 text-xs font-semibold"
					style="background-color: {riskColor(row.risk_class)}22; color: {riskColor(
						row.risk_class
					)}"
				>
					{riskLabel(row.risk_class)} (class {row.risk_class})
				</span>
			</div>
		</div>
		<div class="mt-6 flex gap-3">
			{#each comps as c (c.name)}
				<div class="flex-1">
					<div class="mb-1 flex justify-between text-xs font-medium text-slate-500">
						<span>{c.name}</span>
						<span>{(c.value * 100).toFixed(1)}</span>
					</div>
					<div class="h-2.5 w-full overflow-hidden rounded-full bg-slate-100">
						<div
							class="h-full rounded-full"
							style="width: {c.value * 100}%; background-color: {c.color}"
						></div>
					</div>
				</div>
			{/each}
		</div>
	</section>

	<section class="grid grid-cols-2 gap-4 lg:grid-cols-4">
		<KpiCard label="Population" value={formatInt(row.pop_est)} sub="modelled (Kontur 2023)" />
		<KpiCard
			label="Mean elevation"
			value={`${row.elev_mean_m.toFixed(1)} m`}
			sub="Copernicus DEM 30m"
		/>
		<KpiCard label="Schools" value={String(row.schools)} sub="point facilities" />
		<KpiCard
			label="Health facilities"
			value={String(row.health_facilities)}
			sub="point facilities"
		/>
	</section>

	{#if feat}
		<section class="mt-8 rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
			<h2 class="mb-4 text-lg font-semibold">Indicators</h2>
			<div class="grid grid-cols-2 gap-6 md:grid-cols-3">
				<div>
					<h3 class="mb-2 text-xs font-semibold tracking-wide text-slate-400 uppercase">
						Rainfall
					</h3>
					<dl class="space-y-2 text-sm">
						<div class="flex justify-between">
							<dt class="text-slate-500">Annual mean</dt>
							<dd class="font-semibold">{formatInt(feat.rain_annual_mean_mm)} mm</dd>
						</div>
						<div class="flex justify-between">
							<dt class="text-slate-500">Last 5 yrs mean</dt>
							<dd class="font-semibold">{formatInt(feat.rain_annual_last5_mean_mm)} mm</dd>
						</div>
						<div class="flex justify-between">
							<dt class="text-slate-500">Extreme months</dt>
							<dd class="font-semibold">{feat.rain_extreme_months}</dd>
						</div>
						<div class="flex justify-between">
							<dt class="text-slate-500">95th pct month</dt>
							<dd class="font-semibold">{formatInt(feat.rain_p95_monthly_mm)} mm</dd>
						</div>
					</dl>
				</div>
				<div>
					<h3 class="mb-2 text-xs font-semibold tracking-wide text-slate-400 uppercase">Terrain</h3>
					<dl class="space-y-2 text-sm">
						<div class="flex justify-between">
							<dt class="text-slate-500">Elevation min/max</dt>
							<dd class="font-semibold">
								{feat.elev_min_m.toFixed(1)} / {feat.elev_max_m.toFixed(1)} m
							</dd>
						</div>
						<div class="flex justify-between">
							<dt class="text-slate-500">Mean slope</dt>
							<dd class="font-semibold">{feat.slope_mean_pct.toFixed(1)} %</dd>
						</div>
						<div class="flex justify-between">
							<dt class="text-slate-500">Area</dt>
							<dd class="font-semibold">{formatDec(feat.area_km2)} km²</dd>
						</div>
						<div class="flex justify-between">
							<dt class="text-slate-500">Pop. density</dt>
							<dd class="font-semibold">{formatInt(feat.pop_density)} /km²</dd>
						</div>
					</dl>
				</div>
				<div>
					<h3 class="mb-2 text-xs font-semibold tracking-wide text-slate-400 uppercase">
						Socio-demographic
					</h3>
					<dl class="space-y-2 text-sm">
						<div class="flex justify-between">
							<dt class="text-slate-500">Children (&lt;15)</dt>
							<dd class="font-semibold">{(feat.child_share * 100).toFixed(1)} %</dd>
						</div>
						<div class="flex justify-between">
							<dt class="text-slate-500">Elderly (65+)</dt>
							<dd class="font-semibold">{(feat.elderly_share * 100).toFixed(1)} %</dd>
						</div>
						<div class="flex justify-between">
							<dt class="text-slate-500">Recent rainfall-flood idx</dt>
							<dd class="font-semibold">{formatDec(feat.rfh_mean)}</dd>
						</div>
					</dl>
				</div>
			</div>
			<p class="mt-4 text-xs text-slate-400">
				Children/elderly shares are kota-level (WorldPop ADM2), shared by all kecamatan in {row.kota}.
			</p>
		</section>
	{/if}

	<section class="mt-8">
		<button
			onclick={async () => {
				await goto(resolve('/map'));
			}}
			class="rounded-lg border border-sky-600 px-4 py-2 text-sm font-medium text-sky-700 hover:bg-sky-50"
		>
			View on risk map →
		</button>
	</section>
{/if}
