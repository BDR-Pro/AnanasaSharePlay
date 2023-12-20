import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Card from 'react-bootstrap/Card';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import Detail from './detail'; // Import your Detail component
import { render } from 'react-dom';

const App = () => {
  const [games, setGames] = useState([]);

  useEffect(() => {
    // Fetch games from your API and update the state
    fetch('/api/gameslist')
      .then(response => response.json())
      .then(data => setGames(data))
      .catch(error => console.error('Error fetching data:', error));
  }, []); // The empty dependency array ensures the effect runs once on mount

  return (
    <Router>
      <Switch>
        {/* Route for the game list */}
        <Route exact path="/">
          <Row xs={2} md={2} className="g-4">
            {games.map((game) => (
              <Col key={game.id}>
                <a href={`/game/${game.slug}`}>
                  <Card>
                    <Card.Img
                      variant="top"
                      src={game.image}
                      style={{ maxWidth: '100%', height: 'auto' }}
                      className="d-flex justify-content-center mx-auto mt-3"
                    />
                    <Card.Body className="text-center">
                      <Card.Title>{game.title}</Card.Title>
                      <Card.Text className="description">{game.description}</Card.Text>
                    </Card.Body>
                  </Card>
                </a>
              </Col>
            ))}
          </Row>
        </Route>

        {/* Route for individual game details */}
        <Route path="/game/:slug">
          <Detail />
        </Route>
      </Switch>
    </Router>
  );
};

export default App;


const appDiv = document.getElementById('app');
render(<App />, appDiv);
