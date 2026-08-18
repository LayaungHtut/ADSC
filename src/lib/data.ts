import type { DistrictRow, FeatureRow, RainfallRow, RiskSummary } from './types';
import featuresJson from './data/features.json';
import rainfallJson from './data/rainfall.json';
import districtJson from './data/district.json';
import riskSummaryJson from './data/risk-summary.json';

export const features = featuresJson as unknown as FeatureRow[];
export const rainfall = rainfallJson as unknown as RainfallRow[];
export const district = districtJson as unknown as DistrictRow[];
export const riskSummary = riskSummaryJson as unknown as RiskSummary[];

export const RISK_CLASS_COLORS = ['#d1fae5', '#a7f3d0', '#fde68a', '#fdba74', '#ef4444'];
export const RISK_CLASS_LABELS = ['Low', 'Moderate-low', 'Moderate', 'High', 'Very high'];

export const byCode = new Map(riskSummary.map((r) => [r.tship_code, r]));

export function riskColor(cls: number): string {
	return RISK_CLASS_COLORS[Math.min(Math.max(Math.round(cls) - 1, 0), 4)];
}

export function riskLabel(cls: number): string {
	return RISK_CLASS_LABELS[Math.min(Math.max(Math.round(cls) - 1, 0), 4)];
}

export function formatInt(n: number): string {
	return n.toLocaleString('en-US', { maximumFractionDigits: 0 });
}

export function formatDec(n: number, digits = 1): string {
	return n.toLocaleString('en-US', { maximumFractionDigits: digits });
}

export const topRisk = [...riskSummary].sort((a, b) => b.risk_score - a.risk_score).slice(0, 10);
export const totalPop = riskSummary.reduce((s, r) => s + r.pop_est, 0);
export const meanRisk = riskSummary.reduce((s, r) => s + r.risk_score, 0) / riskSummary.length;

export function monthlyClimatology(): { month: number; mean: number }[] {
	const m = Array.from({ length: 12 }, (_, i) => ({ month: i + 1, sum: 0, n: 0 }));
	for (const r of rainfall) {
		m[r.month - 1].sum += r.rainfall_mm;
		m[r.month - 1].n += 1;
	}
	return m.map((x) => ({ month: x.month, mean: x.sum / x.n }));
}

export function annualSeries(): { year: number; rain: number; flood: boolean }[] {
	const by: Record<number, { sum: number; n: number; flood: boolean }> = {};
	for (const r of rainfall) {
		by[r.year] ??= { sum: 0, n: 0, flood: false };
		by[r.year].sum += r.rainfall_mm;
		by[r.year].n += 1;
		by[r.year].flood ||= r.flood_year === 1;
	}
	return Object.entries(by)
		.map(([year, v]) => ({ year: +year, rain: v.sum / v.n, flood: v.flood }))
		.sort((a, b) => a.year - b.year);
}

export function rainfallRange(): { start: number; end: number; months: number } {
	const years = rainfall.map((r) => r.year);
	return { start: Math.min(...years), end: Math.max(...years), months: rainfall.length };
}
