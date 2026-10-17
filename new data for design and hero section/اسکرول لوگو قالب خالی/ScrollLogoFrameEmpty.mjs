'use client';
import {createElement as h} from 'react';
/** Copy assets to public/pezeshkon-vital-frame and import the companion CSS. */
export function ScrollLogoFrameEmpty({children=null,theme='dark',assetBase='/pezeshkon-vital-frame',className=''}){
 const mode=theme==='day'?'day':'dark';
 return h('div',{className:`pez-shell ${mode==='day'?'pez-shell-day ':''}${className}`,dir:'rtl'},
 h('div',{className:'pez-shell-screen'},h('main',{className:'pez-shell-content'},children)),
 h('aside',{className:'pez-shell-vital','aria-label':'اسکرول و لوگو'},h('img',{src:`${assetBase.replace(/\/$/,'')}/vital-${mode}.svg`,alt:'اسکرول و لوگوی پزشکآن'})),
 h('div',{className:'pez-shell-tab','aria-hidden':true},'⌃'));
}
