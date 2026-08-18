<script lang="ts">
	import { RISK_CLASS_COLORS, RISK_CLASS_LABELS, riskColor } from '$lib/data';
	import type { RiskSummary } from '$lib/types';
	import { goto } from '$app/navigation';
	import { resolve } from '$app/paths';

	let props = $props<{ rows: RiskSummary[]; searchable?: boolean }>();

	let query = $state('');
	let kotaFilter = $state('all');
	let sortKey = $state<keyof RiskSummary>('risk_score');
	let sortDesc = $state(true);

	const kotas = $derived([...new Set(props.rows.map((r: RiskSummary) => r.kota))].sort());

	const visible = $derived(
		props.rows
			.filter((r: RiskSummary) => {
				if (kotaFilter !== 'all' && r.kota !== kotaFilter) return false;
				if (!props.searchable) return true;
				const q = query.trim().toLowerCase();
				return !q || r.kecamatan.toLowerCase().includes(q) || r.kec_code.includes(q);
			})
			.sort((a: RiskSummary, b: RiskSummary) => {
				const av = a[sortKey];
				const bv = b[sortKey];
				const cmp =
					typeof av === 'string' || typeof bv === 'string'
						? String(av).localeCompare(String(bv))
						: Number(av) - Number(bv);
				return sortDesc ? -cmp : cmp;
			})
	);

	function toggle(key: keyof RiskSummary) {
		if (sortKey === key) {
			sortDesc = !sortDesc;
		} else {
			sortKey = key;
			sortDesc = true;
		}
	}

	function arrow(key: keyof RiskSummary): string {
		if (sortKey !== key) return '';
		return sortDesc ? ' ↓' : ' ↑';
	}

	async function openDetail(kecamatan: string) {
		await goto(resolve(`/locations/${encodeURIComponent(kecamatan)}`));
	}
</script>

<div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
	{#if props.searchable}
		<input
			type="search"
			bind:value={query}
			placeholder="Search kecamatan or code..."
			class="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm sm:w-64"
		/>
	{/if}
	<select bind:value={kotaFilter} class="rounded-lg border border-slate-300 px-3 py-2 text-sm">
		<option value="all">All areas</option>
		{#each kotas as k (k)}<option value={k}>{k}</option>{/each}
	</select>
</div>

<div class="overflow-x-auto rounded-xl border border-slate-200 bg-white shadow-sm">
	<table class="min-w-full divide-y divide-slate-200 text-sm">
		<thead
			class="bg-slate-50 text-left text-xs font-semibold tracking-wide text-slate-500 uppercase"
		>
			<tr>
				<th class="px-4 py-3"
					><button onclick={() => toggle('kecamatan')}>Kecamatan{arrow('kecamatan')}</button></th
				>
				<th class="px-4 py-3"
					><button onclick={() => toggle('kota')}>Area{arrow('kota')}</button></th
				>
				<th class="px-4 py-3"
					><button onclick={() => toggle('risk_score')}>Risk{arrow('risk_score')}</button></th
				>
				<th class="px-4 py-3">Class</th>
				<th class="px-4 py-3"
					><button onclick={() => toggle('pop_est')}>Population{arrow('pop_est')}</button></th
				>
				<th class="px-4 py-3"
					><button onclick={() => toggle('elev_mean_m')}>Elevation{arrow('elev_mean_m')}</button
					></th
				>
				<th class="px-4 py-3"
					><button onclick={() => toggle('schools')}>Schools{arrow('schools')}</button></th
				>
				<th class="px-4 py-3"
					><button onclick={() => toggle('health_facilities')}
						>Health{arrow('health_facilities')}</button
					></th
				>
			</tr>
		</thead>
		<tbody class="divide-y divide-slate-100">
			{#each visible as r (r.kec_code)}
				<tr class="cursor-pointer hover:bg-sky-50" onclick={() => openDetail(r.kecamatan)}>
					<td class="px-4 py-3 font-medium text-slate-800">{r.kecamatan}</td>
					<td class="px-4 py-3 text-slate-500">{r.kota}</td>
					<td class="px-4 py-3 font-semibold text-slate-800">{r.risk_score.toFixed(1)}</td>
					<td class="px-4 py-3">
						<span
							class="inline-flex items-center gap-1.5 rounded-full px-2 py-0.5 text-xs font-medium"
							style="background-color: {riskColor(r.risk_class)}33; color: {riskColor(
								r.risk_class
							)}"
						>
							<span class="h-2 w-2 rounded-full" style="background-color: {riskColor(r.risk_class)}"
							></span>
							{RISK_CLASS_LABELS[r.risk_class - 1]}
						</span>
					</td>
					<td class="px-4 py-3 text-slate-600"
						>{r.pop_est.toLocaleString('en-US', { maximumFractionDigits: 0 })}</td
					>
					<td class="px-4 py-3 text-slate-600">{r.elev_mean_m.toFixed(1)} m</td>
					<td class="px-4 py-3 text-slate-600">{r.schools}</td>
					<td class="px-4 py-3 text-slate-600">{r.health_facilities}</td>
				</tr>
			{/each}
			{#if visible.length === 0}
				<tr
					><td colspan="8" class="px-4 py-8 text-center text-slate-400">No matching kecamatan.</td
					></tr
				>
			{/if}
		</tbody>
	</table>
</div>
<div class="flex items-center gap-2 text-xs text-slate-400">
	<span class="h-2 w-2 rounded-full" style="background-color: {RISK_CLASS_COLORS[0]}"></span>
	{#each RISK_CLASS_LABELS as label (label)}<span class="inline-flex items-center gap-1"
			><span
				class="h-2 w-2 rounded-full"
				style="background-color: {RISK_CLASS_COLORS[RISK_CLASS_LABELS.indexOf(label)]}"
			></span>{label}</span
		>{/each}
</div>
