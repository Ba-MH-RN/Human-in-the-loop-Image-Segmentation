import React from 'react';
import { useEffect, useRef } from 'react'

import LabelStudio from "label-studio";
import "label-studio/build/static/css/main.css";

export default function LsfWrapper({
  triggerRefresh,
  config,
  task,
  callbackOnSubmitAnnotation,
  setLsfRef
}) {
  const ref = useRef(null);

  useEffect(() => {
    if (!ref.current) {
      return;
    } 
    var labelStudio = new LabelStudio(
      "label-studio", 
      {
        config: config,
        interfaces: [
          "side-column",
        ],
        task: task,

        onLabelStudioLoad: function (ls) {
          var c = ls.annotationStore.addAnnotation({
            userGenerate: true
          });
          ls.annotationStore.selectAnnotation(c.id);
        },
        onSubmitAnnotation: callbackOnSubmitAnnotation,
      }
    );
    ref.current = labelStudio;
    setLsfRef(ref.current);
    },
    // warning for 'missing dependencies' and 'react-hooks/exhaustive-deps' can be ignored
    [triggerRefresh]
  );

  // wrapper node to place LSF into
  return (
    <>
      <div id="label-studio" ref={ref}></div>
    </>
  );
}
