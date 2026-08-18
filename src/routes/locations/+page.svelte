<script lang="ts">
	import RiskTable from '$lib/components/RiskTable.svelte';
	import { riskSummary } from '$lib/data';
</script>

<svelte:head>
	<title>Townships — FloodResilience Yangon</title>
</svelte:head>

<section class="mb-6">
	<h1 class="text-3xl font-bold tracking-tight">Township explorer</h1>
	<p class="mt-2 max-w-3xl text-slate-600">
		Search, sort and filter all 45 urban townships. Click a row to open the full risk profile.
	</p>
</section>

<section>
	<RiskTable rows={riskSummary} searchable />
</section>
