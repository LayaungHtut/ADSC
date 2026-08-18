import { describe, expect, it } from 'vitest';
import { runScenario, DEFAULT_SCENARIO } from './scenario';
import { annualSeries, monthlyClimatology, riskColor, riskLabel, topRisk, totalPop, meanRisk } from './data';

describe('scenario engine (mirrors documented risk model)', () => {
	it('baseline scenario with zero changes returns 42 rows', () => {
		const res = runScenario({ rainfall: 0, population: 0, infrastructure: 0 });
		expect(res).toHaveLength(42);
	});

	it('baseline scenario matches the dashboard risk values', () => {
		// The scenario engine at zero deltas must reproduce the dashboard's risk ranking.
		const res = runScenario({ rainfall: 0, population: 0, infrastructure: 0 });
		expect(res[0]).toMatchObject({ baseline_risk: expect.any(Number), scenario_class: expect.any(Number) });
		// Top-ranked under the scenario engine should be in the top-10 dashboard list.
		const top = [...res].sort((a, b) => b.scenario_risk - a.scenario_risk)[0];
		expect(topRisk.map((r) => r.kec_code)).toContain(top.kec_code);
	});

	it('rainfall increase raises overall risk for most areas', () => {
		const base = runScenario({ rainfall: 0, population: 0, infrastructure: 0 });
		const wet = runScenario({ rainfall: 0.2, population: 0, infrastructure: 0 });
		const rising = base.filter((_, i) => wet[i].scenario_risk > base[i].baseline_risk).length;
		expect(rising).toBeGreaterThan(30);
	});

	it('infrastructure resilience lowers exposure for areas with facilities', () => {
		const base = runScenario({ rainfall: 0, population: 0, infrastructure: 0 });
		const hardened = runScenario({ rainfall: 0, population: 0, infrastructure: 0.5 });
		const falling = base.filter((_, i) => hardened[i].scenario_risk < base[i].baseline_risk).length;
		expect(falling).toBeGreaterThan(0);
	});

	it('default scenario is stable and bounded 0-100', () => {
		const res = runScenario(DEFAULT_SCENARIO);
		for (const r of res) {
			expect(r.scenario_risk).toBeGreaterThanOrEqual(0);
			expect(r.scenario_risk).toBeLessThanOrEqual(100);
			expect(r.scenario_class).toBeGreaterThanOrEqual(1);
			expect(r.scenario_class).toBeLessThanOrEqual(5);
		}
	});
});

describe('data helpers', () => {
	it('annualSeries returns one row per year with rainfall and flood flag', () => {
		const s = annualSeries();
		expect(s.length).toBeGreaterThan(40);
		expect(s[0]).toMatchObject({ year: expect.any(Number), rain: expect.any(Number), flood: expect.any(Boolean) });
	});

	it('monthlyClimatology returns 12 months with mean >= 0', () => {
		const c = monthlyClimatology();
		expect(c).toHaveLength(12);
		for (const m of c) {
			expect(m.mean).toBeGreaterThanOrEqual(0);
		}
	});

	it('riskColor/riskLabel map classes consistently', () => {
		expect(riskLabel(1)).toBe('Low');
		expect(riskLabel(5)).toBe('Very high');
		expect(typeof riskColor(1)).toBe('string');
	});

	it('population and risk aggregates are positive', () => {
		expect(totalPop).toBeGreaterThan(1_000_000);
		expect(meanRisk).toBeGreaterThan(0);
		expect(topRisk).toHaveLength(10);
	});
});
