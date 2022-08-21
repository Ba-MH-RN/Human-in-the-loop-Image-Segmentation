import React from "react";
import { Navbar, Container, Nav } from "react-bootstrap";

const NavigationBar = () => {
  return(
  <>
    <Navbar bg="light" variant="light" sticky="top" expand="lg">
        <Container>
          <Navbar.Brand>
            <img 
              src="logo-de.svg"
              width="75"
              className="d-inline-block align-top"
              alt="Website Logo OST"
            />{'              '}
            Human-in-the-loop Image-Segmentation
          </Navbar.Brand>
          <Nav className="me-auto">
            <Nav.Link href="/">Zusammenfassung</Nav.Link>
            <Nav.Link href="/segmentation">Segmentierungs-Tool</Nav.Link>
            <Nav.Link href="/instruction">Systemübersicht</Nav.Link>
          </Nav>
        </Container>
      </Navbar>
  </>
  );
}

export default NavigationBar