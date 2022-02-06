// a simple button that when clicked, refreshes the label with a new random number
import m from 'mithril';

export function RandomSlot({ attrs }) {
  let value = '' + (attrs.init || Math.floor(Math.random() * 10));

  function rollAgain() {
    value = '?';
    setTimeout(function() {
      value = '' + Math.floor(Math.random() * 10);
      m.redraw();
    }, 1500);
  }

  function view({ attrs }) {
    return m('button', {
        onclick: rollAgain,
        style: 'font-size: 20pt; padding-left: 15px; padding-right: 15px; color: ' + attrs.color,
      },
      value,
    );
  }

  return { view };
}
