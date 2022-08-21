export default class LsfOptionFactory{

  /**
   * create a config object for Lsf with given labels
   */
  static createConfig(labels) {
    const configPrefix = `
      <View style="">
        <View style="display: flex; justify-content: center;">
          <PolygonLabels
          name="label" 
          toName="image"

          choice="single"
          maxUsages="9999"

          showInline="true"
          opacity="0.9"
          fillColor="#fcc844"

          strokeColor="#fc6c44"
          strokeWidth="3" 

          pointSize="small"
          pointStyle="rectangle"
          >
    `;
    const configSuffix = `
          </PolygonLabels>
        </View>

        <View style="box-shadow: 2px 2px 8px #AAA; display: flex; justify-content: center; background: #fafafa;">
          <Image
            width="100%"
            name="image" 
            value="$image"
            

            zoom="true"
            negativeZoom="true"
            zoomBy="1.0"
    
            grid="false"
            gridSize="30"
            gridColor="#EEEEF4"

            zoomControl="true"
            brightnessControl="false"
            contrastControl="false"
            rotateControl="false"

            crosshair="true"
          />
        </View>
      </View>
    `;

    // create Label section
    let configDynamic = "";
    labels.forEach(label => {
      configDynamic = configDynamic.concat(
        '<Label value="',
        label,
        `" />`
      );
    });

    // connect static and dynamic parts of config
    return configPrefix.concat(configDynamic, configSuffix);
  }

  
  /**
    * create a task object for Lsf with given imgPath
    * concat given annotation to new Task
   */
  static createTask(imgPath, oldLsfAnnots, newLsfAnnots) {
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
    }

    if (oldLsfAnnots !== undefined && oldLsfAnnots !== []) {
      task.annotations[0].result = task.annotations[0].result.concat(oldLsfAnnots);
    }

    if (newLsfAnnots !== undefined && newLsfAnnots !== []) {
      task.annotations[0].result = task.annotations[0].result.concat(newLsfAnnots);
    }
    return task;
  }
}