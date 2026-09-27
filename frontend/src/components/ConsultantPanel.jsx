import { useEffect, useState } from "react";
import { toast } from "sonner";
import { Sparkles } from "lucide-react";
import { api, apiError } from "../lib/api";
import { Section } from "./Field";
import { Markdown } from "./AiPanel";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./ui/select";
import { dt } from "../lib/format";

// One topic, one structured memo -- the consultant answers a question the engineer
// already has, from figures the engine has already computed. Not a chat: no history,
// no follow-ups; for those there is the Apt copilot.
export default function ConsultantPanel({
  projectId,
  defaultTopic = "general",
  topics = null,          // optional subset of topic ids to offer
  readOnly = false,
  testid = "ai-consult",
}) {
  const [allTopics, setAllTopics] = useState([]);
  const [topic, setTopic] = useState(defaultTopic);
  const [question, setQuestion] = useState("");
  const [busy, setBusy] = useState(false);
  const [memo, setMemo] = useState(null);

  useEffect(() => {
    api.get("/ai/consult/topics")
      .then(({ data }) => {
        const list = topics ? data.filter((t) => topics.includes(t.id)) : data;
        setAllTopics(list);
        if (list.length && !list.some((t) => t.id === topic)) setTopic(list[0].id);
      })
      .catch(() => setAllTopics([]));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const run = async () => {
    setBusy(true);
    try {
      const { data } = await api.post(`/projects/${projectId}/ai/consult`, {
        topic, question: question.trim(),
      });
      setMemo(data);
      toast.success("Advisory memo generated");
    } catch (e) {
      toast.error(apiError(e.response?.data?.detail));
    } finally {
      setBusy(false);
    }
  };

  return (
    <Section
      title="AI Engineering Consultant"
      description="A topic-driven advisory memo grounded in this project's computed figures — pick a topic, add a specific question if you have one"
      testid={`${testid}-section`}
    >
      <div className="flex flex-col sm:flex-row gap-2">
        <Select value={topic} onValueChange={setTopic} disabled={readOnly || busy}>
          <SelectTrigger className="w-full sm:w-56 rounded-sm h-9" data-testid={`${testid}-topic`}>
            <SelectValue placeholder="Topic" />
          </SelectTrigger>
          <SelectContent>
            {allTopics.map((t) => (
              <SelectItem key={t.id} value={t.id}>{t.label}</SelectItem>
            ))}
          </SelectContent>
        </Select>
        <Input
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Optional — e.g. can we add two floors without breaking parking?"
          className="flex-1 rounded-sm h-9"
          disabled={readOnly || busy}
          data-testid={`${testid}-question`}
          onKeyDown={(e) => { if (e.key === "Enter" && !busy && !readOnly) run(); }}
        />
        <Button onClick={run} disabled={busy || readOnly} variant="ai" className="rounded-sm h-9"
          data-testid={`${testid}-run`}>
          <Sparkles className={`h-3.5 w-3.5 mr-1.5 ${busy ? "animate-pulse" : ""}`} />
          {busy ? "Consulting…" : memo ? "Re-consult" : "Consult"}
        </Button>
      </div>
      {memo ? (
        <div className="mt-3 border rounded-sm px-3 py-2" data-testid={`${testid}-memo`}>
          <Markdown text={memo.text} testid={`${testid}-memo-text`} />
          <p className="text-[11px] text-slate-400 font-mono mt-2">
            {memo.model} · {dt(memo.generated_at)}
          </p>
        </div>
      ) : (
        <p className="text-sm text-slate-500 mt-2">
          The memo cites only numbers the engine produced for this project — where data is missing it says so
          instead of guessing.
        </p>
      )}
    </Section>
  );
}
