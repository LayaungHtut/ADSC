<script lang="ts">
	const steps = [
		{
			n: 1,
			title: 'Hazard (40%)',
			body: 'Physical likelihood of flooding from rainfall and terrain.',
			formula:
				'Hazard = 0.35·(1 − elevation) + 0.30·rainfall + 0.20·extreme months + 0.15·recent intensity'
		},
		{
			n: 2,
			title: 'Exposure (35%)',
			body: 'People and critical services present in a flood-prone area.',
			formula: 'Exposure = 0.35·population + 0.25·density + 0.20·schools + 0.20·health facilities'
		},
		{
			n: 3,
			title: 'Vulnerability (25%)',
			body: 'Capacity of residents to cope, proxied by age composition.',
			formula: 'Vulnerability = 0.60·children (<15) + 0.40·elderly (65+)'
		}
	];

	const weights = [
		['Default', '0.40 / 0.35 / 0.25'],
		['Hazard-priority', '0.50 / 0.30 / 0.20'],
		['Exposure-priority', '0.30 / 0.50 / 0.20'],
		['Vulnerability-priority', '0.30 / 0.30 / 0.40'],
		['Balanced', '0.34 / 0.33 / 0.33']
	];
</script>

<svelte:head>
	<title>Methodology — FloodResilience Jakarta</title>
</svelte:head>

<section class="mb-8">
	<h1 class="text-3xl font-bold tracking-tight">Methodology</h1>
	<p class="mt-2 max-w-3xl text-slate-600">
		How the composite flood-risk index is computed. Every component is normalized to a 0-1 scale
		using min-max scaling across the 42 urban kecamatan, then combined with documented weights.
		Scores are rescaled to 0-100 and assigned to quintile classes (1 = lowest .. 5 = highest).
	</p>
</section>

<section class="mb-8 grid gap-4 md:grid-cols-3">
	{#each steps as s (s.n)}
		<div class="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
			<div
				class="mb-3 flex h-9 w-9 items-center justify-center rounded-lg bg-sky-600 text-sm font-bold text-white"
			>
				{s.n}
			</div>
			<h2 class="font-semibold">{s.title}</h2>
			<p class="mt-1 text-sm text-slate-600">{s.body}</p>
			<p class="mt-3 text-xs leading-relaxed text-slate-500">{s.formula}</p>
		</div>
	{/each}
</section>

<section class="mb-8 rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
	<h2 class="mb-3 text-lg font-semibold">Final index</h2>
	<div class="overflow-x-auto">
		<table class="w-full text-sm">
			<tbody>
				<tr class="border-b border-slate-100">
					<td class="py-2 font-medium">Composite risk</td>
					<td class="py-2 text-slate-600">
						Risk = 0.40 · Hazard + 0.35 · Exposure + 0.25 · Vulnerability → normalized 0-100
					</td>
				</tr>
				<tr class="border-b border-slate-100">
					<td class="py-2 font-medium">Hazard inputs</td>
					<td class="py-2 text-slate-600">
						Mean elevation (inverse), annual rainfall, count of extreme-rainfall months (≥ 95th
						percentile), recent rainfall-flood index (World Bank/GFDRR)
					</td>
				</tr>
				<tr class="border-b border-slate-100">
					<td class="py-2 font-medium">Exposure inputs</td>
					<td class="py-2 text-slate-600">
						Population, population density, schools, health facilities (all area-weighted / point
						counts)
					</td>
				</tr>
				<tr>
					<td class="py-2 font-medium">Vulnerability inputs</td>
					<td class="py-2 text-slate-600">
						Share of children under 15 and elderly over 65 (kota-level from WorldPop ADM2)
					</td>
				</tr>
			</tbody>
		</table>
	</div>
</section>

<section class="mb-8 rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
	<h2 class="mb-3 text-lg font-semibold">Sensitivity analysis</h2>
	<p class="mb-4 text-sm text-slate-600">
		Rankings were recomputed under five alternative weighting schemes. The mean change in rank
		position is small, indicating the ranking is not driven by a single arbitrary weighting.
	</p>
	<div class="overflow-x-auto">
		<table class="w-full text-sm">
			<thead class="text-left text-xs text-slate-400 uppercase">
				<tr>
					<th class="py-2">Scheme</th>
					<th class="py-2">Weights (Hazard / Exposure / Vulnerability)</th>
				</tr>
			</thead>
			<tbody>
				{#each weights as w (w[0])}
					<tr class="border-t border-slate-100">
						<td class="py-2 font-medium">{w[0]}</td>
						<td class="py-2 text-slate-600">{w[1]}</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
</section>

<section class="rounded-xl border border-amber-200 bg-amber-50 p-5">
	<h2 class="mb-2 text-lg font-semibold text-amber-900">Limitations</h2>
	<ul class="list-disc space-y-1.5 pl-5 text-sm text-amber-800">
		<li>
			Vulnerability is computed at kota level, so all kecamatan in the same city share an identical
			score.
		</li>
		<li>CHIRPS rainfall has ~5.5 km resolution — coarse for intra-district differences.</li>
		<li>
			No district-level poverty or socioeconomic data was available from open sources (BPS
			restricted access).
		</li>
		<li>
			Observed flood-extent polygons are not available at kecamatan level; hazard relies on rainfall
			+ elevation proxies.
		</li>
		<li>
			The index is a relative ranking tool for prioritization, not an absolute measure of flood
			danger.
		</li>
	</ul>
</section>
