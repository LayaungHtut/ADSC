<script lang="ts">
	import RiskTable from '$lib/components/RiskTable.svelte';
	import { riskSummary } from '$lib/data';
</script>

<svelte:head>
	<title>Kecamatan — FloodResilience Jakarta</title>
</svelte:head>

<section class="mb-6">
	<h1 class="text-3xl font-bold tracking-tight">Kecamatan explorer</h1>
	<p class="mt-2 max-w-3xl text-slate-600">
		Search, sort and filter all 42 urban kecamatan. Click a row to open the full risk profile.
	</p>
</section>

<section>
	<RiskTable rows={riskSummary} />
</section>
