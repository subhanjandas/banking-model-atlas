import {useEffect,useRef,useImperativeHandle,forwardRef} from 'react';
import cytoscape,{type Core,type StylesheetJson} from 'cytoscape';
import {graphElements} from './graph';
import type {ViewState} from './model';
export type GraphHandle={fit:()=>void;zoom:(factor:number)=>void;png:()=>string|undefined};
const styles:StylesheetJson=[
 {selector:'node',style:{'background-color':'#ffffff','border-width':1.5,'border-color':'data(color)',label:'data(label)','font-family':'Inter, system-ui, sans-serif','font-size':12,'font-weight':500,color:'#213b43','text-wrap':'wrap','text-valign':'center','text-halign':'center','text-max-width':'210px','line-height':1.7,shape:'round-rectangle',width:222,height:86,'overlay-opacity':0}},
 {selector:'node[kind="domain"]',style:{width:246,height:128,'font-size':13,'font-weight':600,'border-width':2,'text-max-width':'220px','background-color':'#fffefb'}},
 {selector:':parent',style:{label:'data(label)','font-size':12,'font-weight':700,'text-valign':'top','text-halign':'left','text-margin-x':12,'text-margin-y':-8,'background-color':'data(color)','background-opacity':0.045,'border-width':1,'border-opacity':0.35,'border-style':'dashed',padding:'22px',shape:'round-rectangle'}},
 {selector:'edge',style:{width:1.2,'line-color':'#a5b7b7','target-arrow-color':'#a5b7b7','target-arrow-shape':'triangle','arrow-scale':0.7,'curve-style':'bezier',opacity:0.5,'loop-direction':'-35deg','loop-sweep':'65deg','control-point-step-size':40,'overlay-opacity':0}},
 {selector:'edge[kind="domain_edge"]',style:{'target-arrow-shape':'none',width:1.5,opacity:0.4}},
 {selector:'.selected',style:{'border-color':'#153e42','border-width':3,'background-color':'#e8f1eb','z-index':20}},
 {selector:'edge.selected',style:{'line-color':'#17685a','target-arrow-color':'#17685a',width:3,opacity:1,label:'data(label)','font-size':11,'text-background-color':'#fff','text-background-opacity':1,'text-background-padding':'4px','text-rotation':'autorotate'}},
 {selector:'.near',style:{opacity:1,'line-color':'#528c82','target-arrow-color':'#528c82',width:2}},
 {selector:'.dim',style:{opacity:0.17}}
];
export const Graph=forwardRef<GraphHandle,{state:ViewState;onEntity:(id:string)=>void;onDomain:(id:string)=>void;onEdge:(id:string)=>void;onZoom:(z:number)=>void}>(function Graph({state,onEntity,onDomain,onEdge,onZoom},ref){
 const container=useRef<HTMLDivElement>(null),cy=useRef<Core|null>(null);
 const callbacks=useRef({onEntity,onDomain,onEdge,onZoom});callbacks.current={onEntity,onDomain,onEdge,onZoom};
 useImperativeHandle(ref,()=>({fit:()=>{cy.current?.fit(undefined,44);},zoom:f=>{const c=cy.current;if(c)c.zoom({level:c.zoom()*f,renderedPosition:{x:c.width()/2,y:c.height()/2}});},png:()=>cy.current?.png({bg:'#f6f7f2',full:true,scale:2,maxWidth:4000,maxHeight:4000})}),[]);
 useEffect(()=>{
  const c=cytoscape({container:container.current!,elements:[],style:styles,minZoom:0.12,maxZoom:3,wheelSensitivity:0.18,boxSelectionEnabled:false,selectionType:'single',autounselectify:true});cy.current=c;
  c.on('tap','node',e=>{const n=e.target;if(n.data('kind')==='domain')callbacks.current.onDomain(n.id());else if(n.data('kind')==='entity')callbacks.current.onEntity(n.id());});
  c.on('tap','edge',e=>{if(e.target.data('kind')==='relationship')callbacks.current.onEdge(e.target.id());});
  c.on('zoom',()=>callbacks.current.onZoom(c.zoom()));
  const resize=new ResizeObserver(()=>{c.resize();});resize.observe(container.current!);
  return()=>{resize.disconnect();c.destroy();cy.current=null;};
 },[]);
 useEffect(()=>{const c=cy.current;if(!c)return;c.elements().remove();c.add(graphElements(state));c.layout({name:'preset',fit:true,padding:44}).run();},[state.view,state.domain,state.journey,state.focus]);
 useEffect(()=>{const c=cy.current;if(!c)return;c.elements().removeClass('selected near dim');const id=state.entity||state.edge;if(!id)return;const selected=c.getElementById(id);if(selected.empty())return;selected.addClass('selected');if(state.entity){const n=selected.closedNeighborhood();c.edges().not(n).addClass('dim');selected.connectedEdges().addClass('near');if(c.zoom()<0.65)c.zoom(0.9);c.center(selected);}else{selected.connectedNodes().addClass('selected');c.edges().not(selected).addClass('dim');}},[state.entity,state.edge,state.view,state.domain,state.journey,state.focus]);
 return <div ref={container} className="graph-canvas" data-testid="graph-canvas" role="img" aria-label={state.view==='domains'?'Interactive banking domain map. Use the domain list for keyboard navigation.':'Interactive entity relationship graph. Use the entity and relationship lists for keyboard navigation.'}/>;
});
