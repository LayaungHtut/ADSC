import { features } from './data';
import type { FeatureRow } from './types';

/**
 * Scenario engine — mirrors the documented risk methodology in
 * floodresilience/features/risk_index.py so scenario results are computed by
 * the same defensible model, not by arbitrary UI arithmetic.
 *
 * Risk = 0.40 * Hazard + 0.35 * Exposure + 0.25 * Vulnerability
 *
 * Hazard       = 0.35*(1-norm(elev_mean_m)) + 0.30*norm(rain_annual_mean_mm)
 *              + 0.20*norm(rain_extreme_months) + 0.15*norm(rfh_mean)
 * Exposure     = 0.35*norm(pop_est) + 0.25*norm(pop_density)
 *              + 0.20*norm(schools) + 0.20*norm(health_facilities)
 * Vulnerability = 0.60*norm(child_share) + 0.40*norm(elderly_share)
 *
 * Scenarios perturb the RAW indicator values (not the normalized scores), then
 * re-run the full pipeline. Normalization anchors to the observed (baseline)
 * min/max of each indicator, so uniform shocks (e.g. +20% rainfall everywhere)
 * genuinely move the scores instead of being erased by re-normalization.
 *
 * IMPORTANT: Scenario outputs are illustrative model exercises, NOT forecasts.
 */

export interface ScenarioInputs {
	/** Fractional change to annual rainfall indicators, e.g. 0.10 = +10% */
	rainfall: number;
	/** Fractional change to population count + density, e.g. 0.05 = +5% */
	population: number;
	/** Fractional reduction in infrastructure exposure from resilience
	 *  investments, e.g. 0.20 = -20% exposed facilities */
	infrastructure: number;
}

export interface ScenarioResultRow {
	tship_code: string;
	township: string;
	district: string;
	baseline_risk: number;
	baseline_class: number;
	scenario_risk: number;
	scenario_class: number;
	risk_delta: number;
}

function minmax(values: number[]): number[] {
	const lo = Math.min(...values);
	const hi = Math.max(...values);
	if (hi === lo) return values.map(() => 0.5);
	return values.map((v) => (v - lo) / (hi - lo));
}

function minmaxAnchored(values: number[], reference: number[]): number[] {
	const lo = Math.min(...reference);
	const hi = Math.max(...reference);
	if (hi === lo) return values.map(() => 0.5);
	return values.map((v) => (v - lo) / (hi - lo));
}

function quantileClass(scores: number[]): number[] {
	const sorted = [...scores].sort((a, b) => a - b);
	return scores.map((s) => {
		const idx = sorted.findIndex((x) => x >= s);
		const q = (idx + 1) / sorted.length;
		return Math.min(Math.max(Math.ceil(q * 5), 1), 5);
	});
}

function applyScenario(row: FeatureRow, s: ScenarioInputs): FeatureRow {
	const r = { ...row };
	r.rain_annual_mean_mm *= 1 + s.rainfall;
	r.rain_annual_last5_mean_mm *= 1 + s.rainfall;
	r.rain_p95_monthly_mm *= 1 + s.rainfall;
	r.rfh_mean *= 1 + s.rainfall;
	r.pop_est *= 1 + s.population;
	r.pop_density = r.pop_est / r.area_km2;
	r.schools = Math.max(0, r.schools * (1 - s.infrastructure));
	r.health_facilities = Math.max(0, r.health_facilities * (1 - s.infrastructure));
	return r;
}

function riskScore(rows: FeatureRow[], reference: FeatureRow[] = rows): { hazard: number; exposure: number; vulnerability: number; risk: number }[] {
	const get = (f: (r: FeatureRow) => number) => rows.map(f);
	const ref = (f: (r: FeatureRow) => number) => reference.map(f);
	const norm = (f: (r: FeatureRow) => number) => minmaxAnchored(get(f), ref(f));
	return rows.map((_, i) => {
		const hazard =
			0.35 * (1 - norm((r) => r.elev_mean_m)[i]) +
			0.3 * norm((r) => r.rain_annual_mean_mm)[i] +
			0.2 * norm((r) => r.rain_extreme_months)[i] +
			0.15 * norm((r) => r.rfh_mean)[i];
		const exposure =
			0.35 * norm((r) => r.pop_est)[i] +
			0.25 * norm((r) => r.pop_density)[i] +
			0.2 * norm((r) => r.schools)[i] +
			0.2 * norm((r) => r.health_facilities)[i];
		const vulnerability =
			0.6 * norm((r) => r.child_share)[i] + 0.4 * norm((r) => r.elderly_share)[i];
		return {
			hazard,
			exposure,
			vulnerability,
			risk: 0.4 * hazard + 0.35 * exposure + 0.25 * vulnerability
		};
	});
}

export function runScenario(inputs: ScenarioInputs): ScenarioResultRow[] {
	const baseline = riskScore(features);
	const scenario = riskScore(
		features.map((r) => applyScenario(r, inputs)),
		features
	);

	const baseScores = baseline.map((s) => s.risk * 100);
	const scenScores = scenario.map((s) => s.risk * 100);
	const baseClass = quantileClass(baseScores);
	const scenClass = quantileClass(scenScores);

	return features.map((r, i) => ({
		tship_code: r.tship_code,
		township: r.township,
		district: r.district,
		baseline_risk: baseScores[i],
		baseline_class: baseClass[i],
		scenario_risk: scenScores[i],
		scenario_class: scenClass[i],
		risk_delta: scenScores[i] - baseScores[i]
	}));
}

export const DEFAULT_SCENARIO: ScenarioInputs = {
	rainfall: 0.1,
	population: 0.05,
	infrastructure: 0.2
};
