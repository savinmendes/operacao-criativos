import { expect, mock, test } from 'claude-code/testing'

const PANE_PROPS = {
  title: 'Progresso',
  isFocused: false,
  bodyColumns: 60,
  placement: 'dock' as const,
  scroll: { offset: 0, bodyRows: 40 },
  view: {},
}

const USAGE = {
  startedAt: 0,
  context: { window: 200000, tokens: 20000, percent: 10 },
  rateLimits: [{ kind: 'five_hour', percentUsed: 40, resetsAt: '2026-10-14T20:00:00Z' }],
}

test('prompt.compose recebe a seção de próximos passos', async ($, on) => {
  mock.clock(on)
  mock.store(on)
  on('prompt.compose', () => ({ sections: [{ id: 'intro', text: 'base', scope: 'shared' as const }] }))

  const composed = await $.prompt.compose({
    model: 'claude-sonnet-5-5',
    promptModel: 'claude-sonnet-5-5',
    surfaces: ['desktop'],
    tools: ['AskUserQuestion'],
    outputStyle: null,
    traits: [],
  })
  const mine = composed.sections.find(s => s.id === 'progresso:proximos-passos')

  expect(mine).toBeDefined()
  expect(mine?.scope).toBe('session')
  expect(mine?.text).toMatch(/AskUserQuestion/)
  expect(mine?.text).toMatch(/Sem preferência/)
})

test('o painel mostra o título ao enviar e "Concluída" ao terminar', async ($, on) => {
  const clock = mock.clock(on, { now: 1_000_000 })
  mock.store(on)
  on('session.usage', () => ({ value: USAGE }))
  on('ui.open', () => ({ value: { isPlaced: true as const } }))
  on('ui.status', () => ({ value: undefined }))
  on('prompt.submit', ($, e) => ({ text: e.text }))
  on('turn.complete', () => ({ text: '' }))

  await $.prompt.submit({ text: 'Gerar relatório de vendas do Chile\ncom detalhes' })

  const ui = await $.ui.mount({ plugin: 'progresso', surface: 'desktop', component: 'Pane', props: PANE_PROPS, requestId: 'progresso' })
  // Recolhido por padrão: só a barrinha, sem o título.
  expect(await ui.find({ type: 'Text', text: /%/ })).toBeDefined()
  expect(await ui.find({ type: 'Text', text: /Gerar relatório de vendas do Chile/ })).toBeUndefined()
  await ui.press({ key: 'detalhes' })
  expect(await ui.find({ type: 'Text', text: /Gerar relatório de vendas do Chile/ })).toBeDefined()

  await clock.advance(110_000)
  await $.turn.complete({
    answer: 'pronto',
    durationMs: 110_000,
    isAborted: false,
    turnId: 't1',
    reason: 'answer',
    usage: {
      model: 'claude-sonnet-5-5',
      input_tokens: 1200,
      output_tokens: 300,
      cache_read_input_tokens: 5000,
      cache_creation_input_tokens: 800,
    },
  })

  expect(await ui.find({ type: 'Text', text: /Concluída em 1m50s/ })).toBeDefined()
  expect(await ui.find({ type: 'Text', text: /Consumo/ })).toBeDefined()
  await ui.unmount()
})
