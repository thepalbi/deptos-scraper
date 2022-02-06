import m from "mithril";

const apiHost = "http://localhost:8000"

var RealEstate = {
  list: [],
  loadList: async function () {
    const res = await m.request({
      method: "GET",
      url: `${apiHost}/real_estates/`
    });
    RealEstate.list = res.data;
    return;
  }
};

export default RealEstate;
