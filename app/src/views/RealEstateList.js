import m from "mithril";
import RealEstate from "../model/RealEstate";

export default {
  oninit: RealEstate.loadList,
  view: function () {
    return m(".real-estate-list", RealEstate.list.map((re) => {
      return m(".real-estate-item", re.url)
    }));
  }
}