import React, { useEffect } from "react";

import styles from "./styles.module.css";

export const InfoConstants = {
  SERVER_OFFLINE: 0,
  SERVER_ONLINE: 1,
  PREDICTION_PENDING: 2,
  PREDICTION_READY: 3,
  WAITING_IMAGE: 4,
};

export default function Info({ state }) {
  let text = ""; // init with dummy value
  let style = styles.SERVER_OFFLINE; // init with dummy value

  switch (state) {
    case InfoConstants.SERVER_OFFLINE:
      text = "Offline-Mode: The server can not be reached or an error occured";
      style = styles.offline;
      break;
    case InfoConstants.SERVER_ONLINE:
      text = "Server is ready";
      style = styles.online;
      break;
    case InfoConstants.PREDICTION_PENDING:
      text = "Server is working on the segmentation proposal";
      style = styles.pending;
      break;
    case InfoConstants.PREDICTION_READY:
      text = "Segmentation proposal has been added";
      style = styles.ready;
      break;
    case InfoConstants.WAITING_IMAGE:
      text = "Segmentations have been exported, waiting for new image";
      style = styles.waiting;
      break;
    default:
      text = "Error: State could not match InfoConstants";
      style = styles.offline;
      break;
  }

  // State observer
  useEffect(() => {}, [state]);

  return (
  <>
    <div className={style}>
      <h5>Backend Status:</h5>
      <p style={{"marginBottom":0}}>{text}</p>
    </div>
  </>
  );
}