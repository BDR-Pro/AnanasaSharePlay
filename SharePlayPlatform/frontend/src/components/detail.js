import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom'; // Assuming you are using React Router
import Card from 'react-bootstrap/Card';
import Container from 'react-bootstrap/Container';

const Detail = () => {
  const { slug } = useParams();
  const [gameDetails, setGameDetails] = useState(null);
  slug = window.slugFromDjango;
  useEffect(() => {
    // Fetch game details based on the slug
    fetch('/api/gamesdetail/${slug}')
      .then(response => response.json())
      .then(data => setGameDetails(data))
      .catch(error => console.error('Error fetching data:', error));
  }, [slug]);

  if (!gameDetails) {
    return <div>Loading...</div>;
  }

  return (
    <Container className="detail-container">
      <Card>
        <Card.Img
          variant="top"
          src={gameDetails.image}
          className="detail-image"
        />
        <Card.Body>
          <Card.Title>{gameDetails.title}</Card.Title>
          <Card.Text>{gameDetails.description}</Card.Text>
          <Card.Text>
            <strong>Genre:</strong> {gameDetails.genre}
          </Card.Text>
        </Card.Body>
      </Card>
    </Container>
  );
};

export default Detail;
