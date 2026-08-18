import { page } from 'vitest/browser';
import { describe, expect, it } from 'vitest';
import { render } from 'vitest-browser-svelte';
import KpiCard from './KpiCard.svelte';

describe('KpiCard.svelte', () => {
	it('renders label, value and sub', async () => {
		render(KpiCard, { label: 'Townships assessed', value: '45', sub: 'urban areas' });

		await expect.element(page.getByText('Townships assessed')).toBeInTheDocument();
		await expect.element(page.getByText('45')).toBeInTheDocument();
		await expect.element(page.getByText('urban areas')).toBeInTheDocument();
	});

	it('renders value without sub when omitted', async () => {
		render(KpiCard, { label: 'Mean risk', value: '43.5' });

		await expect.element(page.getByText('Mean risk')).toBeInTheDocument();
		await expect.element(page.getByText('43.5')).toBeInTheDocument();
	});
});
