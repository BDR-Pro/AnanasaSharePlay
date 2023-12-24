import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import Card from 'react-bootstrap/Card';
import Container from 'react-bootstrap/Container';
import { render } from 'react-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faHeart } from '@fortawesome/free-solid-svg-icons';

const Detail = () => {
  const slug = window.location.pathname.split('/')[2];
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isFav, setIsFav] = useState(false);
  const [gameDetails, setGameDetails] = useState(null);
  const [error, setError] = useState(null);
  const csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;

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

  useEffect(() => {
    const checkFavStatus = async () => {
      try {
        const response = await fetch(`/api/isFav/${slug}`);
        if (response.ok) {
          const data = await response.json();
          setIsFav(data.status === 'success');
        } else {
          setIsFav(false);
        }
      } catch (error) {
        console.error('Error checking favorite status:', error);
        setIsFav(false);
      }
    };

    checkFavStatus();
  }, [slug]);

  useEffect(() => {
    // Fetch game details based on the slug
    const fetchGameDetails = async () => {
      try {
        const response = await fetch(`/api/gamesdetail/${slug}/`);
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        setGameDetails(data);
      } catch (error) {
        console.error('Error fetching game details:', error);
        setError('Error fetching game details. Please try again later.');
      }
    };

    fetchGameDetails();
  }, [slug]);

  if (error) {
    return <div>{error}</div>;
  }

  if (!gameDetails) {
    return <div>Loading...</div>;
  }

  const addFav = async () => {
    try {
      const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' ,
        'X-CSRFToken': csrfToken
      },
        body: JSON.stringify({ slug }),
      };

      const response = await fetch(`/game/${slug}/`, requestOptions);
      const data = await response.json();
      console.log(data);
    } catch (error) {
      console.error('Error adding to favorites:', error);
    }
    window.location.reload();
  };

  const removeFav = async () => {
    try {
      const requestOptions = {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' ,
        'X-CSRFToken': csrfToken
      },
        body: JSON.stringify({ slug }),
      };

      const response = await fetch(`/game/${slug}/`, requestOptions);
      const data = await response.json();
      console.log(data);
    } catch (error) {
      console.error('Error removing from favorites:', error);
    }
    window.location.reload();

  };

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
          <a href={`/game/genre/${gameDetails.genre}`}>
          <Card.Text className="text-muted">{gameDetails.genre}</Card.Text>
           </a>

          {isAuthenticated && isFav && (
            <button className="btn btn-success" onClick={removeFav} >
              Remove from Favorites
              <FontAwesomeIcon icon={faHeart} color="red" size="2x" />
            </button>
          )}
          {isAuthenticated && !isFav && (
            <button className="btn btn-info" onClick={addFav}>
              Add to Favorites
              <FontAwesomeIcon icon={faHeart} color="grey" size="2x" />
            </button>
          )}
        </Card.Body>
      </Card>
    </Container>
  );
};

// Assuming you have a div with id 'detail' in your HTML
const appDetail = document.getElementById('detail');

render(<Detail />, appDetail);
