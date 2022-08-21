export default class LsfTaskHelper {
  
  static parseCocoAnnots2LsfAnnots(cocoJson, prefix) {
    let width = cocoJson.cocoJSON.images[0].width;
    let height = cocoJson.cocoJSON.images[0].height;
    let cocoAnnots = cocoJson.cocoJSON.annotations;

    if (cocoAnnots === null || cocoAnnots === undefined) {
      cocoAnnots = [];
    }

    let lsfAnnots = [];
    cocoAnnots.forEach((annot) => {
      // create a base lsf-annot
      let lsfAnnot = {
        original_width: width,
        original_height: height,
        image_rotation: 0,
        from_name: "label",
        to_name: "image",
        type: "polygonlabels",
        value: {
          points: [],
          polygonlabels: "undefined",
        }
      };

      // add prefix to matching label/category
      lsfAnnot.value.polygonlabels = [ prefix.concat(
        cocoJson.cocoJSON.categories.find(
          cat => cat.id === annot.category_id
        ).name
      ) ];

      // scale and transform polygon
      for (let i = 0; i < annot.segmentation.length; i = i+2) {
        let x = annot.segmentation[i] / width * 100;
        let y = annot.segmentation[i+1] / height * 100;
        let p = [x, y];
        lsfAnnot.value.points.push(p);
      }
      lsfAnnots.push(lsfAnnot);
    });

    return lsfAnnots;
  }

  static removeFromLsfAnnotsLabel(lsfAnnots, label) {
    if (lsfAnnots === undefined || lsfAnnots === null) {
      return [];
    }
    if (label === undefined || label === null) {
      return lsfAnnots;
    }
    let newLsfAnnots = [];
    lsfAnnots.forEach(
      (e) => {
        if (label !== e.value.polygonlabels[0]) {
          newLsfAnnots.push(e);
        }
      }
    );
    return newLsfAnnots; 
  }
}