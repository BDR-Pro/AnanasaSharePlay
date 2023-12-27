import React, { useState, useEffect } from 'react';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Form from 'react-bootstrap/Form';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';
import Offcanvas from 'react-bootstrap/Offcanvas';
import { render } from 'react-dom';

function NavbarComponent() {
  const [searchQuery, setSearchQuery] = useState('');
  const [isAuthenticated, setIsAuthenticated] = useState(false); // Assuming initial state is not authenticated

  useEffect(() => {
    const checkAuthentication = async () => {
      try {
        const response = await fetch('/users');
        if (response.ok) {
          const data = await response.json();
          setIsAuthenticated(data.message === 'User is authenticated');
        } else {
          setIsAuthenticated(false);
        }
      } catch (error) {
        console.error('Error checking authentication:', error);
        setIsAuthenticated(false);
      }
    };

    checkAuthentication();
  }, []);

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
              {/* ... (Same as your existing code) */}
              <Offcanvas.Body>
                <Nav className="justify-content-end flex-grow-1 pe-3">

                  {!isAuthenticated && (
                    <>
                      <Nav.Link href="/login">Login</Nav.Link>
                      <Nav.Link href="/register">Sign up</Nav.Link>
                    </>
                  )}

                  {isAuthenticated && (
                    <>
                   <Nav.Link href="/profile">Profile</Nav.Link>
                   <Nav.Link href="/users/logout">Logout</Nav.Link>
                   </> 
                  )}
                  <NavDropdown
                    title="Library"
                    id={`offcanvasNavbarDropdown-expand-${expand}`}
                  >
                    <NavDropdown.Item href="/MyGames">My Games</NavDropdown.Item>
                    <NavDropdown.Item href="/profile/rents">
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
