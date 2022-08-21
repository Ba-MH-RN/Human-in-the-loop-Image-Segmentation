import React from "react";

import BtnUpload from "./BtnUpload";

import styles from "./styles.module.css";

export default function Control({ callbackFileUpload, callbackDownload, callbackClearWorkplace, callbackClearAllSelectedLabels }) {
  return (
  <>
    <div className={styles.div}>

      <BtnUpload 
        callback={callbackFileUpload}
      />

      <button
        className={styles.button}
        onClick={() => {callbackDownload()}}
      >
        Export<br/>Segmentations
      </button>

      <button
        className={styles.button}
        onClick={() => {callbackClearAllSelectedLabels()}}
      >
        Clear all Segmentations<br/>with selected Label
      </button>

      <button
        className={styles.button}
        onClick={() => {callbackClearWorkplace()}}
      >
        Clear<br/>Workplace
      </button>

    </div>
  </>
  );
}