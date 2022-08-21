import React from "react";
import { useRef } from "react";

import styles from "./styles.module.css"

export default function BtnUpload({ callback }) {
  const inputRef = useRef(null);

  // functionalities to open file chooser
  const onClick = () => {
    inputRef.current.click();
  };
  const onChange = (event) => {
    if (event.target.files === null || event.target.files[0] === null) {
      return;
    }
    callback(event.target.files[0]);
  };

  return (
  <>
    <input
      style={{display: 'none'}}
      ref={inputRef}
      type='file'
      accept='.png, .jpg'
      onChange={onChange}
    />
    <button
      onClick={onClick}
      className={styles.button}
    >
      Upload<br/>Image
    </button>
  </>
  );
}