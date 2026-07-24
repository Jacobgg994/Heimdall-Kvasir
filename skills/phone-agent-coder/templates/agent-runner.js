/**
 * agent-runner.js — minimal per-phone agent loop.
 *
 * Polls a Postgres `agent_tasks` queue, claims one task, calls the Claude API,
 * writes the result back. Idempotent and crash-safe.
 *
 * Run:
 *   node agent-runner.js               # forever loop
 *   node agent-runner.js --once        # one task then exit (good for cron)
 *   node agent-runner.js --once --dry-run
 */
import 'dotenv/config';
import os from 'node:os';
import process from 'node:process';
import { Client as PgClient } from 'pg';
import Anthropic from '@anthropic-ai/sdk';

const PHONE_ID = process.env.PHONE_ID === 'auto' || !process.env.PHONE_ID
  ? os.hostname()
  : process.env.PHONE_ID;

const DEFAULT_MODEL = process.env.DEFAULT_MODEL ?? 'claude-haiku-4-5-20251001';

const args = new Set(process.argv.slice(2));
const ONCE = args.has('--once');
const DRY  = args.has('--dry-run');

const anthropic = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });

async function pg() {
  const c = new PgClient({
    host: process.env.PG_HOST, port: +process.env.PG_PORT,
    user: process.env.PG_USER, password: process.env.PG_PASSWORD,
    database: process.env.PG_DATABASE,
  });
  await c.connect();
  return c;
}

/** Claim one queued task atomically. Returns null if none available. */
async function claim(pg) {
  const r = await pg.query(`
    UPDATE agent_tasks
       SET status      = 'running',
           phone_id    = COALESCE(phone_id, $1),
           attempts    = attempts + 1,
           started_at  = now()
     WHERE id = (
       SELECT id FROM agent_tasks
        WHERE status = 'queued'
          AND (phone_id IS NULL OR phone_id = $1)
        ORDER BY created_at ASC
        LIMIT 1
        FOR UPDATE SKIP LOCKED
     )
     RETURNING id, kind, prompt, context, model;`, [PHONE_ID]);
  return r.rows[0] ?? null;
}

async function complete(pg, id, result) {
  await pg.query(`
    UPDATE agent_tasks
       SET status = 'done', result = $2::jsonb, finished_at = now()
     WHERE id = $1;`, [id, JSON.stringify(result)]);
}

async function fail(pg, id, error) {
  await pg.query(`
    UPDATE agent_tasks
       SET status = CASE WHEN attempts >= 3 THEN 'failed' ELSE 'queued' END,
           error_message = $2, finished_at = now()
     WHERE id = $1;`, [id, String(error?.message ?? error).slice(0, 1000)]);
}

async function runOne() {
  const c = await pg();
  try {
    const task = await claim(c);
    if (!task) {
      console.log(`[${PHONE_ID}] no work`);
      return false;
    }
    console.log(`[${PHONE_ID}] task ${task.id} (${task.kind})`);

    if (DRY) {
      await complete(c, task.id, { dryRun: true, phoneId: PHONE_ID });
      return true;
    }

    const model = task.model ?? DEFAULT_MODEL;
    const ctx = typeof task.context === 'string' ? JSON.parse(task.context) : (task.context ?? {});
    const systemPrompt = ctx.system ?? 'You are a focused coding/content agent on a Thai-market growth team. Be concise.';
    const userBlocks = [];
    if (typeof task.prompt === 'string') userBlocks.push({ type: 'text', text: task.prompt });
    if (Array.isArray(ctx.attachments)) {
      for (const a of ctx.attachments) userBlocks.push({ type: 'text', text: `--- attachment: ${a.name} ---\n${a.body}` });
    }

    const t0 = Date.now();
    const resp = await anthropic.messages.create({
      model,
      max_tokens: ctx.maxTokens ?? 2000,
      system: systemPrompt,
      messages: [{ role: 'user', content: userBlocks }],
    });
    const ms = Date.now() - t0;

    const text = resp.content
      .filter((b) => b.type === 'text')
      .map((b) => b.text)
      .join('\n')
      .trim();

    await complete(c, task.id, {
      phoneId: PHONE_ID,
      model,
      latencyMs: ms,
      usage: resp.usage,
      output: text,
    });
    console.log(`[${PHONE_ID}] task ${task.id} done in ${ms}ms (${resp.usage.input_tokens} in / ${resp.usage.output_tokens} out)`);
    return true;
  } catch (err) {
    console.error(`[${PHONE_ID}] error:`, err.message);
    // Try to mark the most recent running task as failed; best-effort.
    try {
      const r = await c.query(
        `SELECT id FROM agent_tasks WHERE phone_id = $1 AND status='running' ORDER BY started_at DESC LIMIT 1`,
        [PHONE_ID]);
      if (r.rows[0]) await fail(c, r.rows[0].id, err);
    } catch {}
    return false;
  } finally {
    await c.end();
  }
}

async function loop() {
  let backoff = 1000;
  while (true) {
    const did = await runOne();
    if (did) backoff = 1000;
    else     backoff = Math.min(backoff * 2, 30_000);
    await new Promise((r) => setTimeout(r, did ? 250 : backoff));
  }
}

(ONCE ? runOne() : loop()).catch((e) => { console.error(e); process.exit(1); });
