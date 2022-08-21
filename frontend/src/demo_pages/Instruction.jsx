import React from "react";

const Instruction = () => {
  return (
  <>
    <div>
      <h1 className="Title">Systemübersicht</h1>
      <p className="Text">
        Diese Webseite demonstriert die erzielten Resultate der Bachelorarbeit.
        Der dazugehörige Bericht ist ebenfalls über das <a href="https://github.com/Ba-MH-RN/Human-in-the-loop-Image-Segmentation" target="_blank" rel="noreferrer">Git-Repository</a> verfügbar.
        Der Bericht dokumentiert die einzelnen Bestandteile des entstandeden Systems im Detail.
      </p>

      <p className="Text">
        <h4>Systemaufbau</h4>
        Das System ist darauf ausgelegt, sich einfach in eine bestehende Infrastruktur integrieren zu lassen.
        In folgender Abbildung sind die einzelnen Komponenten des Systems dargestellt und 
        an welchem Ort sich diese Befinden.
        <div><img className="Image" src="./media/Deployment.png" alt="Deploymentdiagramm von Frontend, Backend und Image-Segmentation."></img></div>
        Das Segmentation-Backend existiert abseits vom Website-Backend auf dem Server.
        In ihm ist das eigentliche Backend und die Image-Segmentation untergebracht.
        Das Backend stellt über eine REST-API ein Interface für das Frontend zur Verfügung.
        Ebenfalls kümmert sich das Backend um die Verwaltung der Trainingsdaten und der nachtrainierten Modelle.
        Zu diesem Zweck wird eine relationale Datenbank genutzt,
        wobei der Nutzer keinen Zugriff auf die Trainingsdaten hat.
        Das Frontend wird als React-Komponente in die Webseite eingebunden.
        Als Teil der Webseite liegt das Frontend daher auf dem Website-Backend und wird vom Browser angefordert und geladen.
        Beim Einbinden des Frontends wird ihm die URL des Segmentation-Backends mitgegeben.
        Durch diese URL kann auf die REST-API zugegriffen und somit das Backend genutzt werden.
        Die Daten zur Bearbeitung eines Segmentierungsauftrages liegen dabei lokal im Frontend. 
        Zu diesen Daten gehören das Bild und die Segmentierung.
        Diese werden, solange wie der Auftrag dauert, im Speicher des Browsers gehalten.
        Sobald der Auftrag beendet wird, werden auch die Daten verworfen.
        <br/>
        Die drei Hauptkomponenten Frontend, Backend und Image-Segmentation sind klar durch Schnittstellen abgegrenzt.
        Zwischen dem Frontend und Backend kommt dazu eine REST-API zum Einsatz, 
        während zwischen Backend und Image-Segmentation die Schnittstelle über ein Python-Interface implementiert wird.
        <div><img className="Image" src="./media/CommunicationDiagram.png" alt="Kommunikationsdiagramm von Frontend, Backend und Image-Segmentation."></img></div>
        Dabei dienen die Pfade mit 1.x.x der Initialisierung des Systems.
        Der eigentliche Segmentierungsvorgang ist mit den Pfaden 2.x.x abgebildet.
        Den Abschluss eines Segmentierungsauftrages ist über die Pfade 4.x.x dargestellt.
        Ist ein Auftrag abgeschlossen wird vom Backend überprüft, ob ein Nachtrainieren ausgelöst werden soll.
        Dieser Fall ist mit den Pfaden 5.x.x dargestellt.
        <br/>
        Das Frontend übernimmt die Rolle eines Segmentierungswerkzeuges.
        Es ermöglicht dies über interaktive Polygone, welche über das Bild gelegt werden.
        Diese Polygone können manipuliert und abschliessend heruntergeladen werden.
        <br/>
        Um einen Benutzer bei dieser Aufgabe zu unterstützen, wird das Bild an das Backend geschickt.
        Das Backend übernimmt dabei die Rolle der Verwaltung.
        Neben dem Weiterleiten des Bildes an die Image-Segmentation, wird das Bild gespeichert, um es später für Trainingszwecke
        zu benutzen.
        Für das Training werden auch die Verbesserungen, welche im Frontend stattfinden, benötigt.
        Diese Daten werden genutzt, um das neuronale Netzwerk nach zu trainieren und somit die Image-Segmentation zu verbessern.
        <br/>
        Die Image-Segmentation nutzt ein künstliches neuronales Netzwerk, um Segmentierungsvorschläge zu erarbeiten.
        Aus diesen wird in einem zweiten Schritt eine Liste von Polygonen erstellt.
        Diese werden an das Backend zurückgegeben, welches wiederum diese an das Frontend weiterleitet.
        Hier werden die Vorschläge dem Nutzer grafisch präsentiert.
      </p>

      <p className="Text">
        <h4>Verwendete Technologien</h4>
        Für das Backend kommt das Framework FastAPI zum Einsatz.
        Dieses ermöglicht eine REST-API mittels Python zu implementieren.
        Durch den Einsatz von Python im Backend können Bibliotheken und
        Frameworks für das Machine-Learning einfach eingebunden werden.
        <br/>
        Das Frontend ist als React-Komponente umgesetzt.
        Als solche kann es von React-Applikationen sowie über HTML-Webseiten eingebunden werden.
        Für die Darstellung und Bearbeitung der Segmentation wird Label-Studio-Frontend genutzt.
        Dies ist eine Bibliothek, um eine Datenannotierung in Webapplikationen zu realisieren.
      </p>
      
      <p className="Text">
        <h4>Abgrenzungen</h4>
        Dieses System ist als ein Konzept zu betrachten.
        Dementsprechend sind einige Gebiete, welche für eine Applikation in einer Produktionsumgebung essentiell wären, ausgegrenzt worden.
        Die Sicherheit ist ein Aspekt, welcher nicht behandelt wurde. 
        Mechanismen gegen Angriffe auf das System oder gegen einen Missbrauch wurden nicht integriert.
        Die Skalierbarkeit des Systems steht nicht im Fokus.
        Es richtet sich an Nutzer, welche einzelne Bilder segmentieren möchten.
        Es ist nicht darauf ausgelegt ganze Datensätze zu segmentieren.
        Die Implementierung eines vollumfänglichen Data- oder Model-Versioning-Systems für die Daten- oder Modellverwaltung
        wurde auf das Minimum reduziert.
      </p>
    </div>  
  </>
  );
}

export default Instruction;
