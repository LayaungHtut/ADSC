<script lang="ts">
	import { riskSummary } from '$lib/data';

	const sources = [
		{
			name: 'CHIRPS v2.0 (UCSB/Climate Hazards Center)',
			use: 'Monthly rainfall 1981-2026',
			note: '~5.5 km gridded, satellite + station blend; clipped to Jakarta study box'
		},
		{
			name: 'Copernicus DEM 30m',
			use: 'Elevation and slope',
			note: 'Tiles S06/S07 × E106/E107 via NASA Earthdata'
		},
		{
			name: 'Kontur population grid',
			use: 'Population & density',
			note: 'H3 hexagons, Nov 2023; area-weighted to kecamatan'
		},
		{
			name: 'WorldPop ADM2 (UN adjusted)',
			use: 'Age structure (children/elderly)',
			note: '2020 population counts by 5-year age band'
		},
		{
			name: 'HDX / OSM facility data',
			use: 'Schools & health facilities',
			note: 'Point counts per kecamatan'
		},
		{
			name: 'World Bank / GFDRR rainfall indicators',
			use: 'Recent rainfall-flood index',
			note: '10-day scale, 2022+, kota level'
		},
		{
			name: 'Dartmouth Flood Observatory (DFO)',
			use: 'Historical flood events',
			note: '244 Indonesia events used as context'
		},
		{
			name: 'GeoBoundaries / Alf-Anas admin boundaries',
			use: 'Kecamatan boundaries',
			note: 'Official codes from Indonesian statistics'
		}
	];

	const totals = {
		schools: riskSummary.reduce((s, r) => s + r.schools, 0),
		health: riskSummary.reduce((s, r) => s + r.health_facilities, 0)
	};
</script>

<svelte:head>
	<title>Data — FloodResilience Jakarta</title>
</svelte:head>

<section class="mb-8">
	<h1 class="text-3xl font-bold tracking-tight">Data sources & provenance</h1>
	<p class="mt-2 max-w-3xl text-slate-600">
		All inputs are public, open data. Every download is recorded in a provenance log (file, source,
		timestamp, SHA-256) so every number in this dashboard can be traced back to its origin.
	</p>
</section>

<section class="mb-8 grid grid-cols-2 gap-4 lg:grid-cols-4">
	<div class="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
		<p class="text-sm text-slate-500">Kecamatan</p>
		<p class="mt-1 text-2xl font-bold">{riskSummary.length}</p>
		<p class="text-xs text-slate-400">42 urban areas (2 offshore excluded)</p>
	</div>
	<div class="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
		<p class="text-sm text-slate-500">Rainfall months</p>
		<p class="mt-1 text-2xl font-bold">547</p>
		<p class="text-xs text-slate-400">CHIRPS, 1981-2026</p>
	</div>
	<div class="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
		<p class="text-sm text-slate-500">Schools</p>
		<p class="mt-1 text-2xl font-bold">{totals.schools}</p>
		<p class="text-xs text-slate-400">point facilities</p>
	</div>
	<div class="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
		<p class="text-sm text-slate-500">Health facilities</p>
		<p class="mt-1 text-2xl font-bold">{totals.health}</p>
		<p class="text-xs text-slate-400">point facilities</p>
	</div>
</section>

<section class="mb-8">
	<h2 class="mb-3 text-lg font-semibold">Source catalog</h2>
	<div class="overflow-x-auto rounded-xl border border-slate-200 bg-white shadow-sm">
		<table class="min-w-full divide-y divide-slate-200 text-sm">
			<thead
				class="bg-slate-50 text-left text-xs font-semibold tracking-wide text-slate-500 uppercase"
			>
				<tr>
					<th class="px-4 py-3">Source</th>
					<th class="px-4 py-3">Used for</th>
					<th class="px-4 py-3">Notes</th>
				</tr>
			</thead>
			<tbody class="divide-y divide-slate-100">
				{#each sources as s (s.name)}
					<tr>
						<td class="px-4 py-3 font-medium text-slate-800">{s.name}</td>
						<td class="px-4 py-3 text-slate-600">{s.use}</td>
						<td class="px-4 py-3 text-slate-500">{s.note}</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
</section>

<section class="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
	<h2 class="mb-3 text-lg font-semibold">Quality control</h2>
	<p class="text-sm text-slate-600">
		The processed kecamatan dataset (42 rows × 27 columns) contains zero missing values. A full
		data-quality report covering range checks, completeness and spatial coverage is generated with
		the pipeline. WorldPop age shares and the World Bank rainfall indices are kota-level and
		documented as such in every report and on this dashboard.
	</p>
</section>
