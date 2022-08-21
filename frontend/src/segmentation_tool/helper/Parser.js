import CocoHelper from "./CocoHelper";
import LsfTaskHelper from "./LsfTaksHelper";

export default class Parser {
  static prefix = "AI_";

  
  static createCocoJson(backendAnnots, lsfAnnots, imgName, labels) {
    let token = null;
    let info = null;
    let categories = null;
    let images = null;

    if (backendAnnots !== null && backendAnnots !== undefined) {
      const metaInfo = CocoHelper.getMetaInfoFromBackendAnnots(backendAnnots);
      token = metaInfo.token;
      info = metaInfo.info;
      categories = metaInfo.categories;
      images = metaInfo.images;
      images[0].file_name = imgName;
    }
    else if ((lsfAnnots !== undefined && lsfAnnots !== null) && lsfAnnots.length > 0) {
      const metaInfo = CocoHelper.getMetaInfoFromLsfAnnotsAndLabels(lsfAnnots, labels);
      token = metaInfo.token;
      info = metaInfo.info;
      categories = metaInfo.categories;
      images = metaInfo.images;
      images[0].file_name = imgName;
    }

    let json = CocoHelper.createBaseJson(token, info, categories, images);

    let cocoAnnots = CocoHelper.parseLsfAnnots2CocoAnnots(json, lsfAnnots, this.prefix);
    json.cocoJSON.annotations = cocoAnnots;

    return json;
  }


  static integrateCocoJsonIntoLsfTask(backendAnnots, lsfAnnots, imgPath) {
    let task = {
      data: {
        image: imgPath,
      },
      predictions: [],
      annotations: [
        {
          result: [],
        }   
      ],
    };

    if (lsfAnnots === undefined || lsfAnnots === null) {
      lsfAnnots = [];
    }
    let lsfAnnotsFromCoco = LsfTaskHelper.parseCocoAnnots2LsfAnnots(backendAnnots, this.prefix);
    task.annotations[0].result = lsfAnnots.concat(lsfAnnotsFromCoco);

    return task;
  }


  static extractLabelsFromBackendAnnot(backendAnnots) {
    let labels = [];

    backendAnnots.cocoJSON.categories.forEach(
      (cat) => {
        labels.push(cat.name);
        labels.push(this.prefix.concat(cat.name));
      }
    );
    return labels;
  }
}