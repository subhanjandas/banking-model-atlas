export type Theme = 'light' | 'dark';
export function initialTheme():Theme {
 try {const saved=localStorage.getItem('atlas-theme');if(saved==='light'||saved==='dark')return saved;}catch{/* Storage can be disabled. */}
 return typeof matchMedia==='function'&&matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light';
}
export function applyTheme(theme:Theme){
 document.documentElement.dataset.theme=theme;
 try{localStorage.setItem('atlas-theme',theme);}catch{/* The toggle still works in memory. */}
}
