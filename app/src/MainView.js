import m from 'mithril';
import * as model from './model';
import { RandomSlot} from './RandomSlot';

export function MainView({ attrs }) {
  let color = 'red';

  function colorChanged(ev) {
    color = ev.target.value;
  }

  function view({ attrs }) {
    return m('div', [
      m('h1', 'Hello World !!'),
      m('h3', [
        'Color: ',
        m('input', {
          type: 'text',
          value: color,
          onchange: colorChanged,
          style: 'font-size: 15pt;',
        }),
      ]),
      m('div', [m(RandomSlot, { init: 1, color: color }), m(RandomSlot, { init: 2, color: color }), m(RandomSlot, { color: color })]),
      m('h3',
        m('button', { onclick: model.fetchAjax, style: 'font-size: 15pt' }, model.getResult()),
      ),
      <div class="foo">Hi jsx</div>
    ]);
  }

  return { view };
}
