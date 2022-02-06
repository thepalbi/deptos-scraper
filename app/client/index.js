// Babel has deprecated @babel/polyfill, and the following two imports are used for polyfills instead.
import 'core-js/stable';
import 'regenerator-runtime/runtime';
import m from 'mithril';
import { MainView } from './MainView';

m.mount(document.body, MainView);
