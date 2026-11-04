import test from 'node:test';import assert from 'node:assert/strict';
test('API package exposes the required scripts',async()=>{const p=await import('../package.json',{with:{type:'json'}});assert.equal(p.default.scripts.start,'node src/server.js');assert.ok(p.default.dependencies.express);});
