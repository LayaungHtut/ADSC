export interface RiskSummary {
	tship_code: string;
	township: string;
	district: string;
	hazard: number;
	exposure: number;
	vulnerability: number;
	risk_score: number;
	risk_class: number;
	pop_est: number;
	elev_mean_m: number;
	schools: number;
	health_facilities: number;
}

export interface FeatureRow {
	tship_code: string;
	township: string;
	district: string;
	district_code: string;
	rain_annual_mean_mm: number;
	rain_annual_last5_mean_mm: number;
	rain_wet_season_share: number;
	rain_extreme_months: number;
	rain_annual_trend_mm_yr: number;
	rain_annual_trend_pct_yr: number;
	rain_p95_monthly_mm: number;
	rain_total_months: number;
	elev_mean_m: number;
	elev_min_m: number;
	elev_max_m: number;
	slope_mean_pct: number;
	pop_est: number;
	schools: number;
	health_facilities: number;
	rfh_mean: number;
	r1h_mean: number;
	r3h_mean: number;
	rfh_p95: number;
	n_obs: number;
	child_share: number;
	elderly_share: number;
	area_km2: number;
	pop_density: number;
}

export interface RainfallRow {
	year: number;
	month: number;
	rainfall_mm: number;
	flood_year: number;
}

export interface DistrictRow {
	district: string;
	district_code: string;
	n_township: number;
	pop_est: number;
	schools: number;
	health_facilities: number;
}

export interface TshipProps extends RiskSummary {
	area_km2?: number;
}

export interface TshipFeature {
	type: 'Feature';
	properties: TshipProps;
	geometry: unknown;
}
