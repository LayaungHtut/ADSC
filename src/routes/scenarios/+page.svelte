<script lang="ts">
	import { DEFAULT_SCENARIO, runScenario, type ScenarioInputs } from '$lib/scenario';
	import { riskColor } from '$lib/data';

	let rainfall = $state(DEFAULT_SCENARIO.rainfall);
	let population = $state(DEFAULT_SCENARIO.population);
	let infrastructure = $state(DEFAULT_SCENARIO.infrastructure);

	const inputs = $derived.by(() => ({ rainfall, population, infrastructure }) as ScenarioInputs);
	const results = $derived(runScenario(inputs));
	const sorted = $derived([...results].sort((a, b) => b.scenario_risk - a.scenario_risk));
	const top = $derived(sorted.slice(0, 10));
	const totalDelta = $derived(results.reduce((s, r) => s + r.risk_delta, 0));

	function pct(x: number): string {
		return `${x >= 0 ? '+' : ''}${(x * 100).toFixed(0)}%`;
	}

	function classShiftLabel(r: { baseline_class: number; scenario_class: number }): string {
		if (r.scenario_class > r.baseline_class) return `↑ ${r.baseline_class} → ${r.scenario_class}`;
		if (r.scenario_class < r.baseline_class) return `↓ ${r.baseline_class} → ${r.scenario_class}`;
		return `= class ${r.baseline_class}`;
	}
</script>

<svelte:head>
	<title>Scenarios — FloodResilience Jakarta</title>
</svelte:head>

<section class="mb-6">
	<h1 class="text-3xl font-bold tracking-tight">Scenario explorer</h1>
	<p class="mt-2 max-w-3xl text-slate-600">
		Explore how changes to rainfall, population and infrastructure resilience would re-rank flood
		risk across Jakarta's 42 kecamatan.
	</p>
</section>

<div class="mb-6 rounded-xl border border-amber-200 bg-amber-50 p-4 text-sm text-amber-900">
	<p class="font-semibold">Illustrative scenario — not a forecast.</p>
	<p class="mt-1">
		Scenarios perturb the observed indicators and re-run the exact documented risk model. They show
		relative re-prioritization under stated assumptions; they do not predict real future flooding,
		rainfall or growth.
	</p>
</div>

<section class="mb-8 grid gap-6 lg:grid-cols-3">
	<div class="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
		<div class="mb-1 flex items-baseline justify-between">
			<label for="rain-slider" class="text-sm font-medium text-slate-600">Rainfall</label>
			<span class="text-sm font-bold text-sky-700">{pct(rainfall)}</span>
		</div>
		<input
			id="rain-slider"
			type="range"
			min="-0.2"
			max="0.3"
			step="0.01"
			bind:value={rainfall}
			class="w-full accent-sky-600"
		/>
		<p class="mt-1 text-xs text-slate-400">
			Change applied to annual rainfall indicators and recent rainfall-flood index.
		</p>
	</div>

	<div class="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
		<div class="mb-1 flex items-baseline justify-between">
			<label for="pop-slider" class="text-sm font-medium text-slate-600">Population exposure</label>
			<span class="text-sm font-bold text-sky-700">{pct(population)}</span>
		</div>
		<input
			id="pop-slider"
			type="range"
			min="-0.2"
			max="0.3"
			step="0.01"
			bind:value={population}
			class="w-full accent-sky-600"
		/>
		<p class="mt-1 text-xs text-slate-400">
			Change applied to modelled population count and density.
		</p>
	</div>

	<div class="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
		<div class="mb-1 flex items-baseline justify-between">
			<label for="infra-slider" class="text-sm font-medium text-slate-600"
				>Infrastructure resilience</label
			>
			<span class="text-sm font-bold text-sky-700">-{Math.round(infrastructure * 100)}%</span>
		</div>
		<input
			id="infra-slider"
			type="range"
			min="0"
			max="0.5"
			step="0.01"
			bind:value={infrastructure}
			class="w-full accent-sky-600"
		/>
		<p class="mt-1 text-xs text-slate-400">
			Reduces the exposure contribution of schools and health facilities (e.g. flood-proofing).
		</p>
	</div>
</section>

<section class="mb-8 grid grid-cols-2 gap-4 lg:grid-cols-4">
	<div class="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
		<p class="text-sm text-slate-500">Areas in top class</p>
		<p class="mt-1 text-2xl font-bold">{results.filter((r) => r.scenario_class === 5).length}</p>
		<p class="text-xs text-slate-400">class 5 (highest) under scenario</p>
	</div>
	<div class="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
		<p class="text-sm text-slate-500">Mean risk change</p>
		<p class="mt-1 text-2xl font-bold" style="color: {totalDelta >= 0 ? '#dc2626' : '#059669'}">
			{totalDelta >= 0 ? '+' : ''}{totalDelta.toFixed(1)}
		</p>
		<p class="text-xs text-slate-400">0-100 scale, across all areas</p>
	</div>
	<div class="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
		<p class="text-sm text-slate-500">Highest scenario risk</p>
		<p class="mt-1 text-2xl font-bold">{top[0]?.scenario_risk.toFixed(1) ?? '—'}</p>
		<p class="text-xs text-slate-400">{top[0]?.kecamatan ?? ''}</p>
	</div>
	<div class="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
		<p class="text-sm text-slate-500">Class changed</p>
		<p class="mt-1 text-2xl font-bold">
			{results.filter((r) => r.scenario_class !== r.baseline_class).length}
		</p>
		<p class="text-xs text-slate-400">areas shifting risk class</p>
	</div>
</section>

<section class="mb-8 rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
	<h2 class="mb-4 text-lg font-semibold">Top-10 under scenario vs baseline</h2>
	<div class="overflow-x-auto">
		<table class="min-w-full divide-y divide-slate-200 text-sm">
			<thead class="text-left text-xs font-semibold tracking-wide text-slate-500 uppercase">
				<tr>
					<th class="px-4 py-3">Kecamatan</th>
					<th class="px-4 py-3">Baseline risk</th>
					<th class="px-4 py-3">Scenario risk</th>
					<th class="px-4 py-3">Change</th>
					<th class="px-4 py-3">Risk class</th>
				</tr>
			</thead>
			<tbody class="divide-y divide-slate-100">
				{#each top as r (r.kec_code)}
					<tr>
						<td class="px-4 py-3 font-medium text-slate-800">{r.kecamatan}</td>
						<td class="px-4 py-3 text-slate-600">{r.baseline_risk.toFixed(1)}</td>
						<td class="px-4 py-3 font-semibold text-slate-800">{r.scenario_risk.toFixed(1)}</td>
						<td class="px-4 py-3" style="color: {r.risk_delta >= 0 ? '#dc2626' : '#059669'}">
							{r.risk_delta >= 0 ? '+' : ''}{r.risk_delta.toFixed(1)}
						</td>
						<td class="px-4 py-3">
							<span
								class="inline-flex items-center gap-1.5 rounded-full px-2 py-0.5 text-xs font-medium"
								style="background-color: {riskColor(r.scenario_class)}33; color: {riskColor(
									r.scenario_class
								)}"
							>
								{classShiftLabel(r)}
							</span>
						</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
</section>

<section class="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
	<h2 class="mb-2 text-lg font-semibold">How this is calculated</h2>
	<p class="text-sm leading-relaxed text-slate-600">
		Each scenario perturbs the raw indicators, re-normalizes them with min-max scaling across the 42
		kecamatan, and recomputes the documented risk model:
	</p>
	<ul class="mt-3 list-disc space-y-1 pl-5 text-sm text-slate-600">
		<li>
			Rainfall change scales the CHIRPS annual-mean, 95th-percentile and World Bank rainfall-flood
			indicators.
		</li>
		<li>Population change scales Kontur population and recomputes density from area.</li>
		<li>Infrastructure resilience reduces the school and health-facility exposure terms.</li>
		<li>Risk = 0.40 · Hazard + 0.35 · Exposure + 0.25 · Vulnerability, then quintile classes.</li>
	</ul>
	<p class="mt-3 text-xs text-slate-400">
		This mirrors <code>floodresilience/features/risk_index.py</code>. Results are relative, not
		predictions.
	</p>
</section>
