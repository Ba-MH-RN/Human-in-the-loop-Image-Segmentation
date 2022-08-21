// extern libs
import React from "react";
import { useState, useEffect } from "react";
import axios from "axios";
import { useDropzone } from "react-dropzone";

// jsx-elements
import Control from "./control/Control";
import LsfWrapper from "./lsf/LsfWrapper";
import Info from "./info/Info";

// intern libs
import { InfoConstants } from "./info/Info";
import Parser from "./helper/Parser"
import LsfTaskHelper from "./helper/LsfTaksHelper";
import LsfOptionFactory from "./helper/LsfOptionFactory";

// style and media
import styles from "./styles.module.css";
import img_placeholder from "./media/placeholder2.jpg";



const States = {
  INIT: 0,                // Start State --> sends Heartbeat to Server
  OFFLINE: 1,             // if Heartbeat does't reach Server
  ONLINE: 2,              // get Labels from Server
  READY: 3,               // waits for new Image
  PREDICTION_PENDING: 4,  // Image was sended to Server
  PREDICTION_READY: 5,    // Server Annotation arrived at Frontend
  PREDICTION_ADDING: 6,   // Server Annotation are integrating in Frontend/Task
  PREDICTION_ADDED: 7,    // Server Annotation has inserted in Task, waiting for User Adjustment or Action
  DOWNLOAD: 8,            // User triggered 'Export'
  WAITING_IMAGE: 9,       // similar to Ready
  CLEAR_SELECTED_ANNOTS: 10 // User triggered 'Clear selected Labels'
}


export default function SegmentationTool({ backendUrl, fallbackLabels, callbackExport, downloadEnabled, imagePlaceholderUrl }) {
  const [img, setImg] = useState(
    {
      file: null,
      path: ((imagePlaceholderUrl === null || imagePlaceholderUrl === undefined) ? img_placeholder : imagePlaceholderUrl),
      name: "placeholder",
    }
  );
  const [isServerOnline, setIsServerOnline] = useState(false);
  const [state, setState] = useState(States.INIT);
  const [infoState, setInfoState] = useState(InfoConstants.SERVER_OFFLINE);
  const [labels, setLabels] = useState(fallbackLabels);
  const [backendAnnotation, setBackendAnnotation] = useState(null);
  const [lsfAnnotations, setLsfAnnotations] = useState(null);
  const [lsfRef, setLsfRef] = useState();
  const [shouldLsfRefresh, setShouldLsfRefresh] = useState(true);
  const [lsfConfig, setLsfConfig] = useState(LsfOptionFactory.createConfig(labels));
  const [lsfTask, setLsfTask] = useState(LsfOptionFactory.createTask(img.path, [], []));
  const [selectedLabel, setSelectedLabel] = useState("");
  const [previousState, setPreviousState] = useState(States.INIT);

  /**
   * This function is to Trigger a Rerender of the Lsf
   * The Lsf is new created with the current lsfConfig and lsfTask
   */
  function refreshLsf() {
    setShouldLsfRefresh(!shouldLsfRefresh);
  }

  /**
   * Sends Image to Server
   * Server responds is saved and state changed to PREDICTION_READY
   */
  function uploadImg2Server(imageFile) {
    let formData = new FormData();
    formData.append('file', imageFile);

    axios(
      {
        baseURL: backendUrl,
        url: '/ImageSegmentation/uploadImage',
        method: 'POST',
        data: formData,
        responseType: 'json'
      }
    ).then(
      (result) => {
        reactionServerError(result);

        setBackendAnnotation(result.data);
        setState(States.PREDICTION_READY);
      }
    ).catch((error) => {reactionConnectionError(error)}).then(() => {});
  }

  /**
   * Sends a Cosing/Ending message to the server
   * inform the server, the image with corresponding token will not receive a correction upload
   */
  function sendDeathBeat() {
    if (backendAnnotation !== null && isServerOnline) {
      console.debug(backendAnnotation.token);
      axios(
        {
          baseURL: backendUrl,
          url: '/ImageSegmentation/uploadNoCorrection',
          method: 'post',
          data: {
            token: backendAnnotation.token
          },
        }
      ).then().catch().then();
    }
  }

  /**
   * Function to handle Server and Connection errors
   * log the error and change state to offline
   */ 
  const reactionServerError = (result) => {
    if (result.status  !== 200) {
      logError("Server-Response", result.config.url, result.status, result.statusText);
      setState(States.OFFLINE);
      setIsServerOnline(false);
      return;
    }
  }
  const reactionConnectionError = (error) => {
    logError("Error", error.config.url, error.code, error.message, error);
    setState(States.OFFLINE);
    setIsServerOnline(false);
  }
  function logError(type, url, code, message, errorObject) {
    console.log("".concat(type, ": ", url));
    console.log("".concat(code, ": ", message));
    console.log(errorObject);
  }


  // ---- Callbacks ----
  /**
   * Handle a Fileinput
   * Does nothing when a prediction is pending
   * sends a deathbeat when state is READY or WAITING_IMAGE
   */
  const callbackFileUpload = (file) => {
    // Server works on prediction -> no new file accepting
    if (state === States.PREDICTION_PENDING) {
      alert("Waiting for Server-Response, please wait... \n If the page seems stuck, please reload the page.");
      return;
    }
    else if (state !== States.READY || state !== States.WAITING_IMAGE) {
      if (backendAnnotation !== null) {
        sendDeathBeat();
        setState(States.INIT);
      }
    }
    if (img.path !== null) {
      URL.revokeObjectURL(img.file);
    }
    setImg(
      {
        file: file,
        path: URL.createObjectURL(file),
        name: file.name,
      }
    );
  }

  /**
   *  Handle 'clear workplace' input --> resets tool
   */
  const callbackClearWorkplace = () => {
    if (state === States.PREDICTION_PENDING) {
      alert("Waiting for Server-Response, please wait... \n If the page seems stuck, please reload the page.");
      return;
    }
    sendDeathBeat();
    setImg(
      {
        file: null,
        path: img_placeholder,
        name: "placeholder",
      }
    );
    setIsServerOnline(false);
    setState(States.INIT);
    setInfoState(InfoConstants.SERVER_OFFLINE);
    setLabels(fallbackLabels);
    setBackendAnnotation(null);
    setLsfAnnotations(null);
    setLsfRef(null);
    setLsfConfig(LsfOptionFactory.createConfig(labels));
    setLsfTask(LsfOptionFactory.createTask(img_placeholder), [], []);
  }

  /**
   * Handles 'Clear Labels' Input
   */
  const callbackClearAllSelectedLabels = () => {
    if (state !== States.PREDICTION_ADDED && state !== States.WAITING_IMAGE && state !== States.OFFLINE) {
      return;
    }
    const lsfLabels = lsfRef.annotationStore.selected.results;
    if (lsfLabels === undefined || lsfLabels === null) {
      return;
    }
    setPreviousState(state);
    lsfLabels.forEach(
      (e) => {
        if (e.selectedLabels[0].selected) {
          setSelectedLabel(e.selectedLabels[0]._value);
        }
      }
    );
    lsfRef.submitAnnotation(); 
    setState(States.CLEAR_SELECTED_ANNOTS);
  }


  // ---- Helpers ----
  /**
   * Extract Annotations from Lsf
   * Callback set Annotations --> they are ready on next cycle
   * lsfRef.submitAnnotation() triggers the onSubmitAnnotation event of Lsf
   * User -> callbackDownload() -> lsfRef.submitAnnotation() -> onSubmitAnnotation() -> callbackOnSubmitAnnotation() --> setLsfAnnotations()
   * Roundtrip necessary to access lsfAnnotations, no direct way/method has been found to extract the Annotation from LSF
   */
  function callbackOnSubmitAnnotation(ls, annotation) {
    setLsfAnnotations(annotation.serializeAnnotation());
 }
  const callbackDownload = () => {
    if (img.file === null) {
      alert("Please Upload an Image first...");
      return;
    }
    lsfRef.submitAnnotation(); 
    setState(States.DOWNLOAD);
  }
  
   /**
    * Dropzone functionalities
    * does not react to clicks
    */
  const onDrop = (files) => {
    if (files === null || files === undefined || files[0] === null || files[0] === undefined) {
      return;
    }
    callbackFileUpload(files[0]);
  }
  const {getRootProps} = useDropzone({
    onDrop: onDrop,
    noClick: true,
    multiple: false,
    accept: {'image/*': ['.png', '.jpg']}
  });


  //---- componentDidUpdate Life-cycle -----
  /**
   * reacts to changes of state
   * FSM for Flow control
   */
  useEffect(
    () => {
      switch(state) {

        // initial state: check if Server is online with timeout
        case States.INIT: {
          axios(
            {
              baseURL: backendUrl,
              url: '/heartbeat',
              method: 'get',
              timeout: 1000, // waiting time in ms => 1 second
            }
          ).then(
            (result) => {
              reactionServerError(result);
              setState(States.ONLINE);
              setIsServerOnline(true);
            }
          ).catch((error) => {reactionConnectionError(error);console.log(error)}).then(() => {});

          setInfoState(InfoConstants.SERVER_OFFLINE);
          setIsServerOnline(false);
          break;
        }

        // Server is Offline
        case States.OFFLINE: {
          setInfoState(InfoConstants.SERVER_OFFLINE);
          break;
        }

        // Server is Online
        // get Labels from Server --> overrides the fallbacks
        case States.ONLINE: {
          axios(
            {
              baseURL: backendUrl,
              url: '/ImageSegmentation/getCategories',
              method: 'get',
              responseType: 'json'
            }
          ).then(
            (result) => {
              reactionServerError(result);

              let labels = [];
              result.data.categories.forEach(element => {
                labels.push(element.name);
              });
              setLabels(labels);
              setState(States.READY)
            }
          ).catch((error) => {reactionConnectionError(error)}).then(() => {});
          
          setInfoState(InfoConstants.SERVER_OFFLINE); // Info Panel is still offline
          break;
        }

        // Tool is Ready
        // server online and labels present
        // when Image is uploaded change to next state
        // if already a image is uploaded --> fall trough to the next State
        case States.READY: {
          if (img.path !== img_placeholder) {
            setState(States.PREDICTION_PENDING);
          }
          setInfoState(InfoConstants.SERVER_ONLINE);
          break;
        }

        // Server is working on Predictions
        // When Prediction is received, change to next state
        case States.PREDICTION_PENDING: {
          setInfoState(InfoConstants.PREDICTION_PENDING);
          break;
        }

        // Predictions are ready
        // integrate prediction in current lsf task
        // Trigger lsf -> get Annotations from User
        // to be able to access lsfAnnotations, wait one cycle --> wait for next state
        case States.PREDICTION_READY: {
          lsfRef.submitAnnotation();

          setState(States.PREDICTION_ADDING);
          setInfoState(InfoConstants.PREDICTION_PENDING);
          break;
        }

        // create new task from old annotations and predicted
        
        case States.PREDICTION_ADDING: {
          let task = Parser.integrateCocoJsonIntoLsfTask(backendAnnotation, lsfAnnotations, img.path);
          let labels = Parser.extractLabelsFromBackendAnnot(backendAnnotation);
          setLsfTask(task);
          setLsfConfig(LsfOptionFactory.createConfig(labels));

          setState(States.PREDICTION_ADDED)
          setInfoState(InfoConstants.PREDICTION_PENDING);
          break;
        }

        // Waiting State for user to adjust predictions
        // change to download when user clicks on button 'export'
        // change to init when new image is uploaded
        case States.PREDICTION_ADDED: {
          setInfoState(InfoConstants.PREDICTION_READY);
          break;
        }

        // Json to Download
        // sends Json as correction to Backend, if backend is online/reachable
        case States.DOWNLOAD: {
          let cocoJson = Parser.createCocoJson(backendAnnotation, lsfAnnotations, img.name, labels);

          if (isServerOnline) {
            axios(
              {
                baseURL: backendUrl,
                url: '/ImageSegmentation/uploadCorrection',
                method: 'post',
                data: cocoJson,
              }
            ).then(
              (result) => {
                reactionServerError(result);
                console.debug("Correction send to Backend");
              }
            ).catch((error) => {reactionConnectionError(error)}).then(() => {});
          }

          // create Download
          if (downloadEnabled) {
            let data = new Blob([JSON.stringify(cocoJson.cocoJSON)], {type: 'text/json'});
            let jsonUrl = URL.createObjectURL(data);
            let tempLink = document.createElement('a');
            tempLink.href = jsonUrl;
            tempLink.setAttribute('download', "".concat(img.name.split('.').slice(0, -1).join('.'), ".json"));
            tempLink.click();
            URL.revokeObjectURL(data);
          }
          // forward Json to outer Callback
          if (callbackExport !== null && callbackExport !== undefined) {
            callbackExport(cocoJson.cocoJSON);
          }
          
          setState(States.WAITING_IMAGE);
          // no change to infoState
          break;
        }

        // waiting for new image after downloading Annotations
        // upload a new image set state to INIT
        case States.WAITING_IMAGE: {
          setInfoState(InfoConstants.WAITING_IMAGE);
          break;
        }

        case States.CLEAR_SELECTED_ANNOTS: {
          const newAnnots = LsfTaskHelper.removeFromLsfAnnotsLabel(lsfAnnotations, selectedLabel);
          let task = LsfOptionFactory.createTask(img.path, newAnnots, []);
          setLsfTask(task);
          setState(previousState);
          break;
        }

        default: {
          setState(States.INIT)
        }
      }

      // Debug Info
      console.debug("state: ".concat(state));
    },
    // warning for 'missing dependencies' and 'react-hooks/exhaustive-deps' can be ignored
    [state]);


  /**
   * reacts to changes to img and labels
   * create new task and config for lsf accordingly
   * new img are also uploaded to the backend
   */
  useEffect(
    () => {
      let config = null;
      let task = null;
      
      if (state === States.READY && img.path !== img_placeholder) {
        uploadImg2Server(img.file);
      }
      else if (state === States.WAITING_IMAGE){
        setState(States.INIT);
      }

      // update LSF
      if (config === null) {
        config = LsfOptionFactory.createConfig(labels);
      }
      if (task === null) {
        task = LsfOptionFactory.createTask(img.path, [], []);
      }
      setLsfConfig(config);
      setLsfTask(task);
    },
    // warning for 'missing dependencies' and 'react-hooks/exhaustive-deps' can be ignored
    [
      img, 
      labels,
    ]
  );

  /**
   * triggers lsf update when task or config change
   */
  useEffect(
    () => {
      refreshLsf();
    },
    // warning for 'missing dependencies' and 'react-hooks/exhaustive-deps' can be ignored
    [
      lsfConfig,
      lsfTask,
    ]
  );

  /**
   * Reset of the tool if outside props changes
   */
  useEffect(
    () => {
      callbackClearWorkplace();
    },
    // warning for 'missing dependencies' and 'react-hooks/exhaustive-deps' can be ignored
    [backendUrl, fallbackLabels, callbackExport, downloadEnabled]
  );
  
  

  //---- Rendering -----
  return (
  <>
    <section className="container">
      <div {...getRootProps({className: 'dropzone'})}>
        <div className={styles.divOuter}>
          <div className={styles.divControl}>
            <Control 
              callbackFileUpload={callbackFileUpload}
              callbackDownload={callbackDownload}
              callbackClearWorkplace={callbackClearWorkplace}
              callbackClearAllSelectedLabels={callbackClearAllSelectedLabels}
            />
          </div>
          <div>
            <Info 
              // state={InfoConstants.WAITING_IMAGE}
              state={infoState}
            />
          </div>
          <br />
          <div className={styles.divWrapper}>
            <LsfWrapper
              triggerRefresh={shouldLsfRefresh}
              config={lsfConfig}
              task={lsfTask}
              callbackOnSubmitAnnotation={callbackOnSubmitAnnotation}
              setLsfRef={setLsfRef}
            />
          </div>
        </div>
      </div>
    </section>
  </>
  );
}