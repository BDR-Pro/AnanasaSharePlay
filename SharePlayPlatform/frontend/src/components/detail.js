import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import Card from 'react-bootstrap/Card';
import Container from 'react-bootstrap/Container';
import { render } from 'react-dom';

const Detail = () => {
  // Get the slug from the data attribute
  const element = document.getElementById('detail');
  const slug = element ? element.getAttribute('data-slug') : null;

  if (!slug) {
    // Handle the case when slug is not available
    console.error('No slug provided');
    return <div>No slug provided</div>;
  }

  const [gameDetails, setGameDetails] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Fetch game details based on the slug
    fetch(`/api/gamesdetail/${slug}/`)
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => setGameDetails(data))
      .catch(error => {
        console.error('Error fetching data:', error);
        setError('Error fetching data. Please try again later.');
      });
  }, [slug]);

  if (error) {
    return <div>{error}</div>;
  }

  if (!gameDetails) {
    return <div>Loading...</div>;
  }

  return (
    <Container className="mt-4">
      <Card>
        <Card.Img
          variant="top"
          src={gameDetails.image || 'placeholder-image-url'}
          style={{ maxWidth: '30%', height: 'auto' }}
          className="d-flex justify-content-center mx-auto mt-3"
        />
        <Card.Body>
          <Card.Title className="h2">{gameDetails.title}</Card.Title>
          <Card.Text className="lead">{gameDetails.description}</Card.Text>
          <Card.Text className="text-muted">{gameDetails.genre}</Card.Text>
        </Card.Body>
      </Card>
    </Container>
  );
};
export default Detail;

// Assuming you have a div with id 'detail' in your HTML
const appDetail = document.getElementById('detail');

render(<Detail />, appDetail);
