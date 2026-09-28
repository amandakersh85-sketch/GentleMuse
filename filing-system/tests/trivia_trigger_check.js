// Runs the Code node that ships in daily-trivia-trigger.json the way n8n runs
// it, on 1 payload, and prints the verdict as JSON. No n8n needed. It runs the
// committed workflow, not the source file, so what is tested is what imports.
//
//   node trivia_trigger_check.js <workflow.json> <payload.json>
'use strict';
const fs = require('fs');

const [workflowPath, payloadPath] = process.argv.slice(2);
const workflow = JSON.parse(fs.readFileSync(workflowPath, 'utf8'));
const node = workflow.nodes.find((n) => n.name === 'Check the payload');
const body = JSON.parse(fs.readFileSync(payloadPath, 'utf8'));

// What the webhook node hands on: the request, with the JSON under body.
const call = {json: {headers: {}, params: {}, query: {}, body: body}};
const $input = {first: () => call, all: () => [call]};
const out = new Function('$input', node.parameters.jsCode)($input);
process.stdout.write(JSON.stringify(out[0].json) + '\n');
