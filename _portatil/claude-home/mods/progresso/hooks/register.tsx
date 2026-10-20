import { atom, read, update } from 'claude-code'
import type { EngineInterface, Register, Timer } from 'claude-code'

import type { Limits, ReadInfo, Step, Task, TaskStatus, Tip, Tokens, Window } from '../types'

const PANE = 'progresso'
const PANE_TITLE = 'Progresso'
const AVG_KEY = 'avgSec'
const DEFAULT_AVG = 90

const taskAtom = atom({ plugin: 'progresso', key: 'task' } as const, null)
const limitsAtom = atom({ plugin: 'progresso', key: 'limits' } as const, { fiveHour: null, sevenDay: null })
const modelAtom = atom({ plugin: 'progresso', key: 'model' } as const, null)
const tickAtom = atom({ plugin: 'progresso', key: 'tick' } as const, 0)
const expandedAtom = atom({ plugin: 'progresso', key: 'expanded' } as const, false)

const NEXT_STEPS = [
  'Próximos passos: ao final de uma resposta, se houver sugestões de próximos passos, NÃO as escreva como texto.',
  'Em vez disso, chame a ferramenta AskUserQuestion com a pergunta "Qual próximo passo você quer seguir?",',
  'de 2 a 3 opções específicas (label curto + description) e uma última opção "Sem preferência".',
  'Se a pessoa escolher "Sem preferência", siga com o que for mais útil ou encerre.',
  'Se não houver próximos passos relevantes, não pergunte. Escreva a pergunta e as opções na língua do usuário.',
].join(' ')

// O único valor de módulo: o handle do relógio (o resto vive em $.state).
let timer: Timer | undefined

type Engine = EngineInterface

// ---------- funções puras ----------

function fmtDuration(ms: number): string {
  const s = Math.max(0, Math.round(ms / 1000))
  if (s < 60) return `${s}s`
  const h = Math.floor(s / 3600)
  const m = Math.floor((s % 3600) / 60)
  const sec = s % 60
  if (h > 0) return `${h}h${String(m).padStart(2, '0')}m`
  return `${m}m${String(sec).padStart(2, '0')}s`
}

function friendlyModel(id: string | null): string {
  if (!id) return '—'
  const m = /claude-([a-z]+)-(\d+)-(\d+)/i.exec(id)
  if (!m) return id
  const name = m[1].charAt(0).toUpperCase() + m[1].slice(1)
  return `${name} ${m[2]}.${m[3]}`
}

function titleOf(text: string): string {
  const first = text.trim().split(/\r?\n/)[0] ?? ''
  return first.length > 70 ? `${first.slice(0, 69)}…` : first
}

function progressOf(task: Task): number {
  if (task.status !== 'running') return 100
  if (task.todos.length > 0) {
    const done = task.todos.filter(t => t.status === 'done').length
    const active = task.todos.filter(t => t.status === 'active').length
    return Math.min(95, Math.round((100 * (done + 0.5 * active)) / task.todos.length))
  }
  return Math.min(90, Math.round(100 * (1 - Math.exp(-task.actionCount / 10))))
}

function estimateTotalMs(task: Task, elapsedMs: number, pct: number): number {
  const avgMs = task.avgSec * 1000
  if (pct <= 15) return Math.max(avgMs, elapsedMs + 1000)
  const paceMs = elapsedMs / (pct / 100)
  const w = Math.min(1, (pct - 15) / 60)
  return Math.max(elapsedMs + 1000, (1 - w) * avgMs + w * paceMs)
}

function bar(pct: number, size: number): { full: string; empty: string } {
  const n = Math.max(0, Math.min(size, Math.round((pct / 100) * size)))
  return { full: '█'.repeat(n), empty: '░'.repeat(size - n) }
}

function limitColor(pct: number): string {
  if (pct >= 85) return 'error'
  if (pct >= 60) return 'warning'
  return 'success'
}

function windowOf(list: readonly { kind: string; percentUsed: number; resetsAt?: string }[], kind: string): Window | null {
  const one = list.find(r => r.kind === kind)
  return one ? { percent: one.percentUsed, resetsAt: one.resetsAt ?? null } : null
}

function categoryOf(tool: string): { label: string; kind: 'read' | 'edit' | 'shell' | 'search' | 'web' | 'agent' | 'other' } {
  if (tool === 'Read') return { label: 'Ler arquivo', kind: 'read' }
  if (tool === 'Edit' || tool === 'Write' || tool === 'MultiEdit' || tool === 'NotebookEdit') return { label: 'Editar arquivo', kind: 'edit' }
  if (tool === 'Bash' || tool === 'PowerShell') return { label: 'Comando no terminal', kind: 'shell' }
  if (tool === 'Grep' || tool === 'Glob') return { label: 'Buscar no código', kind: 'search' }
  if (tool === 'WebFetch' || tool === 'WebSearch') return { label: 'Pesquisar na web', kind: 'web' }
  if (tool === 'Agent' || tool === 'Task') return { label: 'Agente', kind: 'agent' }
  return { label: tool, kind: 'other' }
}

function shortPath(p: string): string {
  const parts = p.split(/[\\/]/)
  return parts.slice(-2).join('/')
}

function buildTips(task: Task): Tip[] {
  const tips: Tip[] = []
  const whole = task.reads.filter(r => r.isWhole && r.totalLines >= 400)
  if (whole.length > 0) {
    const big = whole.reduce((a, b) => (b.chars > a.chars ? b : a))
    tips.push({
      title: 'Arquivo grande lido inteiro',
      happened: `${whole.length} leitura(s) completa(s) de arquivo com 400+ linhas; a maior foi ${shortPath(big.path)} (${big.totalLines} linhas, ~${Math.round(big.chars / 4).toLocaleString('pt-BR')} tokens, estimativa).`,
      todo: 'Diga a parte do arquivo que interessa (função, seção ou trecho de linhas) para o Claude ler só ela.',
      example: `"No ${shortPath(big.path)}, olhe só a função X (perto da linha 200) e corrija o erro Y."`,
    })
  }
  const counts = new Map<string, number>()
  for (const r of task.reads) counts.set(r.path, (counts.get(r.path) ?? 0) + 1)
  const repeated = [...counts.entries()].filter(([, n]) => n >= 2)
  if (repeated.length > 0) {
    const [path, n] = repeated.reduce((a, b) => (b[1] > a[1] ? b : a))
    tips.push({
      title: 'Mesma leitura repetida',
      happened: `${repeated.length} arquivo(s) lido(s) mais de uma vez; ${shortPath(path)} foi lido ${n} vezes.`,
      todo: 'Junte numa mensagem só tudo o que precisa daquele arquivo, ou cole o trecho relevante no pedido.',
      example: `"Em ${shortPath(path)}, faça A, B e C de uma vez."`,
    })
  }
  if (task.model && /opus|fable/i.test(task.model) && task.actionCount <= 5 && task.editCount <= 1) {
    tips.push({
      title: 'Modelo pesado em tarefa simples',
      happened: `A tarefa usou ${friendlyModel(task.model)} com ${task.actionCount} ação(ões) e ${task.editCount} edição(ões).`,
      todo: 'Para tarefas curtas, troque para um modelo mais leve com /model (ex.: Sonnet) e volte ao pesado nas tarefas grandes.',
      example: '"/model sonnet" e depois: "Renomeie a variável x para total em calc.py."',
    })
  }
  if (task.contextPercent !== null && task.contextPercent >= 50) {
    const urgent = task.contextPercent >= 75
    tips.push({
      title: urgent ? 'Conversa longa (urgente)' : 'Conversa longa',
      happened: `O contexto da conversa está em ${Math.round(task.contextPercent)}%: cada mensagem nova reenvia todo esse histórico.`,
      todo: urgent
        ? 'Rode /compact agora, ou abra uma sessão nova com um resumo do que importa.'
        : 'Considere /compact ou uma sessão nova quando mudar de assunto.',
      example: '"/compact mantenha só as decisões e os arquivos alterados"',
    })
  }
  if (task.promptChars < 80 && task.exploreCount >= 8) {
    tips.push({
      title: 'Pedido vago gerou exploração demais',
      happened: `O pedido tinha ${task.promptChars} caracteres e a tarefa fez ${task.exploreCount} buscas/leituras/agentes para se localizar.`,
      todo: 'Diga onde está o que deve ser mudado (arquivo, pasta, nome da função) e o resultado esperado.',
      example: '"Em src/api/pedidos.ts, faça a função listar() aceitar o filtro por país e mostre o diff."',
    })
  }
  if (task.shellCount >= 12) {
    tips.push({
      title: 'Muitos comandos de terminal',
      happened: `${task.shellCount} comandos Bash/PowerShell nesta tarefa; cada saída entra no contexto.`,
      todo: 'Peça um script único que faça a sequência inteira, ou que os comandos rodem juntos com saída resumida.',
      example: '"Escreva um script que rode os 3 passos e imprima só o resumo final."',
    })
  }
  return tips
}

function newTask(text: string, startedAt: number, avgSec: number, fiveHour: number | null, model: string | null): Task {
  return {
    title: titleOf(text),
    promptChars: text.trim().length,
    startedAt,
    endedAt: null,
    status: 'running',
    todos: [],
    actions: [],
    actionCount: 0,
    editCount: 0,
    exploreCount: 0,
    shellCount: 0,
    reads: [],
    avgSec,
    fiveHourStart: fiveHour,
    fiveHourEnd: null,
    tokens: null,
    contextPercent: null,
    model,
    tips: [],
  }
}

function todosFrom(list: readonly { content?: unknown; status?: unknown; activeForm?: unknown }[]): Step[] {
  return list.map(t => ({
    label: String(t.status === 'in_progress' && t.activeForm ? t.activeForm : t.content ?? ''),
    status: t.status === 'completed' ? 'done' : t.status === 'in_progress' ? 'active' : 'pending',
  }))
}

// ---------- helpers que recebem $ (no topo, como async function) ----------

async function readLimits($: Engine): Promise<Limits> {
  const usage = await $.session.usage()
  return {
    fiveHour: windowOf(usage.rateLimits, 'five_hour'),
    sevenDay: windowOf(usage.rateLimits, 'seven_day'),
  }
}

async function contextPercent($: Engine): Promise<number | null> {
  const usage = await $.session.usage()
  return usage.context.percent ?? null
}

async function statusText($: Engine): Promise<string> {
  const task = await read($, taskAtom)
  const limits = await read($, limitsAtom)
  const now = await $.clock.now()
  const parts: string[] = []
  if (task) {
    if (task.status === 'running') parts.push(`progresso ${progressOf(task)}% · ${fmtDuration(now - task.startedAt)}`)
    else if (task.status === 'done') parts.push(`progresso ✓ Concluída em ${fmtDuration((task.endedAt ?? now) - task.startedAt)}`)
    else parts.push(task.status === 'error' ? '■ erro' : '■ interrompida')
  }
  parts.push(limits.fiveHour ? `5h ${Math.round(limits.fiveHour.percent)}%` : '5h: sem leitura')
  return parts.join(' | ')
}

async function refreshStatus($: Engine): Promise<void> {
  $.ui.status(await statusText($))
}

async function openPane($: Engine): Promise<void> {
  await $.ui.open({ id: PANE, title: PANE_TITLE }).catch(() => undefined)
}

async function finishTask($: Engine, status: TaskStatus, usage: (Tokens & { model: string | null }) | null): Promise<void> {
  const now = await $.clock.now()
  const limits = await readLimits($).catch(() => null)
  if (limits) await update($, limitsAtom, () => limits)
  const ctx = await contextPercent($).catch(() => null)
  const current = await read($, taskAtom)
  if (!current || current.status !== 'running') return
  const done: Task = {
    ...current,
    status,
    endedAt: now,
    todos: status === 'done' ? current.todos.map(t => ({ ...t, status: 'done' as const })) : current.todos,
    actions: current.actions.map(a => ({ ...a, status: 'done' as const })),
    fiveHourEnd: limits?.fiveHour?.percent ?? current.fiveHourEnd,
    tokens: usage ? { input: usage.input, output: usage.output, cacheRead: usage.cacheRead, cacheWrite: usage.cacheWrite } : current.tokens,
    contextPercent: ctx ?? current.contextPercent,
    model: usage?.model ?? current.model,
  }
  done.tips = buildTips(done)
  await update($, taskAtom, () => done)
  if (status === 'done') {
    const lastSec = Math.max(1, (now - current.startedAt) / 1000)
    const oldAvg = Number((await $.store.get(AVG_KEY)) ?? DEFAULT_AVG) || DEFAULT_AVG
    await $.store.set(AVG_KEY, 0.7 * oldAvg + 0.3 * lastSec)
  }
}

async function noteAction($: Engine, tool: string): Promise<void> {
  const cat = categoryOf(tool)
  await update($, taskAtom, t => {
    if (!t || t.status !== 'running') return t
    const actions = [...t.actions.map(a => ({ ...a, status: 'done' as const })), { label: cat.label, status: 'active' as const }].slice(-30)
    return {
      ...t,
      actions,
      actionCount: t.actionCount + 1,
      editCount: t.editCount + (cat.kind === 'edit' ? 1 : 0),
      shellCount: t.shellCount + (cat.kind === 'shell' ? 1 : 0),
      exploreCount: t.exploreCount + (cat.kind === 'search' || cat.kind === 'read' || cat.kind === 'agent' ? 1 : 0),
    }
  })
}

// ---------- registro ----------

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    const limits = await readLimits($).catch(() => null)
    if (limits) await update($, limitsAtom, () => limits)
    await refreshStatus($)
    return next(e)
  })

  on('session.measure', async ($, e, next) => {
    await update($, limitsAtom, () => ({
      fiveHour: windowOf(e.rateLimits, 'five_hour'),
      sevenDay: windowOf(e.rateLimits, 'seven_day'),
    }))
    const pct = e.context.percent
    if (pct !== undefined) {
      await update($, taskAtom, t => (t && t.status === 'running' ? { ...t, contextPercent: pct } : t))
    }
    return next(e)
  })

  on('prompt.compose', async ($, e, next) => {
    await update($, modelAtom, () => e.model)
    const composed = await next(e)
    const sections = composed.sections.filter(s => s.id !== 'progresso:proximos-passos')
    return { ...composed, sections: [...sections, { id: 'progresso:proximos-passos', text: NEXT_STEPS, scope: 'session' as const }] }
  })

  on('prompt.submit', async ($, e, next) => {
    const text = e.text.trim()
    const current = await read($, taskAtom)
    const isRunning = current !== null && current.status === 'running'
    const isIgnored =
      text === '' || text.startsWith('/') || e.turnId !== undefined || isRunning || e.origin?.kind === 'task-notification'
    if (isIgnored) return next(e)

    const now = await $.clock.now()
    const avg = Number((await $.store.get(AVG_KEY)) ?? DEFAULT_AVG) || DEFAULT_AVG
    const limits = await read($, limitsAtom)
    const model = await read($, modelAtom)
    await update($, taskAtom, () => newTask(text, now, avg, limits.fiveHour?.percent ?? null, model))

    timer?.cancel()
    timer = $.clock.every(1000, () => {
      void update($, tickAtom, n => n + 1)
      void refreshStatus($)
    })
    void openPane($)
    await refreshStatus($)
    return next(e)
  }).catch(($, e, next) => next(e))

  on('tool.call', async ($, e, next) => {
    const tool = String(e.tool)
    const task = await read($, taskAtom)
    if (!task || task.status !== 'running' || e.agentId !== undefined) return next(e)

    const input = e as unknown as Record<string, unknown>
    if (tool === 'TodoWrite' && Array.isArray(input.todos)) {
      const steps = todosFrom(input.todos as { content?: unknown; status?: unknown; activeForm?: unknown }[])
      await update($, taskAtom, t => (t && t.status === 'running' ? { ...t, todos: steps } : t))
      return next(e)
    }
    if (tool === 'TaskCreate') {
      const label = String(input.subject ?? input.title ?? input.description ?? 'Etapa')
      await update($, taskAtom, t =>
        t && t.status === 'running' ? { ...t, todos: [...t.todos, { label, status: 'pending' as const }] } : t,
      )
      return next(e)
    }
    if (tool === 'TaskUpdate') {
      const index = Number(input.taskId ?? input.id) - 1
      const st = String(input.status ?? '')
      await update($, taskAtom, t => {
        if (!t || t.status !== 'running' || !(index >= 0 && index < t.todos.length)) return t
        const status = st === 'completed' ? 'done' : st === 'in_progress' ? 'active' : t.todos[index].status
        return { ...t, todos: t.todos.map((s, i) => (i === index ? { ...s, status } : s)) }
      })
      return next(e)
    }

    await noteAction($, tool)
    const ran = await next(e)

    if (tool === 'Read' && ran.result !== undefined) {
      const file = (ran.result as { file?: { totalLines?: number; content?: string } }).file
      const info: ReadInfo = {
        path: String(input.file_path ?? ''),
        isWhole: input.offset === undefined && input.limit === undefined,
        totalLines: file?.totalLines ?? 0,
        chars: file?.content?.length ?? 0,
      }
      await update($, taskAtom, t => (t && t.status === 'running' ? { ...t, reads: [...t.reads, info] } : t))
    }
    return ran
  }).catch(($, e, next) => next(e))

  on('turn.complete', async ($, e, next) => {
    if (e.agentId !== undefined) return next(e)
    if (e.usage) await update($, modelAtom, () => e.usage?.model ?? null)
    const task = await read($, taskAtom)
    if (task && task.status === 'running') {
      const status: TaskStatus = e.isAborted || e.reason === 'aborted' ? 'interrupted' : e.reason === 'error' ? 'error' : 'done'
      const usage = e.usage
        ? {
            input: e.usage.input_tokens,
            output: e.usage.output_tokens,
            cacheRead: e.usage.cache_read_input_tokens,
            cacheWrite: e.usage.cache_creation_input_tokens,
            model: e.usage.model,
          }
        : null
      timer?.cancel()
      timer = undefined
      await finishTask($, status, usage)
      await refreshStatus($)
    }
    return next(e)
  })

  on('ui.render', { component: 'Pane', requestId: PANE }, async ($, e) => {
    const { Box, Text, Button } = $.ui.resolve(e)
    await read($, tickAtom)
    const task = await read($, taskAtom)
    const expanded = await read($, expandedAtom)
    if (!task) {
      return (
        <Box flexDirection="column">
          <Text dimColor>Nenhuma tarefa ainda. Envie um pedido para ver o progresso aqui.</Text>
        </Box>
      )
    }
    const now = await $.clock.now()
    const end = task.endedAt ?? now
    const elapsed = end - task.startedAt
    const pct = progressOf(task)
    const total = estimateTotalMs(task, elapsed, pct)
    const width = Math.max(10, Math.min(40, (e.props.bodyColumns ?? 40) - 12))
    const b = bar(pct, width)
    const steps = task.todos.length > 0 ? task.todos : task.actions.slice(-12)
    const isRunning = task.status === 'running'
    const fiveDelta =
      task.fiveHourStart !== null && task.fiveHourEnd !== null ? task.fiveHourEnd - task.fiveHourStart : null

    const toggle = (
      <Button
        key="detalhes"
        label={expanded ? '▾ recolher' : '▸ detalhes'}
        onPress={() => update($, expandedAtom, v => !v)}
      />
    )
    const barLine = (
      <Box gap={1}>
        <Box>
          <Text color="success">{b.full}</Text>
          <Text dimColor>{b.empty}</Text>
          <Text> {pct}%</Text>
        </Box>
        {toggle}
      </Box>
    )
    // Recolhido (padrão): só a barrinha verde; o resto aparece ao clicar em «detalhes».
    if (!expanded) return barLine

    return (
      <Box flexDirection="column">
        <Text bold wrap="truncate-end">{task.title || '(sem título)'}</Text>
        {barLine}
        {isRunning ? (
          <Box flexDirection="column">
            <Text>Decorrido: {fmtDuration(elapsed)}</Text>
            <Text dimColor>
              Total ~{fmtDuration(total)} · faltam ~{fmtDuration(total - elapsed)} (estimativa)
            </Text>
          </Box>
        ) : task.status === 'done' ? (
          <Text color="success" bold>✓ Concluída em {fmtDuration(elapsed)}</Text>
        ) : (
          <Text color="warning" bold>
            {task.status === 'error' ? '■ Terminou com erro' : '■ Interrompida'} após {fmtDuration(elapsed)}
          </Text>
        )}
        <Text> </Text>
        <Text bold>{task.todos.length > 0 ? 'Etapas' : 'Ações do Claude'}</Text>
        {steps.length === 0 && <Text dimColor>Aguardando a primeira ação…</Text>}
        {steps.map(s => (
          <Text color={s.status === 'done' ? 'success' : undefined} dimColor={s.status === 'pending'} wrap="truncate-end">
            {s.status === 'done' ? '✓' : s.status === 'active' ? '▶' : '○'} {s.label}
          </Text>
        ))}
        {!isRunning && (
          <Box flexDirection="column">
            <Text> </Text>
            <Text bold>Consumo</Text>
            <Text>
              Limite de 5h:{' '}
              {fiveDelta === null ? 'sem leitura' : fiveDelta < 1 ? 'menos de 1% do plano' : `≈ ${Math.round(fiveDelta)}% do plano`}
            </Text>
            {task.tokens ? (
              <Text>
                Tokens (API, exatos): entrada {task.tokens.input.toLocaleString('pt-BR')} · saída{' '}
                {task.tokens.output.toLocaleString('pt-BR')} · cache lido {task.tokens.cacheRead.toLocaleString('pt-BR')} · cache
                gravado {task.tokens.cacheWrite.toLocaleString('pt-BR')}
              </Text>
            ) : (
              <Text dimColor>Tokens: a API não informou para esta tarefa.</Text>
            )}
            <Text dimColor>A % do limite pode incluir outro uso seu no mesmo período.</Text>
            <Text> </Text>
            <Text bold>Como gastar menos tokens</Text>
            {task.tips.length === 0 && <Text color="success">Nada a melhorar nesta tarefa.</Text>}
            {task.tips.map(t => (
              <Box flexDirection="column">
                <Text color="warning" bold>• {t.title}</Text>
                <Text>O que ocorreu: {t.happened}</Text>
                <Text>O que fazer: {t.todo}</Text>
                <Text dimColor>Exemplo: {t.example}</Text>
              </Box>
            ))}
            <Text dimColor>Valores com "~" ou "estimativa" são aproximados (caracteres ÷ 4); os tokens por turno vindos da API são exatos.</Text>
          </Box>
        )}
      </Box>
    )
  })

  on('ui.render', { component: 'AbovePrompt' }, async ($, e, next) => {
    if (e.props.hasSurvey) return next(e)
    const { Box, Text, Button } = $.ui.resolve(e)
    await read($, tickAtom)
    const task = await read($, taskAtom)
    const limits = await read($, limitsAtom)
    const model = await read($, modelAtom)
    const now = await $.clock.now()

    const five = limits.fiveHour
    const fiveBar = five ? bar(five.percent, 10) : null
    const resetMs = five?.resetsAt ? Date.parse(five.resetsAt) - now : NaN
    const fiveDelta =
      task && task.status !== 'running' && task.fiveHourStart !== null && task.fiveHourEnd !== null
        ? task.fiveHourEnd - task.fiveHourStart
        : null

    return (
      <Box flexDirection="row" gap={2}>
        {task && task.status === 'running' && (
          <Text>
            progresso {progressOf(task)}% · {fmtDuration(now - task.startedAt)}
          </Text>
        )}
        {task && task.status === 'done' && (
          <Text color="success">progresso ✓ Concluída em {fmtDuration((task.endedAt ?? now) - task.startedAt)}</Text>
        )}
        {task && (task.status === 'interrupted' || task.status === 'error') && (
          <Text color="warning">{task.status === 'error' ? '■ erro' : '■ interrompida'}</Text>
        )}
        {five && fiveBar ? (
          <Box>
            <Text color={limitColor(five.percent)}>● </Text>
            <Text>5h </Text>
            <Text color={limitColor(five.percent)}>{fiveBar.full}</Text>
            <Text dimColor>{fiveBar.empty}</Text>
            <Text> {Math.round(five.percent)}%</Text>
            {Number.isFinite(resetMs) && resetMs > 0 && <Text dimColor> · renova em {fmtDuration(resetMs)}</Text>}
          </Box>
        ) : (
          <Text dimColor>5h: sem leitura</Text>
        )}
        <Text dimColor>{friendlyModel(model)}</Text>
        {fiveDelta !== null && (
          <Text dimColor>esta tarefa: {fiveDelta < 1 ? 'menos de 1% do plano' : `≈${Math.round(fiveDelta)}% do plano`}</Text>
        )}
        <Button key="painel" label="painel" onPress={() => openPane($)} />
      </Box>
    )
  })
}
