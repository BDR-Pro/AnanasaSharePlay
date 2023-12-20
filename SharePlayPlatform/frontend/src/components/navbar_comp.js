import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Form from 'react-bootstrap/Form';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';
import Offcanvas from 'react-bootstrap/Offcanvas';
import { render } from 'react-dom';
import React from 'react';
import { useState } from 'react';

function NavbarComponent() {
    const [searchQuery, setSearchQuery] = useState('');

    const handleSearch = (event) => {
      event.preventDefault();
      // Redirect to the search page with the search query
      window.location.href = `/search?query=${encodeURIComponent(searchQuery)}`;
    };
  
  return (
    <>
      {['xxl'].map((expand) => (
        <Navbar key={expand} expand={expand} className="bg-body-tertiary mb-3">
          <Container fluid>
            <Navbar.Brand href="/">Ananasa</Navbar.Brand>
            <Navbar.Toggle aria-controls={`offcanvasNavbar-expand-${expand}`} />
            <Navbar.Offcanvas
              id={`offcanvasNavbar-expand-${expand}`}
              aria-labelledby={`offcanvasNavbarLabel-expand-${expand}`}
              placement="end"
            >
              <Offcanvas.Header closeButton>
                <Offcanvas.Title id={`offcanvasNavbarLabel-expand-${expand}`}>
                  Offcanvas
                </Offcanvas.Title>
              </Offcanvas.Header>
              <Offcanvas.Body>
                <Nav className="justify-content-end flex-grow-1 pe-3">
                  <Nav.Link href="/login">login</Nav.Link>
                  <Nav.Link href="/register">sign Up</Nav.Link>
                  <Nav.Link href="/Profile">Profile</Nav.Link>
                  <NavDropdown
                    title="Library"
                    id={`offcanvasNavbarDropdown-expand-${expand}`}
                  >
                    <NavDropdown.Item href="/MyGames">My Games</NavDropdown.Item>
                    <NavDropdown.Item href="/Profile/rents">
                      My Rents
                    </NavDropdown.Item>
                    <NavDropdown.Divider />
                    <NavDropdown.Item href="/Statistic">
                    Statistic
                </NavDropdown.Item>
                  </NavDropdown>
                </Nav>
                <Form className="d-flex" onSubmit={handleSearch}>
                  <Form.Control
                    type="search"
                    placeholder="Search"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="me-2"
                    aria-label="Search"
                  />
                  <Button variant="outline-success">Search</Button>
                </Form>
              </Offcanvas.Body>
            </Navbar.Offcanvas>
          </Container>
        </Navbar>
      ))}
    </>
  );
}

const nav = document.getElementById('navbar');

render(<NavbarComponent />, nav);
