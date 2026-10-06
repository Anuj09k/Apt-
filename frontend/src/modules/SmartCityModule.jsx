import { useEffect, useState } from "react";
import { toast } from "sonner";
import {
  Globe2,
  Car,
  Droplets,
  Zap,
  Flame,
  Sun,
  TrendingUp,
  RefreshCw,
  ShieldCheck,
  Building,
} from "lucide-react";
import { api, apiError } from "../lib/api";
import { Section, Metric } from "../components/Field";
import { Button } from "../components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "../components/ui/table";
import { num } from "../lib/format";

export default function SmartCityModule({ project, projectId }) {
  const [traffic, setTraffic] = useState(null);
  const [utilities, setUtilities] = useState(null);
  const [digitalTwin, setDigitalTwin] = useState(null);
  const [forecast, setForecast] = useState(null);
  const [loading, setLoading] = useState(false);

  const loadData = async () => {
    if (!projectId) return;
    setLoading(true);
    try {
      const [trRes, utRes, twRes, fcRes] = await Promise.all([
        api.get(`/projects/${projectId}/smart-city/traffic`),
        api.get(`/projects/${projectId}/smart-city/utilities`),
        api.get(`/projects/${projectId}/smart-city/digital-twin`),
        api.get(`/projects/${projectId}/smart-city/infrastructure-forecast`),
      ]);
      setTraffic(trRes.data);
      setUtilities(utRes.data);
      setDigitalTwin(twRes.data);
      setForecast(fcRes.data);
    } catch (e) {
      toast.error(apiError(e.response?.data?.detail));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [projectId]);

  return (
    <div className="space-y-6">
      {/* HEADER */}
      <div className="rounded-lg border border-teal-900/40 bg-gradient-to-r from-slate-900 via-slate-900 to-teal-950/40 p-5 text-white">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-teal-600 text-white shadow-lg shadow-teal-500/30">
              <Globe2 className="h-6 w-6" />
            </div>
            <div>
              <h1 className="text-xl font-bold tracking-tight">Smart City Platform</h1>
              <p className="text-xs text-slate-300">
                City-scale urban zoning, traffic LOS simulation, macro utility network optimization, and infrastructure demand forecasting
              </p>
            </div>
          </div>
          <Button onClick={loadData} disabled={loading} size="sm" className="bg-teal-700 hover:bg-teal-800">
            {loading ? <RefreshCw className="mr-1.5 h-3.5 w-3.5 animate-spin" /> : <RefreshCw className="mr-1.5 h-3.5 w-3.5" />}
            Refresh Analytics
          </Button>
        </div>
      </div>

      {/* 1. TRAFFIC SIMULATION & ACCESS */}
      {traffic && (
        <Section
          title="Traffic Simulation & Access Capacity"
          description="Trip generation, road Level of Service (LOS) analysis, and fire tender turning radii clearance"
        >
          <div className="grid grid-cols-2 gap-3 sm:grid-cols-4 mb-4">
            <Metric label="Peak AM Trips" value={`${traffic.trip_generation?.peak_am_trips_per_hour} / hr`} hint="Outbound peak" />
            <Metric label="Peak PM Trips" value={`${traffic.trip_generation?.peak_pm_trips_per_hour} / hr`} hint="Inbound peak" />
            <Metric label="Level of Service" value={traffic.level_of_service?.grade} hint={`V/C Ratio: ${traffic.level_of_service?.volume_capacity_ratio}`} />
            <Metric label="Avg Traffic Delay" value={`${traffic.level_of_service?.traffic_delay_seconds_per_vehicle}s`} hint="Queue delay at gate" />
          </div>

          <div className="rounded border border-slate-200 bg-slate-50/70 p-3 text-xs shadow-2xs">
            <div className="flex items-center justify-between border-b border-slate-200 pb-2">
              <span className="font-bold text-slate-900 flex items-center gap-1.5">
                <Flame className="h-4 w-4 text-orange-600" /> Emergency Fire Tender Maneuverability
              </span>
              <span className={`font-bold ${traffic.emergency_vehicle_clearance?.status?.startsWith("PASS") ? "text-emerald-700" : "text-amber-700"}`}>{traffic.emergency_vehicle_clearance?.status}</span>
            </div>
            <div className="mt-2 grid grid-cols-1 md:grid-cols-3 gap-3 text-slate-700">
              <div>Required Radius: <strong className="text-slate-900">{traffic.emergency_vehicle_clearance?.required_turning_radius_m}m</strong></div>
              <div>Provided Radius: <strong className="text-slate-900">{traffic.emergency_vehicle_clearance?.provided_turning_radius_m ?? "not measured"}{traffic.emergency_vehicle_clearance?.provided_turning_radius_m != null ? "m" : ""}</strong></div>
              <div>Clear Roadway: <strong className="text-slate-900">{traffic.emergency_vehicle_clearance?.clear_access_width_m}m</strong></div>
            </div>
          </div>
        </Section>
      )}

      {/* 2. UTILITY NETWORK OPTIMISATION */}
      {utilities && (
        <Section
          title="Macro Utility Network Optimisation"
          description="Integrated stormwater culverts, looped water distribution, gravity sewerage, and electrical substations"
        >
          <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-4 text-xs">
            {/* Stormwater */}
            <div className="rounded-md border border-slate-200 bg-white p-3 shadow-2xs">
              <div className="flex items-center gap-1.5 font-bold text-teal-700 border-b border-slate-100 pb-1.5">
                <Droplets className="h-4 w-4 text-teal-600" /> Stormwater Network
              </div>
              <ul className="mt-2 space-y-1 text-slate-600">
                <li>Peak Discharge: <strong className="text-slate-900">{utilities.stormwater?.peak_discharge_m3_per_hr} m³/hr</strong></li>
                <li>Profile: <strong className="text-slate-900">{utilities.stormwater?.drain_profile}</strong></li>
                <li>Slope: <strong className="text-slate-900">{utilities.stormwater?.minimum_slope}</strong></li>
                <li>RWH Potential: <strong className="text-slate-900">{num(utilities.stormwater?.annual_harvesting_potential_kl)} KL/yr</strong></li>
              </ul>
            </div>

            {/* Water Supply */}
            <div className="rounded-md border border-slate-200 bg-white p-3 shadow-2xs">
              <div className="flex items-center gap-1.5 font-bold text-blue-700 border-b border-slate-100 pb-1.5">
                <Droplets className="h-4 w-4 text-blue-600" /> Water Supply Loop
              </div>
              <ul className="mt-2 space-y-1 text-slate-600">
                <li>Daily Demand: <strong className="text-slate-900">{utilities.water_supply?.daily_water_demand_kl} KLD</strong></li>
                <li>Primary Main: <strong className="text-slate-900">{utilities.water_supply?.primary_main_diameter_mm}mm DI K9</strong></li>
                <li>Pressure Head: <strong className="text-slate-900">{utilities.water_supply?.residual_pressure_head_m}m residual</strong></li>
                <li>Fire Reserve: <strong className="text-slate-900">{utilities.water_supply?.storage_breakdown?.fire_reserve_dedicated_kl ?? "see Engineering > Fire"}{utilities.water_supply?.storage_breakdown?.fire_reserve_dedicated_kl != null ? " KL" : ""}</strong></li>
              </ul>
            </div>

            {/* Sewerage */}
            <div className="rounded-md border border-slate-200 bg-white p-3 shadow-2xs">
              <div className="flex items-center gap-1.5 font-bold text-amber-800 border-b border-slate-100 pb-1.5">
                <Droplets className="h-4 w-4 text-amber-600" /> Gravity Sewerage
              </div>
              <ul className="mt-2 space-y-1 text-slate-600">
                <li>Daily Sewage: <strong className="text-slate-900">{utilities.sewerage?.daily_sewage_generation_kl} KLD</strong></li>
                <li>Pipe Dia: <strong className="text-slate-900">{utilities.sewerage?.pipe_diameter_mm}mm dia</strong></li>
                <li>Velocity: <strong className="text-slate-900">{utilities.sewerage?.self_cleansing_velocity_m_s} m/s</strong></li>
                <li>Treated Reuse: <strong className="text-slate-900">{utilities.sewerage?.treated_effluent_reuse_kl} KLD</strong></li>
              </ul>
            </div>

            {/* Electrical */}
            <div className="rounded-md border border-slate-200 bg-white p-3 shadow-2xs">
              <div className="flex items-center gap-1.5 font-bold text-yellow-800 border-b border-slate-100 pb-1.5">
                <Zap className="h-4 w-4 text-yellow-600" /> Electrical Grid & ESS
              </div>
              <ul className="mt-2 space-y-1 text-slate-600">
                <li>Connected Load: <strong className="text-slate-900">{num(utilities.electrical?.connected_load_kva)} kVA</strong></li>
                <li>Transformer: <strong className="text-slate-900">{utilities.electrical?.transformer_capacity}</strong></li>
                <li>DG Backup: <strong className="text-slate-900">{num(utilities.electrical?.dg_backup_capacity_kva)} kVA</strong></li>
                <li>Solar PV: <strong className="text-slate-900">{utilities.electrical?.solar_pv_rooftop_kwp ?? "see Sustainability"}{utilities.electrical?.solar_pv_rooftop_kwp != null ? " kWp" : ""}</strong></li>
              </ul>
            </div>
          </div>
        </Section>
      )}

      {/* 3. URBAN DIGITAL TWIN & MICROCLIMATE */}
      {digitalTwin && (
        <Section
          title="Urban Digital Twin & Microclimate"
          description="Georeferenced 3D spatial twin context, sun-path microclimate, and Urban Heat Island (UHI) mitigation"
        >
          <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
            <div className="rounded border border-slate-200 bg-slate-50/70 p-4 text-xs shadow-2xs">
              <div className="flex items-center justify-between border-b border-slate-200 pb-2">
                <span className="font-bold text-slate-900 flex items-center gap-1.5">
                  <Sun className="h-4 w-4 text-amber-600" /> Microclimate & Heat Island Score
                </span>
                <span className="font-bold text-teal-700">
                  UHI Score: {digitalTwin.microclimate_simulation?.urban_heat_island_score ?? "not modelled"}
                </span>
              </div>
              <ul className="mt-3 space-y-2 text-slate-700">
                <li>Annual Sun Exposure: <strong className="text-slate-900">{digitalTwin.microclimate_simulation?.annual_sun_exposure_hours} hrs/yr</strong></li>
                <li>Local Cooling Effect: <strong className="text-teal-700">{digitalTwin.microclimate_simulation?.estimated_local_cooling_effect}</strong></li>
                <li>Mean Wind Velocity: <strong className="text-slate-900">{digitalTwin.microclimate_simulation?.mean_wind_tunnel_velocity_m_s} m/s</strong></li>
                <li>Cross-Ventilation Efficiency: <strong className="text-slate-900">{digitalTwin.microclimate_simulation?.cross_ventilation_efficiency_pct}%</strong></li>
                <li>Shadow Impact: <strong className="text-slate-900">{digitalTwin.microclimate_simulation?.shadow_corridor_impact}</strong></li>
              </ul>
            </div>

            <div className="rounded border border-slate-200 bg-slate-50/70 p-4 text-xs shadow-2xs">
              <div className="border-b border-slate-200 pb-2 font-bold text-slate-900">
                Spatial GIS Twin Layers
              </div>
              <div className="mt-3 space-y-2">
                {digitalTwin.gis_boundary_layers?.map((layer, idx) => (
                  <div key={idx} className="flex items-center justify-between rounded border border-slate-200 bg-white px-2.5 py-1.5 shadow-2xs">
                    <span className="text-slate-700 font-medium">{layer.layer}</span>
                    <span className="rounded border border-teal-200 bg-teal-50 px-1.5 py-0.5 text-[10px] font-semibold text-teal-800">
                      {layer.entities} entities ({layer.status})
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </Section>
      )}

      {/* 4. INFRASTRUCTURE DEMAND FORECAST */}
      {forecast && (
        <Section
          title="Multi-Year Infrastructure Demand Forecasting"
          description="Civic load forecasting across municipal water, power demand, solid waste, and EV charging (2026–2040)"
        >
          <Table>
            <TableHeader>
              <TableRow className="bg-slate-50 border-b border-slate-200">
                <TableHead className="text-slate-900 font-semibold">Year</TableHead>
                <TableHead className="text-right text-slate-900 font-semibold">Population</TableHead>
                <TableHead className="text-right text-slate-900 font-semibold">Water (MLD)</TableHead>
                <TableHead className="text-right text-slate-900 font-semibold">Power (MVA)</TableHead>
                <TableHead className="text-right text-slate-900 font-semibold">Solid Waste (TPD)</TableHead>
                <TableHead className="text-right text-slate-900 font-semibold">Recycled Water</TableHead>
                <TableHead className="text-right text-slate-900 font-semibold">EV Load (kW)</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {forecast.forecast_timeline?.map((row) => (
                <TableRow key={row.year}>
                  <TableCell className="font-bold text-slate-900 text-xs">{row.year}</TableCell>
                  <TableCell className="text-right text-xs text-slate-700">{num(row.projected_population)}</TableCell>
                  <TableCell className="text-right text-xs text-slate-700">{row.water_demand_mld} MLD</TableCell>
                  <TableCell className="text-right text-xs text-slate-700">{row.power_demand_mva} MVA</TableCell>
                  <TableCell className="text-right text-xs text-slate-700">{row.solid_waste_tpd} TPD</TableCell>
                  <TableCell className="text-right text-xs text-teal-700 font-semibold">{row.recycled_water_available_mld} MLD</TableCell>
                  <TableCell className="text-right text-xs text-amber-700 font-semibold">{row.ev_charging_load_kw} kW</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Section>
      )}
    </div>
  );
}
