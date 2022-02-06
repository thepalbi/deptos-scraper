// Babel has deprecated @babel/polyfill, and the following two imports are used for polyfills instead.
import 'core-js/stable';
import 'regenerator-runtime/runtime';
import m from 'mithril';
import RealEstateList from './views/RealEstateList';

m.mount(document.body, RealEstateList);
