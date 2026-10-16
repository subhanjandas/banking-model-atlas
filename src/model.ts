import raw from '../model/banking.model.json';
export type Domain = typeof raw.domains[number];
export type Entity = typeof raw.entities[number];
export type Column = Entity['columns'][number];
export type Relationship = typeof raw.relationships[number];
export type Journey = typeof raw.journeys[number];
export const model = raw;
export const entityById = new Map(model.entities.map(e=>[e.id,e]));
export const domainById = new Map(model.domains.map(d=>[d.id,d]));
export const relationshipById = new Map(model.relationships.map(r=>[r.id,r]));
export type ViewState = {view:'domains'|'tables';domain:string;entity:string;edge:string;journey:string;focus:string;column:string};
export const initialState:ViewState={view:'domains',domain:'',entity:'',edge:'',journey:'',focus:'',column:''};
export function parseState(search:string):{state:ViewState;invalid:boolean} {
 const q=new URLSearchParams(search),s={...initialState};let invalid=false;
 if(q.has('view')){if(['domains','tables'].includes(q.get('view')!))s.view=q.get('view') as ViewState['view'];else invalid=true;}
 for(const [key,valid] of [['domain',domainById],['entity',entityById],['edge',relationshipById],['journey',new Map(model.journeys.map(j=>[j.id,j]))],['focus',entityById]] as const){const v=q.get(key);if(v){if(valid.has(v))s[key]=v;else invalid=true;}}
 if(s.journey){s.domain='';s.focus='';s.view='tables';}
 if(s.focus){s.domain='';s.view='tables';}
 if(s.entity){s.view='tables';s.edge='';if(s.domain&&entityById.get(s.entity)?.domain!==s.domain)s.domain='';const j=model.journeys.find(j=>j.id===s.journey);if(j&&!j.steps.some(x=>x.entity===s.entity))s.journey='';if(s.focus&&!neighbours(s.focus).has(s.entity))s.focus='';}
 if(s.edge){s.view='tables';const r=relationshipById.get(s.edge)!;if(s.domain&&[r.source_entity,r.target_entity].some(id=>entityById.get(id)?.domain!==s.domain))s.domain='';const j=model.journeys.find(j=>j.id===s.journey);if(j&&!j.relationship_ids.includes(s.edge))s.journey='';if(s.focus&&[r.source_entity,r.target_entity].some(id=>!neighbours(s.focus).has(id)))s.focus='';}
 if(q.get('column')){if(entityById.get(s.entity)?.columns.some(c=>c.id===q.get('column')))s.column=q.get('column')!;else invalid=true;}
 return {state:s,invalid};
}
export function serializeState(s:ViewState){const q=new URLSearchParams();if(s.view!=='domains')q.set('view',s.view);for(const k of ['domain','entity','edge','journey','focus','column'] as const)if(s[k])q.set(k,s[k]);return q.toString();}
export function neighbours(id:string){const ids=new Set([id]);model.relationships.forEach(r=>{if(r.source_entity===id)ids.add(r.target_entity);if(r.target_entity===id)ids.add(r.source_entity);});return ids;}
export function visibleModel(s:ViewState){
 const journey=model.journeys.find(j=>j.id===s.journey);
 const ids=journey?new Set(journey.steps.map(s=>s.entity)):s.focus?neighbours(s.focus):new Set(model.entities.filter(e=>!s.domain||e.domain===s.domain).map(e=>e.id));
 const entities=model.entities.filter(e=>ids.has(e.id));
 const relationships=model.relationships.filter(r=>ids.has(r.source_entity)&&ids.has(r.target_entity)&&(!journey||journey.relationship_ids.includes(r.id)));
 const omitted=model.relationships.filter(r=>ids.has(r.source_entity)!==ids.has(r.target_entity)).length;
 return {entities,relationships,omitted};
}
export function searchModel(query:string){const q=query.trim().toLowerCase();if(!q)return [];return model.entities.flatMap(e=>{const cols=e.columns.filter(c=>(c.id+' '+c.description).toLowerCase().includes(q));const name=(e.id+' '+e.label).toLowerCase().includes(q);return name||cols.length?[{entity:e,columns:cols,nameMatch:name}]:[];});}
export function dictionary(){
 return '# Banking Model Atlas — data dictionary\n\nModel '+model.model_version+' · '+model.scenario+'\n\n'+model.entities.map(e=>'## '+e.label+' (`'+e.id+'`)\n\n'+e.description+'\n\nGrain: '+e.grain+'\n\n| Column | Type | Nullable | Definition |\n|---|---|---|---|\n'+e.columns.map(c=>`| ${c.id} | ${c.type} | ${c.nullable?'Yes':'No'} | ${c.description.replaceAll('|','\\|')} |`).join('\n')+'\n\nPrimary key: '+e.primary_key.join(', ')+'\n\n'+e.notes.join(' ')+'\n\n').join('');
}
