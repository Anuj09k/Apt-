import { useState } from "react";
import { Command, Menu } from "lucide-react";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import { Button } from "@/components/ui/button";
import {
  NavigationMenu,
  NavigationMenuContent,
  NavigationMenuItem,
  NavigationMenuList,
  NavigationMenuTrigger,
} from "@/components/ui/navigation-menu";
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet";
import { Brand } from "@/components/Brand";

/**
 * Project navigation — one row of group triggers, each opening a panel of its modules.
 *
 * Replaces the two-tier bar: the second tier only ever showed one group's modules, so it
 * cost a permanent row of height to display three buttons. Here the same three sit in a
 * dropdown that is only on screen while it is being read, and the bar keeps a single row.
 *
 * Below `lg` the whole thing collapses into a sheet with one accordion section per group,
 * because eleven module names in a row is not navigable on a phone.
 */

// One line each, describing what the module decides rather than restating its name --
// "Parking / Parking" tells a first-time user nothing.
const DESCRIPTIONS = {
  plot: "Boundary, area, setback, and height envelope limits",
  gis: "Satellite imagery, terrain elevation, slope, and solar analysis",
  township: "Macro-parcel master zoning & mixed-use commercial planning",
  "autonomous-studio": "Quick-start generative layouts from plot area and budget tier",
  planning: "Unit mix, apartment layouts, circulation cores, and floor plate",
  parking: "Required and provided bays, basement layouts, and vehicular circulation",
  studio: "Parametric facade synthesis, park zoning, and bay generation",
  "3d": "Interactive 3D massing model, floor stacking, and structural bays",
  calculations: "Loads, areas, carpet-to-saleable, and derived design quantities",
  engineering: "Structural member sizing checked against IS and NBC codes",
  bim: "DXF, DWG, and IFC import/export for AutoCAD and Revit interop",
  "digital-twin": "Construction progress and provided or simulated telemetry scenarios",
  boq: "Comprehensive bills of quantities derived from designed structures",
  cost: "Unit rates, material wastage, and itemised cost breakdown",
  procurement: "Indicative material pricing and procurement planning scenarios",
  programme: "CPM critical path schedule, float analysis, and build timeline",
  finance: "Revenue projections, developer margin, IRR, and break-even model",
  compliance: "Supported checks against configured planning controls; not statutory approval",
  "urban-sustainability": "Green building rating (IGBC/GRIHA), solar yield, and carbon footprint",
  "data-health": "Telemetry integrity verification and stale data audit across models",
  reports: "Export statutory drawings, BOQ spreadsheets, and design dossiers",
  collaboration: "Version snapshots, access control roles, and team activity audit",
  "smart-city": "City-scale planning, traffic LOS & macro utility networks",
  "ai-os": "Knowledge graph, engineering memory, decision log & what-if sandbox",
};

function ModuleLink({ item, active, onPick, onDone }) {
  const [key, label, Icon] = item;
  const isActive = active === key;
  return (
    <li>
      <button
        type="button"
        onClick={() => { onPick(key); onDone?.(); }}
        data-testid={`nav-module-${key}`}
        aria-current={isActive ? "page" : undefined}
        className={`flex w-full select-none items-start gap-2.5 rounded-md px-3 py-2 text-left outline-none transition-colors hover:bg-slate-100 hover:text-slate-900 ${
          isActive ? "bg-slate-100 font-medium text-slate-900" : "text-slate-700"
        }`}
      >
        <Icon className={`size-4 shrink-0 mt-0.5 ${isActive ? "text-blue-600" : "text-slate-400"}`} />
        <div className="min-w-0 flex-1">
          <div className="text-xs font-semibold text-slate-900 leading-snug">{label}</div>
          <p className="mt-0.5 text-[11px] leading-relaxed text-slate-500 whitespace-normal break-words">
            {DESCRIPTIONS[key] || ""}
          </p>
        </div>
      </button>
    </li>
  );
}

export function ProjectNav({ groups, active, onPick, onOpenPalette }) {
  const [sheetOpen, setSheetOpen] = useState(false);

  return (
    <nav
      className="sticky top-0 z-20 border-b border-slate-800 bg-slate-900 text-slate-300"
      data-testid="module-nav"
    >
      {/* Desktop */}
      <div className="hidden items-center gap-2 px-2 lg:flex">
        <NavigationMenu>
          <NavigationMenuList>
            {groups.map(([gkey, glabel, items]) => {
              const holdsActive = items.some((m) => m[0] === active);
              return (
                <NavigationMenuItem key={gkey}>
                  <NavigationMenuTrigger
                    data-testid={`nav-group-${gkey}`}
                    className={`h-11 gap-1.5 rounded-none bg-transparent text-[11px] uppercase tracking-wide hover:bg-slate-800 hover:text-white focus:bg-slate-800 focus:text-white data-[state=open]:bg-slate-800 data-[state=open]:text-white ${
                      holdsActive ? "text-white font-bold" : "text-slate-200 font-medium"
                    }`}
                  >
                    {glabel}
                    {holdsActive && <span className="ml-0.5 h-1.5 w-1.5 rounded-full bg-blue-400" />}
                  </NavigationMenuTrigger>
                  <NavigationMenuContent>
                    <ul className="flex flex-col p-1.5 gap-0.5 w-80 sm:w-[380px] max-h-[min(85vh,580px)] overflow-y-auto">
                      {items.map((item) => (
                        <ModuleLink key={item[0]} item={item} active={active} onPick={onPick} />
                      ))}
                    </ul>
                  </NavigationMenuContent>
                </NavigationMenuItem>
              );
            })}
          </NavigationMenuList>
        </NavigationMenu>

        <div className="flex-1" />

        <button
          type="button"
          onClick={onOpenPalette}
          data-testid="nav-open-palette"
          className="flex shrink-0 items-center gap-1.5 whitespace-nowrap px-3 py-1.5 text-[11px] text-slate-200 transition-colors hover:text-white font-medium"
        >
          <Command className="h-3.5 w-3.5 shrink-0" />
          Jump to…
          <kbd className="rounded-sm border border-slate-600 bg-slate-800 px-1 font-mono text-[10px] text-slate-200">Ctrl K</kbd>
        </button>
      </div>

      {/* Mobile / tablet */}
      <div className="block lg:hidden">
        <div className="flex items-center justify-between px-2 py-2">
          <span className="text-[11px] uppercase tracking-wide text-slate-400">
            {groups.find(([, , items]) => items.some((m) => m[0] === active))?.[1] || "Menu"}
          </span>
          <div className="flex items-center gap-1">
            <button
              type="button"
              onClick={onOpenPalette}
              data-testid="nav-open-palette-mobile"
              className="flex items-center gap-1.5 px-2 py-1.5 text-[11px] text-slate-400 transition-colors hover:text-white"
            >
              <Command className="h-3.5 w-3.5 shrink-0" />
              Jump to…
            </button>
            <Sheet open={sheetOpen} onOpenChange={setSheetOpen}>
              <SheetTrigger asChild>
                <Button variant="outline" size="icon" data-testid="nav-open-sheet" aria-label="Open menu">
                  <Menu className="size-4" />
                </Button>
              </SheetTrigger>
              <SheetContent className="overflow-y-auto">
                <SheetHeader>
                  <SheetTitle>
                    <Brand testid="project-nav-sheet-brand" markClass="h-7 w-auto" wordClass="text-[14px]" />
                  </SheetTitle>
                </SheetHeader>
                <div className="my-6 flex flex-col gap-6">
                  <Accordion
                    type="single"
                    collapsible
                    defaultValue={groups.find(([, , items]) => items.some((m) => m[0] === active))?.[0]}
                    className="flex w-full flex-col gap-4"
                  >
                    {groups.map(([gkey, glabel, items]) => (
                      <AccordionItem key={gkey} value={gkey} className="border-b-0">
                        <AccordionTrigger
                          data-testid={`nav-group-${gkey}-mobile`}
                          className="py-0 font-semibold hover:no-underline"
                        >
                          {glabel}
                        </AccordionTrigger>
                        <AccordionContent className="mt-1 pb-1">
                          <ul className="flex flex-col gap-1">
                            {items.map((item) => (
                              <ModuleLink
                                key={item[0]}
                                item={item}
                                active={active}
                                onPick={onPick}
                                onDone={() => setSheetOpen(false)}
                              />
                            ))}
                          </ul>
                        </AccordionContent>
                      </AccordionItem>
                    ))}
                  </Accordion>
                </div>
              </SheetContent>
            </Sheet>
          </div>
        </div>
      </div>
    </nav>
  );
}

export default ProjectNav;
