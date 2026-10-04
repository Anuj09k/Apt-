import { useState } from "react";
import PlotModule from "./PlotModule";
import DevControlsModule from "./DevControlsModule";
import PlanningModule from "./PlanningModule";
import { Building2, MapPin } from "lucide-react";

/** Plot geometry, development controls, and tower/unit planning on one unified page. */
export default function SiteModule(props) {
  const [activeTab, setActiveTab] = useState("plot");

  return (
    <div className="space-y-4">
      <div className="flex border-b border-slate-200 gap-1 pb-1">
        <button
          type="button"
          onClick={() => setActiveTab("plot")}
          className={`flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-t-sm transition-colors ${
            activeTab === "plot"
              ? "bg-white border-t-2 border-t-blue-600 border-x border-slate-200 text-blue-700 shadow-xs"
              : "text-slate-600 hover:text-slate-900 hover:bg-slate-100"
          }`}
        >
          <MapPin className="h-3.5 w-3.5" />
          Plot &amp; Setbacks
        </button>
        <button
          type="button"
          onClick={() => setActiveTab("planning")}
          className={`flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-t-sm transition-colors ${
            activeTab === "planning"
              ? "bg-white border-t-2 border-t-blue-600 border-x border-slate-200 text-blue-700 shadow-xs"
              : "text-slate-600 hover:text-slate-900 hover:bg-slate-100"
          }`}
        >
          <Building2 className="h-3.5 w-3.5" />
          Tower Configuration, Unit Mix &amp; Amenities
        </button>
      </div>

      {activeTab === "plot" ? (
        <>
          <PlotModule {...props} goToModule={(mod) => {
            if (mod === "planning") setActiveTab("planning");
            else document.getElementById("site-controls")?.scrollIntoView({ behavior: "smooth" });
          }} />
          <div id="site-controls" className="scroll-mt-24">
            <DevControlsModule {...props} />
          </div>
        </>
      ) : (
        <PlanningModule {...props} goToModule={(mod) => {
          if (mod === "plot") setActiveTab("plot");
          else props.goToModule?.(mod);
        }} />
      )}
    </div>
  );
}
