// import axios from 'axios';

class Morph {

  #RESOURCE_URL = "http://localhost:8000/dracogate/api/morphs/";

  #createMorph(game_no, name, ...kwargs) {
    const args = {
      game_no,
      name,
      ...kwargs,
    };
    const morphFetchTask = axios
      .get(RESOURCE_URL, {params: args})
      .then(resp => resp.data)
      .catch(err => console.log(err));
    return morphFetchTask;
  };

  async constructor(game_no, name, ...kwargs) {
    const args = {
      game_no,
      name,
      ...kwargs,
    };
    let [isSuccess, data] = await this.#createMorph(args);
    if (!isSuccess) {
      // Repopulate `args` with defaults.
      //console.log(data);
      this.missingParams = data.missingParams;
      args.kwargs = {};
      Object.entries(data.missingParams).forEach(entry => {
        const [key, values] = entry;
        const [defaultVal] = values;
        args.kwargs[key] = defaultVal;
      });
      args.kwargs = JSON.stringify(args.kwargs);
      //console.log(kwargs);
      let [_, defaultMorph] = await this.#createMorph(args);
      //console.log(defaultMorph);
      data = defaultMorph;
    };
    this.initParams = args;
    this.currentCls = data.currentCls;
    this.currentLv = data.currentLv;
    this.currentStats = data.currentStats;
    this.currentMaxes = data.currentMaxes;
  };

};

