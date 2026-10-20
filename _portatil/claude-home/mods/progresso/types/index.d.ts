export type StepStatus = 'done' | 'active' | 'pending'

export type Step = { label: string; status: StepStatus }

export type ReadInfo = {
  path: string
  isWhole: boolean
  totalLines: number
  chars: number
}

export type Tokens = {
  input: number
  output: number
  cacheRead: number
  cacheWrite: number
}

export type Tip = {
  title: string
  happened: string
  todo: string
  example: string
}

export type TaskStatus = 'running' | 'done' | 'interrupted' | 'error'

export type Task = {
  title: string
  promptChars: number
  startedAt: number
  endedAt: number | null
  status: TaskStatus
  /** Etapas vindas de TodoWrite/TaskCreate/TaskUpdate (vazio quando não há lista). */
  todos: Step[]
  /** Etapas de reserva: as ações do Claude. */
  actions: Step[]
  actionCount: number
  editCount: number
  exploreCount: number
  shellCount: number
  reads: ReadInfo[]
  /** Média móvel (s) no início da tarefa. */
  avgSec: number
  fiveHourStart: number | null
  fiveHourEnd: number | null
  tokens: Tokens | null
  contextPercent: number | null
  model: string | null
  tips: Tip[]
}

export type Window = { percent: number; resetsAt: string | null }

export type Limits = {
  fiveHour: Window | null
  sevenDay: Window | null
}

declare module 'claude-code' {
  interface PluginState {
    progresso: {
      task: Task | null
      limits: Limits
      model: string | null
      tick: number
      /** Painel aberto em detalhes (false = só a barrinha). */
      expanded: boolean
    }
  }
}
