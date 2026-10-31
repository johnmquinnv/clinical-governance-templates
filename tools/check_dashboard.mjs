// SPDX-License-Identifier: MIT
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import vm from 'node:vm';
const html=readFileSync(new URL('../data-demo/dashboard.html',import.meta.url),'utf8');
function element(){return {value:'All',textContent:'',children:[],addEventListener(){},append(...nodes){this.children.push(...nodes);},replaceChildren(...nodes){this.children=nodes;}};}
const elements=new Map();
const context={document:{getElementById(id){if(!elements.has(id))elements.set(id,element());return elements.get(id);},createElement:element},window:{print(){}},Blob,URL,setTimeout};
vm.createContext(context);
vm.runInContext(html.match(/<script>([\s\S]*?)<\/script>/)[1],context);
const read=expression=>JSON.parse(vm.runInContext(`JSON.stringify(${expression})`,context));
const rows=read('records');
assert.equal(rows.length,8);assert.equal(new Set(rows.map(r=>r.id)).size,8);
for(const r of rows){assert.ok(['Alpha','Beta'].includes(r.team));for(const k of ['reviewed','handover','action','closed','overdue'])assert.equal(typeof r[k],'boolean');assert.ok(!r.closed||r.action);assert.ok(!r.overdue||(r.action&&!r.closed));}
assert.deepEqual(read('summarize(records)'),{n:8,reviewed:6,handover:5,actions:5,closed:2,overdue:2});
const expected={Alpha:{n:4,reviewed:3,handover:3,actions:2,closed:1,overdue:1},Beta:{n:4,reviewed:3,handover:2,actions:3,closed:1,overdue:1}};
for(const team of ['Alpha','Beta']){elements.get('team').value=team;vm.runInContext('render()',context);assert.deepEqual(read('summarize(selectedRecords())'),expected[team]);assert.equal(elements.get('rows').children.length,4);assert.equal(read('csvFor(selectedRecords())').trim().split('\r\n').length,5);}
assert.equal(read('percent(1,0)'),'Not applicable');assert.deepEqual(read('summarize([])'),{n:0,reviewed:0,handover:0,actions:0,closed:0,overdue:0});
elements.get('team').value='All';vm.runInContext('render()',context);assert.equal(elements.get('rows').children.length,8);assert.equal(read('csvFor(selectedRecords())').trim().split('\r\n').length,9);assert.equal(elements.get('cards').children[2].children[1].textContent,'62.5%');
console.log('PASS: synthetic data invariants, all/team/empty calculations, filter rendering, CSV rows and denominators');
