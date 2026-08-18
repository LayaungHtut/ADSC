<script lang="ts">
	import {
		annualSeries,
		formatDec,
		formatInt,
		monthlyClimatology,
		rainfallRange,
		riskColor,
		riskSummary,
		topRisk,
		totalPop,
		meanRisk,
		byCode
	} from '$lib/data';
	import KpiCard from '$lib/components/KpiCard.svelte';
	import BarChart from '$lib/components/BarChart.svelte';
	import RiskTable from '$lib/components/RiskTable.svelte';
	import { goto } from '$app/navigation';
	import { resolve } from '$app/paths';

	const climate = monthlyClimatology();
	const annual = annualSeries();
	const rain = rainfallRange();
	const monthNames = [
		'Jan',
		'Feb',
		'Mar',
		'Apr',
		'May',
		'Jun',
		'Jul',
		'Aug',
		'Sep',
		'Oct',
		'Nov',
		'Dec'
	];
	const maxClimate = Math.max(...climate.map((c) => c.mean));

	const highClassPop = riskSummary
		.filter((r) => r.risk_class === 5)
		.reduce((s, r) => s + r.pop_est, 0);

	const highClassPct = totalPop > 0 ? ((highClassPop / totalPop) * 100).toFixed(1) : 'n/a';

	const top = topRisk[0];
	const highest = top ? (byCode.get(top.tship_code) ?? null) : null;
</script>

<svelte:head>
	<title>Dashboard — FloodResilience Yangon</title>
</svelte:head>

<section class="mb-8">
	<h1 class="text-3xl font-bold tracking-tight">Flood risk intelligence for Yangon</h1>
	<p class="mt-2 max-w-3xl text-slate-600">
		A data-driven assessment of flood risk across Yangon Region's 45 urban townships, combining
		rainfall, elevation, population and critical infrastructure. Built entirely from public,
		traceable data.
	</p>
</section>

<section class="grid grid-cols-2 gap-4 lg:grid-cols-4">
	<KpiCard
		label="Townships assessed"
		value={String(riskSummary.length)}
		sub="45 townships of Yangon Region"
	/>
	<KpiCard label="Population" value={formatInt(totalPop)} sub="modelled residents (Kontur, 2023)" />
	<KpiCard label="Mean risk score" value={formatDec(meanRisk)} sub="0-100 composite index" />
	<KpiCard
		label="In highest risk class"
		value={formatInt(highClassPop)}
		sub={`~${highClassPct}% of residents (class 5)`}
	/>
</section>

<div class="mt-8 grid gap-6 lg:grid-cols-2">
	<section class="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
		<h2 class="mb-4 text-lg font-semibold">Top-10 highest risk townships</h2>
		<BarChart
			bars={topRisk.map((r) => ({
				label: r.township,
				value: r.risk_score,
				color: riskColor(r.risk_class)
			}))}
		/>
	</section>

	<section class="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
		<h2 class="mb-4 text-lg font-semibold">Rainfall seasonality ({rain.start}-{rain.end})</h2>
		<div class="flex h-48 items-end gap-1.5">
			{#each climate as c (c.month)}
				<div class="group relative flex-1">
					<div
						class="w-full rounded-t-sm bg-sky-500/80 transition-colors group-hover:bg-sky-600"
						style="height: {(c.mean / maxClimate) * 100}%"
					></div>
					<div class="mt-1 text-center text-[10px] text-slate-400">{monthNames[c.month - 1]}</div>
				</div>
			{/each}
		</div>
		<p class="mt-2 text-xs text-slate-500">
			Mean monthly rainfall (mm) across the Yangon study area.
		</p>
	</section>
</div>

<section class="mt-8 rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
	<h2 class="mb-4 text-lg font-semibold">Annual rainfall and documented flood years</h2>
	<div class="relative h-56">
		<svg viewBox="0 0 800 220" preserveAspectRatio="none" class="h-full w-full">
			{#each annual as a (a.year)}
				<rect
					x={(a.year - annual[0].year) * (800 / annual.length) + 1}
					y={220 - (a.rain / 3500) * 200}
					width={800 / annual.length - 2}
					height={(a.rain / 3500) * 200}
					fill={a.flood ? 'var(--color-red-500)' : 'var(--color-sky-300)'}
					rx="1"
				>
					<title>{a.year}: {Math.round(a.rain)} mm{a.flood ? ' (documented flood year)' : ''}</title
					>
				</rect>
			{/each}
		</svg>
	</div>
	<div class="mt-2 flex items-center gap-4 text-xs text-slate-500">
		<span class="inline-flex items-center gap-1"
			><span class="h-2.5 w-2.5 rounded-sm bg-sky-300"></span> Annual rainfall (mm)</span
		>
		<span class="inline-flex items-center gap-1"
			><span class="h-2.5 w-2.5 rounded-sm bg-red-500"></span> Documented flood year</span
		>
	</div>
</section>

{#if highest}
	<section class="mt-8 rounded-xl border border-sky-200 bg-sky-50 p-5">
		<h2 class="text-lg font-semibold text-sky-900">Priority area: {highest.township}</h2>
		<p class="mt-1 text-sm text-sky-800">
			Ranks first with a risk score of {highest.risk_score.toFixed(1)}. It hosts ~{formatInt(
				highest.pop_est
			)} residents,
			{highest.schools} schools and {highest.health_facilities} health facilities, combining strong hazard
			exposure with a large population and dense critical infrastructure.
		</p>
		<button
			onclick={async () => {
				await goto(resolve('/locations'));
			}}
			class="mt-3 rounded-lg bg-sky-600 px-4 py-2 text-sm font-medium text-white hover:bg-sky-700"
		>
			Explore all townships →
		</button>
	</section>
{/if}

<section class="mt-8">
	<h2 class="mb-3 text-lg font-semibold">All townships</h2>
	<RiskTable rows={riskSummary} />
</section>
