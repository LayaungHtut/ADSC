<script lang="ts">
	import './layout.css';
	import { page } from '$app/state';
	import { resolve } from '$app/paths';

	let { children } = $props();

	const nav = [
		{ href: '/', label: 'Dashboard' },
		{ href: '/risk', label: 'Risk explorer' },
		{ href: '/map', label: 'Risk map' },
		{ href: '/scenarios', label: 'Scenarios' },
		{ href: '/locations', label: 'Townships' },
		{ href: '/methodology', label: 'Methodology' },
		{ href: '/data', label: 'Data' },
		{ href: '/about', label: 'About' }
	] as const;

	function isActive(href: string): boolean {
		if (href === '/') return page.url.pathname === '/';
		return page.url.pathname.startsWith(href);
	}
</script>

<svelte:head>
	<title>FloodResilience Yangon — Urban Flood Risk Dashboard</title>
	<meta
		name="description"
		content="Data-driven flood risk intelligence for Yangon's 45 urban townships (ASEAN Data Science Explorers 2026)."
	/>
</svelte:head>

<div class="min-h-screen bg-slate-50 text-slate-900">
	<header class="sticky top-0 z-[1000] border-b border-slate-200 bg-white/95 backdrop-blur">
		<div class="mx-auto flex max-w-6xl items-center justify-between gap-4 px-4 py-3">
			<a href={resolve('/')} class="flex items-center gap-2">
				<span
					class="flex h-8 w-8 items-center justify-center rounded-lg bg-sky-600 text-sm font-bold text-white"
				>
					FR
				</span>
				<span class="text-base font-bold tracking-tight">
					FloodResilience <span class="text-sky-600">Yangon</span>
				</span>
			</a>
			<nav class="hidden items-center gap-1 md:flex">
				{#each nav as n (n.href)}
					<a
						href={resolve(n.href)}
						class="rounded-lg px-3 py-1.5 text-sm font-medium transition-colors {isActive(n.href)
							? 'bg-sky-50 text-sky-700'
							: 'text-slate-600 hover:bg-slate-100'}"
					>
						{n.label}
					</a>
				{/each}
			</nav>
		</div>
		<nav class="flex gap-1 overflow-x-auto px-4 pb-2 md:hidden">
			{#each nav as n (n.href)}
				<a
					href={resolve(n.href)}
					class="rounded-lg px-3 py-1.5 text-sm font-medium whitespace-nowrap {isActive(n.href)
						? 'bg-sky-50 text-sky-700'
						: 'text-slate-600'}"
				>
					{n.label}
				</a>
			{/each}
		</nav>
	</header>

	<main class="mx-auto max-w-6xl px-4 py-8">
		{@render children()}
	</main>

	<footer class="border-t border-slate-200 bg-white">
		<div class="mx-auto max-w-6xl px-4 py-6 text-xs leading-relaxed text-slate-500">
			<p class="font-semibold text-slate-700">
				FloodResilience ASEAN — Urban Flood Risk Intelligence for Yangon
			</p>
			<p>
				Student project for the ASEAN Data Science Explorers 2026 competition. All figures derive
				from public data (CHIRPS, Copernicus DEM, 2014 Census, HDX, World Bank/GFDRR, DFO).
				This dashboard is a decision-support prototype, not an operational early-warning system.
			</p>
		</div>
	</footer>
</div>
