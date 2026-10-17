import type {ElementDefinition} from 'cytoscape';
import {model,entityById,domainById,visibleModel,type ViewState} from './model';
export function graphElements(state:ViewState):ElementDefinition[]{
 if(state.view==='domains'){
  const nodes=model.domains.map((d,i)=>({data:{id:d.id,kind:'domain',color:d.color,label:d.label.toUpperCase()+'\n\n'+model.entities.filter(e=>e.domain===d.id).length+' entities',description:d.description},position:{x:(i%3)*300,y:Math.floor(i/3)*190}}));
  const pairs=new Map<string,{a:string;b:string;count:number}>();
  model.relationships.forEach(r=>{const a=entityById.get(r.source_entity)!.domain,b=entityById.get(r.target_entity)!.domain;if(a!==b){const [x,y]=[a,b].sort(),key=x+'__'+y;const p=pairs.get(key);if(p)p.count++;else pairs.set(key,{a:x,b:y,count:1});}});
  return [...nodes,...[...pairs].map(([id,p])=>({data:{id:'domain_edge_'+id,source:p.a,target:p.b,kind:'domain_edge',label:p.count+' links'}}))];
 }
 const {entities,relationships}=visibleModel(state);
 if(state.journey||state.focus){
  const journey=model.journeys.find(j=>j.id===state.journey);
  const ordered=journey?journey.steps.map(s=>entityById.get(s.entity)!):[...entities].sort((a,b)=>a.id===state.focus?-1:b.id===state.focus?1:0);
  return [...ordered.map((e,i)=>{const row=Math.floor(i/3);return {data:{id:e.id,kind:'entity',color:domainById.get(e.domain)!.color,label:e.id+'\n\nPK  '+e.primary_key[0]+'\n'+e.columns.length+' columns · '+e.rule_ids.length+' rules'},position:{x:(row%2?2-i%3:i%3)*275,y:row*150}};}),...relationships.map(r=>({data:{id:r.id,source:r.source_entity,target:r.target_entity,kind:'relationship',label:r.source_column}}))];
 }
 const domains=model.domains.filter(d=>entities.some(e=>e.domain===d.id));
 const nodes:ElementDefinition[]=[];
 // Each domain occupies its own fixed-width tile. Four rows accommodate the accounting domain.
 domains.forEach((d,di)=>{
  const members=entities.filter(e=>e.domain===d.id),cx=(di%3)*570,cy=Math.floor(di/3)*545;
  nodes.push({data:{id:'group_'+d.id,label:d.label.toUpperCase(),kind:'group',color:d.color}});
  members.forEach((e,i)=>nodes.push({data:{id:e.id,parent:'group_'+d.id,kind:'entity',color:d.color,label:e.id+'\n\nPK  '+e.primary_key[0]+'\n'+e.columns.length+' columns · '+e.rule_ids.length+' rules'},position:{x:cx+(i%2)*252,y:cy+Math.floor(i/2)*115}}));
 });
 return [...nodes,...relationships.map(r=>({data:{id:r.id,source:r.source_entity,target:r.target_entity,kind:'relationship',label:r.source_column,color:domainById.get(entityById.get(r.source_entity)!.domain)!.color}}))];
}
