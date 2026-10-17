'use client';
import {createElement as h} from 'react';
import {VitalPanel} from '@pezeshkon/vital';
/** Import @pezeshkon/vital/styles.css first, then Scroll-Logo-Frame.css. */
export function ScrollLogoFrame({children,theme='dark',metric,vitalProps={}}){
 return h('div',{className:`frame${theme==='day'?' day':''}`,dir:'rtl'},
 h('div',{className:'screen'},h('main',{className:'content'},children)),
 h('aside',{className:'frame-rail','aria-label':'اسکرول و لوگو'},h(VitalPanel,{...vitalProps,theme,metric})),
 h('div',{className:'bottom-tab','aria-hidden':true},'⌃'));
}
