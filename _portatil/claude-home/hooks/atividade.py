"""Hook do Claude Code: registra cada ação (ferramenta, pedido, fim) em painel/atividade.jsonl,
lido pelo feed "Ao vivo" do painel (http://127.0.0.1:8765). Nunca bloqueia nem falha a sessão."""
import json, os, sys, time
from pathlib import Path

ARQ = Path(r"C:\Users\PICHAU\Downloads\Produtividade com ia\painel\atividade.jsonl")
MAX_BYTES, MANTER = 300_000, 400


def resumo(ferr, ent):
    ent = ent or {}
    if ferr in ("Bash", "PowerShell"):
        return ent.get("description") or ent.get("command", "")
    if ferr in ("Read", "Write", "Edit", "NotebookEdit"):
        return ent.get("file_path") or ent.get("notebook_path", "")
    if ferr in ("Grep", "Glob"):
        return f'{ent.get("pattern", "")}  {ent.get("path", "")}'.strip()
    if ferr == "Agent":
        return f'{ent.get("subagent_type", "agente")}: {ent.get("description", "")}'
    if ferr == "Skill":
        return ent.get("skill", "")
    for k in ("description", "query", "url", "prompt", "title", "name", "action"):
        if isinstance(ent.get(k), str) and ent[k]:
            return ent[k]
    return ""


def main():
    try:
        d = json.loads(sys.stdin.buffer.read().decode("utf-8", "replace") or "{}")
    except Exception:
        return
    ev = d.get("hook_event_name", "")
    ferr = d.get("tool_name", "")
    reg = {"t": time.time(), "ev": ev, "sessao": (d.get("session_id") or "")[:8],
           "pasta": os.path.basename(d.get("cwd") or ""), "id": d.get("tool_use_id", ""),
           "agente": d.get("agent_type") or d.get("agent_id") or ""}
    if ev in ("PreToolUse", "PostToolUse", "PostToolUseFailure"):
        reg["ferr"] = ferr.replace("mcp__claude_ai_", "").replace("mcp__", "")
        reg["txt"] = str(resumo(ferr, d.get("tool_input")))[:220]
        resp = d.get("tool_response")
        if isinstance(resp, dict) and (resp.get("is_error") or resp.get("interrupted")):
            reg["erro"] = True
        if ev == "PostToolUseFailure":
            reg["erro"] = True
    elif ev == "UserPromptSubmit":
        reg["txt"] = (d.get("prompt") or "")[:220]
    elif ev in ("Stop", "SubagentStop", "Notification"):
        reg["txt"] = (d.get("message") or "")[:220]
    linha = json.dumps(reg, ensure_ascii=False) + "\n"
    try:
        with open(ARQ, "a", encoding="utf-8") as f:
            f.write(linha)
        if ARQ.stat().st_size > MAX_BYTES:
            linhas = ARQ.read_text(encoding="utf-8").splitlines(True)[-MANTER:]
            tmp = ARQ.with_suffix(".tmp")
            tmp.write_text("".join(linhas), encoding="utf-8")
            os.replace(tmp, ARQ)
    except Exception:
        pass


if __name__ == "__main__":
    main()
