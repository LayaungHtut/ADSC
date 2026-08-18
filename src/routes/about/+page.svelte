<script lang="ts">
	const principles = [
		{
			title: 'Open, traceable data',
			body: 'Every indicator is derived from public datasets with recorded provenance (SHA-256 + source URL). No numbers are invented.'
		},
		{
			title: 'Honest limitations',
			body: 'Coarse rainfall resolution, district-level vulnerability, and missing flood-extent polygons are disclosed on every relevant page.'
		},
		{
			title: 'Decision support, not forecasting',
			body: 'The index prioritizes areas for early-warning and infrastructure investment. It is not an operational flood forecast.'
		}
	];

	const roadmap = [
		['Now', 'Prioritize the top risk class for early-warning and drainage maintenance'],
		['Next', 'Blend flood-extent data (Global Flood Database) and extend the CHIRPS record'],
		['Next', 'Integrate township-level socioeconomic and poverty statistics as they open up'],
		['Later', 'Extend the same framework to other ASEAN cities (Manila, Bangkok, HCMC)']
	];
</script>

<svelte:head>
	<title>About — FloodResilience Yangon</title>
</svelte:head>

<section class="mb-8 max-w-3xl">
	<h1 class="text-3xl font-bold tracking-tight">About the project</h1>
	<p class="mt-2 text-slate-600">
		FloodResilience ASEAN is a student data-science project for the ASEAN Data Science Explorers
		2026 competition. We chose Yangon, Myanmar — a low-lying delta city where monsoon rains, river
		overflow and a dense coastal population combine into a recurring crisis — and built a
		reproducible framework to measure flood risk at the township level.
	</p>
</section>

<section class="mb-8">
	<h2 class="mb-3 text-lg font-semibold">Our approach</h2>
	<div class="grid gap-4 md:grid-cols-3">
		{#each principles as p (p.title)}
			<div class="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
				<h3 class="font-semibold">{p.title}</h3>
				<p class="mt-1 text-sm text-slate-600">{p.body}</p>
			</div>
		{/each}
	</div>
</section>

<section class="mb-8 rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
	<h2 class="mb-3 text-lg font-semibold">Why Yangon?</h2>
	<p class="text-sm leading-relaxed text-slate-600">
		Yangon Region is one of Myanmar's most flood-exposed areas: the low-lying southern townships
		along the Yangon and Bago rivers and the delta coast flood during the south-west monsoon
		(May-October), and the city hosts millions of residents whose daily services are disrupted by
		recurrent inundation. Because the region's open datasets (CHIRPS, Copernicus DEM, Kontur,
		WorldPop, HDX, DFO) are publicly traceable, it is an ideal case to prototype a risk framework
		that can be scaled across the region. Documented major flood years in our rainfall record —
		1988, 1997, 2002, 2007, 2013, 2014 and 2020 — confirm the hazard signal is real.
	</p>
</section>

<section class="mb-8 rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
	<h2 class="mb-3 text-lg font-semibold">From analysis to action</h2>
	<div class="overflow-x-auto">
		<table class="w-full text-sm">
			<tbody>
				{#each roadmap as r (r[0])}
					<tr class="border-t border-slate-100">
						<td class="py-2 pr-4 font-semibold">{r[0]}</td>
						<td class="py-2 text-slate-600">{r[1]}</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
</section>

<section class="rounded-xl border border-sky-200 bg-sky-50 p-5">
	<h2 class="text-lg font-semibold text-sky-900">Team</h2>
	<p class="mt-1 text-sm text-sky-800">
		Two students from Myanmar, ASEAN Data Science Explorers 2026. This dashboard is the interactive
		layer of a storyboard built in SAP Analytics Cloud, sharing the same datasets and methodology.
	</p>
</section>
