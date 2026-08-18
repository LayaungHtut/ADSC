<script lang="ts">
	import { onDestroy, onMount } from 'svelte';
	import { RISK_CLASS_COLORS, RISK_CLASS_LABELS, riskColor } from '$lib/data';
	import type { TshipFeature } from '$lib/types';
	import riskJson from '$lib/data/risk.json';
	import type * as L from 'leaflet';

	let {
		selected,
		onselect,
		height = '60vh'
	}: {
		selected: string | null;
		onselect: (code: string) => void;
		height?: string;
	} = $props();

	let container: HTMLDivElement | undefined = $state();
	let map: L.Map | undefined = $state();
	let layer: L.GeoJSON | undefined = $state();
	let cleanup: (() => void) | undefined;

	const geojson = riskJson as unknown as { type: 'FeatureCollection'; features: TshipFeature[] };

	function styleFor(
		f: { properties: { risk_class: number; tship_code: string } },
		highlight: boolean
	): L.PathOptions {
		const cls = f.properties.risk_class;
		return {
			color: '#ffffff',
			weight: highlight ? 2.5 : 1,
			opacity: 1,
			fillColor: riskColor(cls),
			fillOpacity: highlight ? 0.95 : 0.8
		};
	}

	onMount(async () => {
		const L = (await import('leaflet')).default;
		await import('leaflet/dist/leaflet.css');
		if (!container) return;
		map = L.map(container, { scrollWheelZoom: false }).setView([16.8713, 96.1561], 10);
		L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
			maxZoom: 19,
			attribution: '&copy; OpenStreetMap contributors'
		}).addTo(map);
		layer = L.geoJSON(geojson as unknown as GeoJSON.GeoJsonObject, {
			style: (f) =>
				styleFor(
					f as { properties: { risk_class: number; tship_code: string } },
					(f as { properties: { tship_code: string } }).properties.tship_code === selected
				),
			onEachFeature: (f, l: L.Layer) => {
				l.on('click', () => onselect(f.properties.tship_code));
				l.bindTooltip(`${f.properties.township} — risk ${f.properties.risk_score.toFixed(1)}`, {
					sticky: true
				});
			}
		}).addTo(map);
		map.fitBounds(layer.getBounds().pad(0.05));
		cleanup = () => map?.remove();
	});

	onDestroy(() => cleanup?.());

	$effect(() => {
		const sel = selected;
		if (!layer) return;
		layer.eachLayer((l) => {
			const path = l as L.Path & {
				feature: { properties: { risk_class: number; tship_code: string } };
			};
			path.setStyle(styleFor(path.feature, path.feature.properties.tship_code === sel));
		});
	});
</script>

<div class="relative" style="height: {height}">
	<div bind:this={container} class="h-full w-full rounded-xl"></div>
	<div
		class="pointer-events-none absolute right-4 bottom-4 z-[1000] rounded-lg bg-white/95 p-3 text-xs shadow-lg"
	>
		<p class="mb-2 font-semibold text-slate-700">Risk class</p>
		<div class="flex flex-col gap-1.5">
			{#each RISK_CLASS_LABELS as label, i (label)}
				<span class="flex items-center gap-2">
					<span class="h-3 w-3 rounded-sm" style="background-color: {RISK_CLASS_COLORS[i]}"></span>
					{label}
				</span>
			{/each}
		</div>
	</div>
</div>
