export default class CocoHelper {
  
  static createBaseJson(token, info, categories, images) {
    if (token === null || token === undefined) {
      token = "none";
    }
    if (info === null || info === undefined) {
      info = {
        description: "NoModel",
        ModelVersion: -1,
      }; 
    }
    if (categories === null || categories === undefined || categories.length <= 0) {
      categories = [
        {
          id: 0,
          name: "NoLabel",
        }
      ];
    }
    if (images === null || images === undefined || images.length <= 0) {
      images = [
        {
          id: 0,
          file_name: "NoImage",
          width: 1,
          height: 1,
        }
      ];
    }

    let json = {
      token: token,
        cocoJSON: {
          info: info,
          categories: categories,
          images: images,
          annotations: [],
        }
    };

    return json;
  }


  static getMetaInfoFromBackendAnnots(backendAnnots) {
    const metaInfo = {
      token: backendAnnots.token,
      info: backendAnnots.cocoJSON.info,
      categories: backendAnnots.cocoJSON.categories,
      images: backendAnnots.cocoJSON.images,
    };
    return metaInfo;
  }


  static getMetaInfoFromLsfAnnotsAndLabels(lsfAnnots, labels) {
    let metaInfo = {
      token: "none",
      info: {
        description: "NoModel",
        ModelVersion: -1,
      },
      categories: [],
      images: [
        {
          id: 0,
          file_name: "NoName",
          height: lsfAnnots[0].original_height,
          width: lsfAnnots[0].original_width,
          
        }
      ],
    };

    labels.forEach(
      (item, idx) => {
        let label = {
          id: idx,
          name: item,
        };
        metaInfo.categories.push(label);
      }
    );
    return metaInfo;
  }


  static parseLsfAnnots2CocoAnnots(cocoJson, lsfAnnots, prefix) {
    let width = cocoJson.cocoJSON.images[0].width;
    let height = cocoJson.cocoJSON.images[0].height;
    let cocoAnnots = [];
    let lsfAnnotsCopy = [];

    if (lsfAnnots === null || lsfAnnots === undefined) {
      lsfAnnotsCopy = [];
    }
    else {
      lsfAnnotsCopy = JSON.parse(JSON.stringify(lsfAnnots));
    }

    // remove AI_-prefix of the labels
    lsfAnnotsCopy.forEach(
      (annot) => {
        annot.value.polygonlabels[0] = annot.value.polygonlabels[0].replace(prefix, "");
      }
    );

    lsfAnnotsCopy.forEach(
      (annot, idx) => {
        // create polygon with correct ID
        let polygon = {
          id: idx,
          image_id: cocoJson.cocoJSON.images[0].id,
          category_id: cocoJson.cocoJSON.categories.find(
            cat => cat.name === annot.value.polygonlabels[0]
          ).id,
          segmentation: [],
        };

        // create segmentation from lsf polygon (scale and transform polygon)
        let segmentation = [];
        annot.value.points.forEach(
          (p) => {
            let x = p[0] / 100 * width;
            let y = p[1] / 100 * height;
            segmentation.push(Math.round(x));
            segmentation.push(Math.round(y));
          }
        );

        // close Polygon
        if (segmentation[0] !== segmentation[segmentation.length - 2] || segmentation[1] !== segmentation[segmentation.length - 1]) {
          segmentation.push(segmentation[0]);
          segmentation.push(segmentation[1]);
        }
        polygon.segmentation = segmentation;
        cocoAnnots.push(polygon);
      }
    );
    
    return cocoAnnots;
  }
}