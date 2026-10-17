import React from 'react';
import {createRoot} from 'react-dom/client';
import App from './App';
import Engineering from './Engineering';
import './styles.css';
createRoot(document.getElementById('root')!).render(<React.StrictMode>{new URLSearchParams(location.search).get('page')==='engineering'?<Engineering/>:<App/>}</React.StrictMode>);
