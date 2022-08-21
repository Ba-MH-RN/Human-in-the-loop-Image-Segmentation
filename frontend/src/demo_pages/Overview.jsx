import React from "react";

const Overview = () => {
  return (
  <>
    <div>
      <h1 className="Title">Zusammenfassung</h1>
      <p className="Text">
        Die Image-Segmentation ist eines der Schlüsselprobleme auf dem Gebiet der Computer Vision. 
        Durch das Aufteilen eines Bildes in Segmente (Teilbereiche) kann der Weg zum vollständigen Verständnis des Bildinhalts geebnet werden. 
        Die Bedeutung dieses Problems wird durch die Tatsache unterstrichen, 
        dass eine wachsende Zahl von Anwendungen auf die Ableitung von Wissen aus Bildern angewiesen sind. 
        Einige dieser Anwendungen umfassen selbstfahrende Fahrzeuge, Augmented Reality oder Gesichtserkennung. 
        Der momentane Stand der Technik ist die Nutzung von künstlichen neuronalen Netzwerken für die Image-Segmentation.
        Für das Training dieser Netzwerke werden jedoch grosse Datenmengen benötigt,
        die nicht immer für jede Problemstellung zur Verfügung stehen.
        In solchen Fällen kann keine genügend hohe Genauigkeit mit dem Netzwerk erreicht werden und
        die Segmentation muss manuell erledigt werden.
        <br/>
        Bei dem Human-in-the-loop Ansatz wird die Verwendung von künstlichen neuronalen Netzwerken mit einer manuellen Nachbearbeitung verbunden.
        Dabei soll der Mensch die Segmentierung des neuronalen Netzwerks überprüfen und gegebenenfalls anpassen. 
        Durch die verbesserte Segmentierung generiert der BeBenutzer weitere Daten.
        Diese können benutzt werden, um das neuronale Netzwerk weiter zu trainieren.
        Eine Verbesserung des Netzwerks erzielt genauere Vorschläge, welche die Bearbeitung eines Segmentierungsauftrages beschleunigen.
        Somit lernt das System durch die Benutzung automatisch weiter und kann sich dynamisch der Anwendung anpassen.
        <div>
        <img className="Image" src="./media/Strukturdiagramm.png" alt="Katzenbild-Segmentierung mit dem Human-in-the-loop Ansatz"></img>
        </div>
        Das Resultat dieser Bachelorarbeit ist ein System zur AI-unterstützten Bildsegmentierung, 
        welches sich leicht in eine bestehende Infrastruktur integrieren lässt. 
        Dabei wurde das neuronale Netzwerk austauschbar gemacht. 
        Dadurch ist man nicht nur auf einen Anwendungsfall beschränkt.
        Diese Generalisierung erlaubt unterschiedliche Anwendungsfälle, wie zum Beispiel eine Segmentierung von Katzenbildern oder Gebäudeplänen.
        Das System besteht aus einem Frontend-, einem Backend- und einer Image-Segmentation-Komponente. 
      </p>

      <p className="Text">
        <h4>Frontend</h4>
        Das Frontend ist mit dem React-Framework als Webapplikation implementiert.
        Es lässt sich dadurch einfach in bestehende Webseiten integrieren und diese
        um eine interaktive AI-unterstützte Segmentierung von Bildern erweitern.
        Für die Kommunikation mit dem Backend wird eine REST-Schnittstelle verwendet.
        Das User-Interface ist schlicht gehalten, um einen unkomplizierten Arbeitsablauf sicherzustellen.
        Der Benutzer lädt zunächst das zu segmentierende Bild in die Webapplikation.
        Diese stellt im Hintergrund eine Segmentierungsanfrage an das Backend.
        Das Backend erarbeitet die Segmentierung und gibt als Resultat eine Liste von Polygonen in Form eines COCO-JSONs zurück.
        Diese werden im User-Interface über das Bild gelegt.
        An dieser Stelle kann der Benutzer den Segmentierungsvorschlag verwerfen, annehmen oder verbessern.
        Als letzter Schritt kann die Segmentation als COCO-JSON exportiert werden.
        Dieser Stand der Segmentierung wird gleichzeitig als Korrektur an das Backend geschickt.
      </p>
      <p className="Text">
        <h4>Backend</h4>
        Das Backend nimmt Segmentierungsanfragen über eine REST-Schnittstelle entgegen.
        Um die Schnittstelle für das Frontend zu implementieren wird das Framework FastAPI genutzt.
        Die Anfragen werden an die Image-Segmentation weitergeleitet und 
        die Segmentierung wird als Resultat anschliessend an das Frontend geschickt.
        Die vom Benutzer korrigierte Segmentierung wird abschliessend im Backend abgelegt und 
        später verwendet, um die Image-Segmentation zu verbessern.
        Bei einer Verbesserungsrunde werden verschiedene Metriken gespeichert.
        Diese werden über ein Dashboard dargestellt.
        Über dieses kann die Entwicklung des neuronalen Netzwerks innerhalb der Image-Segmentation beobachtet werden.
      </p>
      <p className="Text">
        <h4>Image-Segmentation</h4>
        Das Image-Segmentation-Modul befasst sich mit der eigentlichen Segmentierung der Bilder. Dabei ist es möglich
        das neuronale Netzwerk auszutauschen, um verschiedenste Anwendungsbereiche zu ermöglichen.  Die Schnittstelle zum
        Backend ist durch ein Python-Interface realisiert.
        Erhält die Image-Segmentation einen Auftrag vom Backend wird als erster Schritt ein Bild in den Arbeitsspeicher geladen und 
        auf die Inputgrösse des neuronalen Netzwerkes skaliert.
        Das skalierte Bild wird dem neuronalen Netzwerk übergeben und dieses erstellt für jeden Pixel eine Wahrscheinlichkeit, ob
        er der jeweiligen Kategorie zugehört.
        Durch das so entstehende Binärbild werden Polygone generiert und anschliessend auf die Orginalgrösse des Bildes skaliert.
        Schlussendlich wird mit den gefundenen Polygonen ein COCO-JSON-Dokument erstellt, welches an das Backend weitergegeben wird.
      </p>
    </div> 
  </>
  );
}

export default Overview;