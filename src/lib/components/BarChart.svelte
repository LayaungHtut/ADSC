<script lang="ts">
	interface Bar {
		label: string;
		value: number;
		color?: string;
	}
	let props = $props<{
		bars: Bar[];
		max?: number;
		unit?: string;
		format?: (n: number) => string;
	}>();

	const top = $derived(Math.max(...props.bars.map((b: Bar) => b.value), props.max ?? 0));
	const fmt = $derived(props.format ?? ((n: number) => n.toLocaleString('en-US')));
	const unit = $derived(props.unit ?? '');
</script>

<div class="flex flex-col gap-2">
	{#each props.bars as b (b.label)}
		<div class="group">
			<div class="mb-1 flex items-baseline justify-between gap-2 text-sm">
				<span class="truncate font-medium text-slate-700">{b.label}</span>
				<span class="shrink-0 text-slate-500">{fmt(b.value)}{unit}</span>
			</div>
			<div class="h-2.5 w-full overflow-hidden rounded-full bg-slate-100">
				<div
					class="h-full rounded-full transition-all"
					style="width: {(b.value / top) * 100}%; background-color: {b.color ??
						'var(--color-sky-500)'}"
				></div>
			</div>
		</div>
	{/each}
</div>
