import m from 'mithril';

let result = 'Click to fetch data';

export function getResult() {
  return result;
}

export async function fetchAjax() {
  result = 'Fetching data ...';
  try {
    let data = await m.request({
      method: 'GET',
      url: MITHRIL_SERVER_URL + '/api/test',
    });
    result = JSON.stringify(data);
  } catch (e) {
    result = 'Error fetching data';
  }
}
