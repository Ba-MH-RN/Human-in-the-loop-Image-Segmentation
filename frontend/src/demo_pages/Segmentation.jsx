import React from "react";

import SegmentationTool from "../segmentation_tool/SegmentationTool";

const Segmentation = () => {
  return (
  <>
    <div>
      <h1 className="Title">Segmentierungs-Tool</h1>
      <p className="Text">
        Zum Starten eines Segmentierungsauftrages bitte ein Bild über die Schaltfläche "Upload Image" auswählen.
        Alternativ kann auch ein Bild direkt in die Arbeitsfläche des Segmentierungs-Tools gezogen werden.
        Über die Schaltfläche "Export Segmentations" können die Segmentierungen als COCO-JSON heruntergeladen werden.
      </p>
      <div>
        <SegmentationTool 
          backendUrl={"http://127.0.0.1:8000/"}
          fallbackLabels={["label_1", "label_2"]}
          downloadEnabled={true}
          callbackExport={null}
          imagePlaceholderUrl={null}
        />
      </div>
    </div> 
  </>
  );
}

export default Segmentation;