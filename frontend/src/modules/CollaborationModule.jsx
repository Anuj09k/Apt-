import { useCallback, useEffect, useState } from "react";
import { toast } from "sonner";
import { 
  History, RotateCcw, Save, Trash2, UserPlus, 
  ShieldCheck, CheckCircle2, AlertCircle, Clock, 
  ListTodo, MessageSquare, Send, CornerDownRight, Zap, Plus, Check
} from "lucide-react";
import { api, apiError } from "../lib/api";
import { Section } from "../components/Field";
import { AiPanel } from "../components/AiPanel";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../components/ui/select";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "../components/ui/table";
import { dt, num } from "../lib/format";

/** Scaled plan view of one scheme: plot outline with tower footprints inside it.
 *
 *  Scalar metrics cannot separate four squat towers from two slender ones on the same
 *  FAR, which is exactly the choice a comparison is usually being made to settle. Drawn
 *  to a shared scale so the two plans are directly comparable in size, not just in shape.
 */
function PlanView({ geometry, label, scale }) {
  if (!geometry?.plot?.length_m) {
    return <div className="text-[11px] text-slate-500">No plot geometry recorded.</div>;
  }
  const { length_m: L, width_m: W } = geometry.plot;
  const pad = 8;
  const w = L * scale + pad * 2;
  const h = W * scale + pad * 2;
  return (
    <div className="space-y-1.5">
      <div className="text-[11px] font-medium text-slate-700">{label}</div>
      <svg width="100%" viewBox={`0 0 ${w} ${h}`} className="border border-slate-200 rounded-sm bg-slate-50"
        role="img" aria-label={`Plan view of ${label}`}>
        <rect x={pad} y={pad} width={L * scale} height={W * scale}
          fill="#FFFFFF" stroke="#94A3B8" strokeWidth="1" />
        {geometry.towers.map((t) => (
          <g key={t.id}>
            <rect x={pad + t.x * scale} y={pad + t.y * scale}
              width={Math.max(t.w * scale, 2)} height={Math.max(t.d * scale, 2)}
              fill="#2563EB" fillOpacity="0.75" stroke="#1D4ED8" strokeWidth="0.75" />
            <title>{`${t.name} — ${t.floors} floors, ${t.height_m} m, ${t.footprint_sqm} m² footprint`}</title>
          </g>
        ))}
      </svg>
      <div className="text-[10px] text-slate-500 leading-snug">
        {num(L, 0)} × {num(W, 0)} m · {geometry.towers.length} tower
        {geometry.towers.length === 1 ? "" : "s"} · {num(geometry.ground_coverage_pct, 1)}% covered
        {geometry.plot.basis !== "recorded plot dimensions" && (
          <> · <span className="text-amber-700">{geometry.plot.basis}</span></>
        )}
        {geometry.placement !== "as positioned" && (
          <> · <span className="text-amber-700">tower positions indicative</span></>
        )}
      </div>
    </div>
  );
}


export default function CollaborationModule({ projectId, setProject, readOnly }) {
  const [versions, setVersions] = useState([]);
  const [shares, setShares] = useState([]);
  const [activity, setActivity] = useState([]);
  const [label, setLabel] = useState("");
  const [shareEmail, setShareEmail] = useState("");
  const [shareRole, setShareRole] = useState("viewer");
  const [schemeA, setSchemeA] = useState("current");
  const [schemeB, setSchemeB] = useState("");
  const [compareResult, setCompareResult] = useState(null);
  const [comparing, setComparing] = useState(false);

  // Collaboration features state
  const [approvals, setApprovals] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [comments, setComments] = useState([]);
  const [automations, setAutomations] = useState([]);

  // Task form state
  const [newTaskTitle, setNewTaskTitle] = useState("");
  const [newTaskStage, setNewTaskStage] = useState("Design");
  const [newTaskPriority, setNewTaskPriority] = useState("medium");
  const [newTaskAssignee, setNewTaskAssignee] = useState("");

  // Comment form state
  const [newCommentText, setNewCommentText] = useState("");
  const [newCommentModule, setNewCommentModule] = useState("Design");
  const [replyTextMap, setReplyTextMap] = useState({});
  const [activeReplyId, setActiveReplyId] = useState(null);
  const [filterModule, setFilterModule] = useState("All");
  const [approvalNotes, setApprovalNotes] = useState({});

  const load = useCallback(async () => {
    try {
      const [v, s, act, app, tsk, cmt, aut] = await Promise.all([
        api.get(`/projects/${projectId}/versions`),
        api.get(`/projects/${projectId}/shares`),
        api.get(`/projects/${projectId}/activity`),
        api.get(`/projects/${projectId}/approvals`).catch(() => ({ data: [] })),
        api.get(`/projects/${projectId}/tasks`).catch(() => ({ data: [] })),
        api.get(`/projects/${projectId}/comments`).catch(() => ({ data: [] })),
        api.get(`/projects/${projectId}/automations`).catch(() => ({ data: [] })),
      ]);
      setVersions(v.data || []);
      setShares(s.data || []);
      setActivity(act.data || []);
      setApprovals(app.data || []);
      setTasks(tsk.data || []);
      setComments(cmt.data || []);
      setAutomations(aut.data || []);
    } catch (e) {
      toast.error(apiError(e.response?.data?.detail));
    }
  }, [projectId]);

  useEffect(() => {
    load();
  }, [load]);

  // The backend state machine is draft → submitted → approved | revisions_requested.
  // "Reject" is "request changes" — the gate keeps its history and returns to the
  // submitter, which is how a statutory sign-off actually cycles.
  const handleApprovalAction = async (approvalId, action) => {
    try {
      await api.post(`/projects/${projectId}/approvals/${approvalId}/action`, {
        action,
        notes: approvalNotes[approvalId] || `Action ${action} recorded`,
      });
      setApprovalNotes((prev) => ({ ...prev, [approvalId]: "" }));
      toast.success(`Workflow gate ${action.replace("_", " ")}d`);
      load();
    } catch (e) {
      toast.error(apiError(e.response?.data?.detail));
    }
  };

  const createTask = async () => {
    if (!newTaskTitle.trim()) return toast.error("Enter task title");
    try {
      await api.post(`/projects/${projectId}/tasks`, {
        title: newTaskTitle,
        stage: newTaskStage,
        priority: newTaskPriority,
        assigned_to: newTaskAssignee || "Unassigned",
        role: "engineer",
      });
      setNewTaskTitle("");
      setNewTaskAssignee("");
      toast.success("Task assigned");
      load();
    } catch (e) {
      toast.error(apiError(e.response?.data?.detail));
    }
  };

  const updateTaskStatus = async (taskId, status) => {
    try {
      await api.patch(`/projects/${projectId}/tasks/${taskId}`, { status });
      toast.success(`Task status: ${status}`);
      load();
    } catch (e) {
      toast.error(apiError(e.response?.data?.detail));
    }
  };

  const deleteTask = async (taskId) => {
    try {
      await api.delete(`/projects/${projectId}/tasks/${taskId}`);
      toast.success("Task removed");
      load();
    } catch (e) {
      toast.error(apiError(e.response?.data?.detail));
    }
  };

  const postComment = async () => {
    if (!newCommentText.trim()) return toast.error("Enter review comment");
    try {
      await api.post(`/projects/${projectId}/comments`, {
        content: newCommentText,
        module: newCommentModule,
        stage: newCommentModule,
        target_ref: "",
      });
      setNewCommentText("");
      toast.success("Review comment added");
      load();
    } catch (e) {
      toast.error(apiError(e.response?.data?.detail));
    }
  };

  const replyComment = async (commentId) => {
    const text = replyTextMap[commentId];
    if (!text?.trim()) return toast.error("Enter reply message");
    try {
      await api.post(`/projects/${projectId}/comments/${commentId}/reply`, {
        content: text,
      });
      setReplyTextMap((prev) => ({ ...prev, [commentId]: "" }));
      setActiveReplyId(null);
      toast.success("Reply recorded");
      load();
    } catch (e) {
      toast.error(apiError(e.response?.data?.detail));
    }
  };

  const toggleResolveComment = async (commentId, isResolved) => {
    try {
      await api.patch(`/projects/${projectId}/comments/${commentId}/resolve?resolved=${!isResolved}`);
      toast.success(!isResolved ? "Thread resolved" : "Thread reopened");
      load();
    } catch (e) {
      toast.error(apiError(e.response?.data?.detail));
    }
  };

  const triggerAutomations = async (trigger = "compliance_violation") => {
    try {
      const { data } = await api.post(`/projects/${projectId}/automations/trigger`, {
        trigger,
        context: { triggered_by: "user", at: new Date().toISOString() },
      });
      const executed = data.actions_executed || [];
      if (executed.length === 0) {
        toast.info(`No rules fired for "${trigger}"`);
      } else {
        toast.success(`Automation executed ${executed.length} action(s): ${executed.map((a) => a.result).join(" · ")}`);
      }
      load();
    } catch (e) {
      toast.error(apiError(e.response?.data?.detail));
    }
  };

  const saveVersion = async () => {
    if (!label.trim()) return toast.error("Enter a version label");
    try {
      await api.post(`/projects/${projectId}/versions`, { label });
      setLabel("");
      toast.success("Snapshot saved");
      load();
    } catch (e) {
      toast.error(apiError(e.response?.data?.detail));
    }
  };

  const restore = async (id) => {
    try {
      const { data } = await api.post(`/projects/${projectId}/versions/${id}/restore`);
      setProject(data);
      toast.success("Project rolled back");
      load();
    } catch (e) {
      toast.error(apiError(e.response?.data?.detail));
    }
  };

  const share = async () => {
    try {
      await api.post(`/projects/${projectId}/shares`, { email: shareEmail, role: shareRole });
      setShareEmail("");
      toast.success("Access granted");
      load();
    } catch (e) {
      toast.error(apiError(e.response?.data?.detail));
    }
  };

  const unshare = async (id) => {
    try {
      await api.delete(`/projects/${projectId}/shares/${id}`);
      toast.success("Access revoked");
      load();
    } catch (e) {
      toast.error(apiError(e.response?.data?.detail));
    }
  };

  const runCompare = async () => {
    if (!schemeA || !schemeB) return toast.error("Pick two schemes to compare");
    if (schemeA === schemeB) return toast.error("Pick two different schemes");
    setComparing(true);
    try {
      const { data } = await api.get(`/projects/${projectId}/versions/compare`, { params: { a: schemeA, b: schemeB } });
      setCompareResult(data);
    } catch (e) {
      toast.error(apiError(e.response?.data?.detail));
    } finally {
      setComparing(false);
    }
  };

  const schemeOptions = [{ id: "current", label: "Current project" }, ...versions.map((v) => ({ id: v.id, label: v.label }))];

  const filteredComments = filterModule === "All" 
    ? comments 
    : comments.filter((c) => c.module?.toLowerCase() === filterModule.toLowerCase());

  return (
    <div className="space-y-4">
      {/* 1. STAGE APPROVAL WORKFLOW */}
      <Section
        title="Stage Approval Workflow (IS & Statutory Gating)"
        description="5-Gate progressive signoffs with cryptographic audit certificates and role enforcement"
        testid="approvals-workflow-section"
      >
        <div className="grid grid-cols-1 md:grid-cols-5 gap-3">
          {approvals.map((app, idx) => {
            const isApproved = app.status === "approved";
            const isSubmitted = app.status === "submitted";
            const isRevisions = app.status === "revisions_requested";
            return (
              <div
                key={app.id || idx}
                className={`p-3 rounded-sm border ${
                  isApproved
                    ? "bg-emerald-50/60 border-emerald-300"
                    : isRevisions
                    ? "bg-rose-50/60 border-rose-300"
                    : isSubmitted
                    ? "bg-amber-50/60 border-amber-300"
                    : "bg-slate-50 border-slate-200"
                } flex flex-col justify-between space-y-2`}
                data-testid={`approval-gate-${app.stage?.toLowerCase().replace(/\s+/g, "-")}`}
              >
                <div>
                  <div className="flex items-center justify-between">
                    <span className="text-[10px] font-mono font-semibold uppercase text-slate-500">
                      Gate {idx + 1}
                    </span>
                    <span
                      className={`text-[10px] font-mono uppercase px-1.5 py-0.5 rounded ${
                        isApproved
                          ? "bg-emerald-100 text-emerald-800 font-semibold"
                          : isRevisions
                          ? "bg-rose-100 text-rose-800 font-semibold"
                          : isSubmitted
                          ? "bg-amber-100 text-amber-800 font-semibold"
                          : "bg-slate-200 text-slate-700"
                      }`}
                    >
                      {app.status === "revisions_requested" ? "changes requested" : app.status}
                    </span>
                  </div>
                  <div className="text-xs font-semibold text-slate-800 mt-1">{app.stage}</div>
                  <div className="text-[10px] text-slate-400 mt-1">
                    Reviewer: <span className="font-mono text-slate-600">admin / engineer</span>
                  </div>
                  {app.notes && (
                    <div className="text-[10px] text-slate-500 mt-1 italic">“{app.notes}”</div>
                  )}
                  {app.submitted_by && (
                    <div className="text-[10px] text-slate-500 mt-1">
                      Submitted by <span className="font-medium">{app.submitted_by}</span>
                      {app.submitted_at && <span className="font-mono"> · {dt(app.submitted_at)}</span>}
                    </div>
                  )}

                  {app.stamp && isApproved && (
                    <div className="mt-2 p-1.5 bg-white/80 border border-emerald-200 rounded text-[10px] text-emerald-900 space-y-0.5">
                      <div className="flex items-center gap-1 font-semibold">
                        <ShieldCheck className="h-3 w-3 text-emerald-600" /> Signed sign-off (HMAC-SHA256)
                      </div>
                      <div className="font-mono text-[9px] text-emerald-700 truncate">
                        Cert: {app.stamp.certificate_id}
                      </div>
                      <div className="text-[9px] text-slate-500">
                        Signed: {app.stamp.signer} ({app.stamp.role}) · {dt(app.stamp.verified_at)}
                      </div>
                    </div>
                  )}

                  {app.history?.length > 0 && (
                    <details className="mt-1.5">
                      <summary className="text-[10px] text-slate-400 cursor-pointer hover:text-slate-600">
                        {app.history.length} audit entr{app.history.length === 1 ? "y" : "ies"}
                      </summary>
                      <ul className="mt-1 space-y-0.5">
                        {app.history.map((h, hi) => (
                          <li key={hi} className="text-[9px] text-slate-500 font-mono">
                            {dt(h.at)} · {h.action} · {h.by}{h.role ? ` (${h.role})` : ""}
                            {h.notes ? ` — ${h.notes}` : ""}
                          </li>
                        ))}
                      </ul>
                    </details>
                  )}
                </div>

                {!readOnly && (
                  <div className="flex flex-wrap gap-1 pt-2 border-t border-slate-200">
                    {app.status === "draft" && (
                      <>
                        <Input
                          placeholder="Notes (optional)..."
                          value={approvalNotes[app.id] || ""}
                          onChange={(e) => setApprovalNotes((prev) => ({ ...prev, [app.id]: e.target.value }))}
                          className="h-6 text-[10px] rounded-sm w-full mb-1"
                        />
                        <Button
                          size="sm"
                          variant="outline"
                          className="h-6 text-[10px] px-2 rounded-sm w-full"
                          onClick={() => handleApprovalAction(app.id, "submit")}
                        >
                          Submit for review
                        </Button>
                      </>
                    )}
                    {app.status === "submitted" && (
                      <>
                        <Input
                          placeholder="Review notes..."
                          value={approvalNotes[app.id] || ""}
                          onChange={(e) => setApprovalNotes((prev) => ({ ...prev, [app.id]: e.target.value }))}
                          className="h-6 text-[10px] rounded-sm w-full mb-1"
                        />
                        <Button
                          size="sm"
                          className="h-6 text-[10px] px-2 rounded-sm bg-emerald-600 hover:bg-emerald-700 text-white flex-1"
                          onClick={() => handleApprovalAction(app.id, "approve")}
                        >
                          <Check className="h-3 w-3 mr-0.5" /> Approve
                        </Button>
                        <Button
                          size="sm"
                          variant="outline"
                          className="h-6 text-[10px] px-2 rounded-sm text-rose-600 border-rose-200 hover:bg-rose-50"
                          onClick={() => handleApprovalAction(app.id, "request_changes")}
                        >
                          Request changes
                        </Button>
                      </>
                    )}
                    {isRevisions && (
                      <>
                        <Input
                          placeholder="Revision notes..."
                          value={approvalNotes[app.id] || ""}
                          onChange={(e) => setApprovalNotes((prev) => ({ ...prev, [app.id]: e.target.value }))}
                          className="h-6 text-[10px] rounded-sm w-full mb-1"
                        />
                        <Button
                          size="sm"
                          variant="outline"
                          className="h-6 text-[10px] px-2 rounded-sm w-full"
                          onClick={() => handleApprovalAction(app.id, "submit")}
                        >
                          Re-submit
                        </Button>
                      </>
                    )}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </Section>

      {/* 2. TASK ASSIGNMENT & ACTION ITEMS */}
      <Section
        title="Task Assignment & Engineering Action Items"
        description="Assign, track, and close deliverables across multidisciplinary disciplines"
        testid="tasks-section"
      >
        {!readOnly && (
          <div className="grid grid-cols-1 sm:grid-cols-5 gap-2 mb-3">
            <Input
              placeholder="Task deliverable (e.g., Check IS 1893 shear walls)..."
              value={newTaskTitle}
              onChange={(e) => setNewTaskTitle(e.target.value)}
              className="sm:col-span-2 rounded-sm h-8 text-xs"
              data-testid="new-task-title-input"
            />
            <Select value={newTaskStage} onValueChange={setNewTaskStage}>
              <SelectTrigger className="rounded-sm h-8 text-xs">
                <SelectValue placeholder="Stage" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="Site">Site</SelectItem>
                <SelectItem value="Design">Design</SelectItem>
                <SelectItem value="Engineering">Engineering</SelectItem>
                <SelectItem value="Cost & BOQ">Cost &amp; BOQ</SelectItem>
                <SelectItem value="Deliver">Deliver</SelectItem>
              </SelectContent>
            </Select>
            <Select value={newTaskPriority} onValueChange={setNewTaskPriority}>
              <SelectTrigger className="rounded-sm h-8 text-xs">
                <SelectValue placeholder="Priority" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="low">Low Priority</SelectItem>
                <SelectItem value="medium">Medium Priority</SelectItem>
                <SelectItem value="high">High Priority</SelectItem>
                <SelectItem value="critical">Critical / Blocker</SelectItem>
              </SelectContent>
            </Select>
            <Button
              onClick={createTask}
              className="rounded-sm h-8 text-xs flex items-center justify-center gap-1"
              data-testid="create-task-button"
            >
              <Plus className="h-3.5 w-3.5" /> Assign Task
            </Button>
          </div>
        )}

        {tasks.length === 0 ? (
          <p className="text-sm text-slate-500">No active action items assigned.</p>
        ) : (
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Status</TableHead>
                <TableHead>Title</TableHead>
                <TableHead>Stage</TableHead>
                <TableHead>Priority</TableHead>
                <TableHead>Assignee</TableHead>
                <TableHead className="w-16" />
              </TableRow>
            </TableHeader>
            <TableBody>
              {tasks.map((task) => (
                <TableRow key={task.id} data-testid={`task-row-${task.id}`}>
                  <TableCell className="py-2">
                    <Select
                      value={task.status}
                      disabled={readOnly}
                      onValueChange={(val) => updateTaskStatus(task.id, val)}
                    >
                      <SelectTrigger className="h-7 w-28 text-[11px] rounded-sm">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="pending">Pending</SelectItem>
                        <SelectItem value="in_progress">In Progress</SelectItem>
                        <SelectItem value="review">In Review</SelectItem>
                        <SelectItem value="completed">Completed</SelectItem>
                      </SelectContent>
                    </Select>
                  </TableCell>
                  <TableCell className={`py-2 text-xs font-medium ${task.status === "completed" ? "line-through text-slate-400" : "text-slate-800"}`}>
                    {task.title}
                  </TableCell>
                  <TableCell className="py-2 text-xs">
                    <span className="bg-slate-100 text-slate-700 px-1.5 py-0.5 rounded font-mono text-[10px]">
                      {task.stage}
                    </span>
                  </TableCell>
                  <TableCell className="py-2 text-xs">
                    <span
                      className={`px-1.5 py-0.5 rounded text-[10px] font-semibold uppercase ${
                        task.priority === "critical"
                          ? "bg-rose-100 text-rose-800"
                          : task.priority === "high"
                          ? "bg-amber-100 text-amber-800"
                          : "bg-slate-100 text-slate-600"
                      }`}
                    >
                      {task.priority}
                    </span>
                  </TableCell>
                  <TableCell className="py-2 text-xs font-mono text-slate-600">
                    {task.assigned_to || "Unassigned"}
                  </TableCell>
                  <TableCell className="py-2">
                    {!readOnly && (
                      <Button
                        size="sm"
                        variant="ghost"
                        className="h-7 px-1 text-slate-400 hover:text-rose-600"
                        onClick={() => deleteTask(task.id)}
                      >
                        <Trash2 className="h-3.5 w-3.5" />
                      </Button>
                    )}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        )}
      </Section>

      {/* 3. COMMENTS & DISCUSSIONS */}
      <Section
        title="Comments & Stage Reviews"
        description="Threaded reviews linked to engineering disciplines and approval stages"
        testid="comments-section"
      >
        <div className="flex flex-wrap items-center justify-between gap-2 mb-3">
          <div className="flex items-center gap-2">
            <span className="text-xs text-slate-500">Filter discipline:</span>
            {["All", "Site", "Architecture", "Structure", "MEP", "Cost", "Compliance"].map((mod) => (
              <button
                key={mod}
                onClick={() => setFilterModule(mod)}
                className={`text-[11px] px-2 py-0.5 rounded-sm border ${
                  filterModule === mod
                    ? "bg-slate-900 text-white border-slate-900"
                    : "bg-slate-50 text-slate-600 border-slate-200 hover:bg-slate-100"
                }`}
              >
                {mod}
              </button>
            ))}
          </div>
        </div>

        {!readOnly && (
          <div className="flex gap-2 mb-4">
            <Select value={newCommentModule} onValueChange={setNewCommentModule}>
              <SelectTrigger className="w-36 h-8 text-xs rounded-sm">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="Site">Site</SelectItem>
                <SelectItem value="Design">Design</SelectItem>
                <SelectItem value="Engineering">Engineering</SelectItem>
                <SelectItem value="Cost & BOQ">Costing</SelectItem>
                <SelectItem value="Deliver">Deliver</SelectItem>
                <SelectItem value="General">General</SelectItem>
              </SelectContent>
            </Select>
            <Input
              placeholder="Add design review comment..."
              value={newCommentText}
              onChange={(e) => setNewCommentText(e.target.value)}
              className="flex-1 h-8 text-xs rounded-sm"
              data-testid="new-comment-input"
            />
            <Button onClick={postComment} className="h-8 text-xs rounded-sm shrink-0" data-testid="post-comment-button">
              <Send className="h-3.5 w-3.5 mr-1" /> Comment
            </Button>
          </div>
        )}

        {filteredComments.length === 0 ? (
          <p className="text-sm text-slate-500">No comments recorded for this discipline.</p>
        ) : (
          <div className="space-y-3">
            {filteredComments.map((comment) => (
              <div
                key={comment.id}
                className={`p-3 rounded-sm border ${
                  comment.resolved ? "bg-slate-50/50 border-slate-200 opacity-75" : "bg-white border-slate-200"
                } space-y-2`}
                data-testid={`comment-card-${comment.id}`}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-semibold text-slate-800">{comment.user_name}</span>
                    <span className="text-[10px] font-mono bg-blue-50 text-blue-700 px-1.5 py-0.5 rounded border border-blue-200">
                      {comment.module}
                    </span>
                    {comment.resolved && (
                      <span className="text-[10px] bg-emerald-100 text-emerald-800 px-1.5 py-0.2 rounded font-medium">
                        Resolved
                      </span>
                    )}
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-[10px] font-mono text-slate-400">{dt(comment.created_at)}</span>
                    {!readOnly && (
                      <button
                        onClick={() => toggleResolveComment(comment.id, comment.resolved)}
                        className="text-[10px] text-blue-600 hover:underline ml-1"
                      >
                        {comment.resolved ? "Reopen" : "Mark resolved"}
                      </button>
                    )}
                  </div>
                </div>
                <div className="text-xs text-slate-700">{comment.content}</div>

                {comment.replies?.length > 0 && (
                  <div className="ml-4 pl-3 border-l-2 border-slate-200 space-y-1.5 pt-1">
                    {comment.replies.map((reply) => (
                      <div key={reply.id} className="text-xs space-y-0.5">
                        <div className="flex items-center gap-2">
                          <span className="font-semibold text-[11px] text-slate-700">{reply.user_name}</span>
                          <span className="text-[10px] font-mono text-slate-400">{dt(reply.created_at)}</span>
                        </div>
                        <div className="text-slate-600">{reply.content}</div>
                      </div>
                    ))}
                  </div>
                )}

                {!readOnly && (
                  <div className="pt-1">
                    {activeReplyId === comment.id ? (
                      <div className="flex gap-1.5 mt-1 ml-4">
                        <Input
                          placeholder="Write reply..."
                          value={replyTextMap[comment.id] || ""}
                          onChange={(e) =>
                            setReplyTextMap((prev) => ({ ...prev, [comment.id]: e.target.value }))
                          }
                          className="h-7 text-xs rounded-sm flex-1"
                        />
                        <Button
                          size="sm"
                          className="h-7 text-xs rounded-sm"
                          onClick={() => replyComment(comment.id)}
                        >
                          Reply
                        </Button>
                        <Button
                          size="sm"
                          variant="ghost"
                          className="h-7 text-xs rounded-sm"
                          onClick={() => setActiveReplyId(null)}
                        >
                          Cancel
                        </Button>
                      </div>
                    ) : (
                      <button
                        onClick={() => setActiveReplyId(comment.id)}
                        className="text-[10px] text-slate-500 hover:text-slate-900 flex items-center gap-1 mt-1"
                      >
                        <CornerDownRight className="h-3 w-3" /> Reply
                      </button>
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </Section>

      {/* 4. WORKFLOW AUTOMATION ENGINE */}
      <Section
        title="Workflow Automation Engine"
        description="Event-driven rules triggering compliance remediation tasks and automatic gate invalidation"
        testid="automations-section"
        actions={
          !readOnly && (
            <Button
              size="sm"
              variant="outline"
              className="h-7 rounded-sm text-xs flex items-center gap-1 text-amber-700 border-amber-300 bg-amber-50 hover:bg-amber-100"
              onClick={triggerAutomations}
              data-testid="trigger-automations-button"
            >
              <Zap className="h-3 w-3 text-amber-600" /> Evaluate Rules Now
            </Button>
          )
        }
      >
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
          {(automations.length > 0 ? automations : []).map((rule) => (
            <div key={rule.id} className="p-3 bg-slate-50 border border-slate-200 rounded-sm space-y-1">
              <div className="flex items-center gap-1.5 text-xs font-semibold text-slate-800">
                {rule.trigger === "compliance_violation" && <AlertCircle className="h-3.5 w-3.5 text-rose-500" />}
                {rule.trigger === "layout_updated" && <RotateCcw className="h-3.5 w-3.5 text-blue-500" />}
                {rule.trigger === "stage_approved" && <ShieldCheck className="h-3.5 w-3.5 text-emerald-500" />}
                {rule.name}
              </div>
              <div className="text-[11px] text-slate-600 leading-snug">{rule.description}</div>
              <div className="flex items-center justify-between mt-1">
                <span className="text-[10px] font-mono text-slate-400">on: {rule.trigger}</span>
                <span className={`text-[10px] font-mono flex items-center gap-1 ${rule.enabled !== false ? "text-emerald-700" : "text-slate-400"}`}>
                  <CheckCircle2 className="h-3 w-3" /> {rule.enabled !== false ? "Active" : "Disabled"}
                </span>
              </div>
            </div>
          ))}
          {automations.length === 0 && (
            <div className="sm:col-span-3 text-sm text-slate-500">No automation rules configured.</div>
          )}
        </div>
        {!readOnly && (
          <div className="flex flex-wrap items-center gap-2 mt-3 pt-3 border-t border-slate-200">
            <span className="text-[11px] text-slate-500">Fire a rule now to verify the wiring:</span>
            <Button size="sm" variant="outline" className="h-7 rounded-sm text-xs text-rose-700 border-rose-200 hover:bg-rose-50"
              onClick={() => triggerAutomations("compliance_violation")} data-testid="trigger-compliance-automation">
              <Zap className="h-3 w-3 mr-1 text-rose-500" /> Compliance violation
            </Button>
            <Button size="sm" variant="outline" className="h-7 rounded-sm text-xs text-blue-700 border-blue-200 hover:bg-blue-50"
              onClick={() => triggerAutomations("layout_updated")} data-testid="trigger-layout-automation">
              <Zap className="h-3 w-3 mr-1 text-blue-500" /> Layout changed
            </Button>
            <Button size="sm" variant="outline" className="h-7 rounded-sm text-xs text-emerald-700 border-emerald-200 hover:bg-emerald-50"
              onClick={() => triggerAutomations("stage_approved")} data-testid="trigger-snapshot-automation">
              <Zap className="h-3 w-3 mr-1 text-emerald-500" /> Stage approved
            </Button>
          </div>
        )}
      </Section>

      <div className="grid lg:grid-cols-2 gap-4">
        <Section title="Project versions" description="Save named snapshots and roll back" testid="versions-section">
          {!readOnly && (
            <div className="flex gap-2 mb-3">
              <Input placeholder="e.g. Pre-approval scheme B" value={label} onChange={(e) => setLabel(e.target.value)}
                className="rounded-sm" data-testid="version-label-input" />
              <Button onClick={saveVersion} className="rounded-sm shrink-0" data-testid="save-version-button">
                <Save className="h-4 w-4 mr-1.5" /> Save snapshot
              </Button>
            </div>
          )}
          {versions.length === 0 ? (
            <p className="text-sm text-slate-500">No snapshots saved yet.</p>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Label</TableHead>
                  <TableHead>By</TableHead>
                  <TableHead>At</TableHead>
                  <TableHead className="w-24" />
                </TableRow>
              </TableHeader>
              <TableBody>
                {versions.map((v) => (
                  <TableRow key={v.id} data-testid={`version-row-${v.id}`}>
                    <TableCell className="py-2 font-medium">{v.label}</TableCell>
                    <TableCell className="py-2 text-xs">{v.user_name}</TableCell>
                    <TableCell className="py-2 text-xs font-mono">{dt(v.at)}</TableCell>
                    <TableCell className="py-2">
                      {!readOnly && (
                        <Button size="sm" variant="outline" className="h-7 rounded-sm text-xs"
                          data-testid={`restore-version-${v.id}`} onClick={() => restore(v.id)}>
                          <RotateCcw className="h-3 w-3 mr-1" /> Restore
                        </Button>
                      )}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </Section>

        <Section title="Project team" description="Share with registered users by role" testid="shares-section">
          {!readOnly && (
            <div className="flex gap-2 mb-3">
              <Input placeholder="user@example.com" value={shareEmail} onChange={(e) => setShareEmail(e.target.value)}
                className="rounded-sm" data-testid="share-email-input" />
              <Select value={shareRole} onValueChange={setShareRole}>
                <SelectTrigger className="w-32 rounded-sm" data-testid="share-role-select"><SelectValue /></SelectTrigger>
                <SelectContent>
                  <SelectItem value="viewer">Viewer</SelectItem>
                  <SelectItem value="engineer">Engineer</SelectItem>
                  <SelectItem value="admin">Admin</SelectItem>
                </SelectContent>
              </Select>
              <Button onClick={share} className="rounded-sm shrink-0" data-testid="share-submit-button">
                <UserPlus className="h-4 w-4" />
              </Button>
            </div>
          )}
          {shares.length === 0 ? (
            <p className="text-sm text-slate-500">Not shared with anyone yet.</p>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Email</TableHead>
                  <TableHead>Role</TableHead>
                  <TableHead className="w-12" />
                </TableRow>
              </TableHeader>
              <TableBody>
                {shares.map((s) => (
                  <TableRow key={s.id} data-testid={`share-row-${s.id}`}>
                    <TableCell className="py-2 font-mono text-xs">{s.email}</TableCell>
                    <TableCell className="py-2 uppercase font-mono text-xs">{s.role}</TableCell>
                    <TableCell className="py-2">
                      {!readOnly && (
                        <Button size="sm" variant="ghost" className="h-7 px-1 text-red-600"
                          data-testid={`unshare-${s.id}`} onClick={() => unshare(s.id)}>
                          <Trash2 className="h-3.5 w-3.5" />
                        </Button>
                      )}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </Section>
      </div>

      <Section title="Scheme Comparison" description="Compare the current project against any saved version — FAR, unit count, cost per flat and more, side by side" testid="scheme-comparison-section">
        <div className="flex flex-wrap items-end gap-2 mb-4">
          <div className="space-y-1">
            <div className="text-[11px] uppercase tracking-wide text-slate-500">Scheme A</div>
            <Select value={schemeA} onValueChange={setSchemeA}>
              <SelectTrigger className="w-56 rounded-sm" data-testid="compare-scheme-a-select"><SelectValue /></SelectTrigger>
              <SelectContent>
                {schemeOptions.map((s) => <SelectItem key={s.id} value={s.id}>{s.label}</SelectItem>)}
              </SelectContent>
            </Select>
          </div>
          <div className="space-y-1">
            <div className="text-[11px] uppercase tracking-wide text-slate-500">Scheme B</div>
            <Select value={schemeB} onValueChange={setSchemeB}>
              <SelectTrigger className="w-56 rounded-sm" data-testid="compare-scheme-b-select"><SelectValue placeholder="Select a version…" /></SelectTrigger>
              <SelectContent>
                {schemeOptions.map((s) => <SelectItem key={s.id} value={s.id}>{s.label}</SelectItem>)}
              </SelectContent>
            </Select>
          </div>
          <Button onClick={runCompare} disabled={comparing} className="rounded-sm" data-testid="run-compare-button">
            {comparing ? "Comparing…" : "Compare"}
          </Button>
        </div>

        {!compareResult ? (
          <p className="text-sm text-slate-500">
            {versions.length === 0
              ? "Save at least one snapshot above to compare it against the current project."
              : "Pick two schemes and click Compare."}
          </p>
        ) : (
          <>
          {compareResult.schemes[0].geometry && compareResult.schemes[1].geometry && (() => {
            // One scale across both plans, so a bigger plot draws bigger.
            const span = Math.max(
              ...compareResult.schemes.map((s) => Math.max(s.geometry.plot.length_m || 1,
                                                           s.geometry.plot.width_m || 1)));
            const scale = 260 / (span || 1);
            return (
              <div className="grid sm:grid-cols-2 gap-4 mb-4" data-testid="compare-plans">
                {compareResult.schemes.map((s) => (
                  <PlanView key={s.id} geometry={s.geometry} label={s.label} scale={scale} />
                ))}
              </div>
            );
          })()}
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Metric</TableHead>
                <TableHead className="text-right">{compareResult.schemes[0].label}</TableHead>
                <TableHead className="text-right">{compareResult.schemes[1].label}</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {compareResult.keys.map((k) => {
                const va = compareResult.schemes[0].metrics[k];
                const vb = compareResult.schemes[1].metrics[k];
                return (
                  <TableRow key={k} data-testid={`compare-row-${k.replace(/[^a-z0-9]/gi, "-").toLowerCase()}`}>
                    <TableCell className="py-1.5 text-slate-600">{k}</TableCell>
                    <TableCell className="py-1.5 text-right font-mono">{typeof va === "number" ? num(va, Number.isInteger(va) ? 0 : 2) : va}</TableCell>
                    <TableCell className="py-1.5 text-right font-mono">{typeof vb === "number" ? num(vb, Number.isInteger(vb) ? 0 : 2) : vb}</TableCell>
                  </TableRow>
                );
              })}
            </TableBody>
          </Table>
          </>
        )}

        {compareResult && (
          <div className="mt-4">
            <AiPanel
              title="AI comparison"
              description="Explains what the differences above mean in practice and which scheme is the stronger choice"
              endpoint={`/projects/${projectId}/ai/compare?a=${encodeURIComponent(schemeA)}&b=${encodeURIComponent(schemeB)}`}
              method="get"
              readOnly={readOnly}
              testid="ai-compare"
              buttonLabel="Explain the difference"
              emptyHint="Turn the metric table above into a recommendation, with the trade-offs each scheme is making."
            />
          </div>
        )}
      </Section>

      <Section title="Activity log" description="Who changed what and when" testid="activity-section">
        {activity.length === 0 ? (
          <p className="text-sm text-slate-500">No activity recorded.</p>
        ) : (
          <ul className="divide-y divide-slate-200">
            {activity.map((a) => (
              <li key={a.id} className="py-2 flex items-start gap-2 text-sm" data-testid={`activity-${a.id}`}>
                <History className="h-4 w-4 text-slate-400 mt-0.5 shrink-0" />
                <div className="flex-1 min-w-0">
                  <span className="font-medium">{a.user_name}</span>{" "}
                  <span className="font-mono text-xs bg-slate-100 px-1 rounded-sm">{a.action}</span>{" "}
                  <span className="text-slate-500">{a.detail}</span>
                </div>
                <span className="text-[11px] font-mono text-slate-400 shrink-0">{dt(a.at)}</span>
              </li>
            ))}
          </ul>
        )}
      </Section>
    </div>
  );
}
