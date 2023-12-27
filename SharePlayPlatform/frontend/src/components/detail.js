// Detail.js
import React, { useEffect, useState } from 'react';
import Card from 'react-bootstrap/Card';
import Container from 'react-bootstrap/Container';
import Button from 'react-bootstrap/Button';
import { render } from 'react-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import RatingStars from './RatingStars.js';
import { faHeart } from '@fortawesome/free-solid-svg-icons';
import Badge from 'react-bootstrap/Badge';
import Avatar from '@material-ui/core/Avatar';
import { getUserNickname, getAvatarById } from './utils';

const Detail = ({ context }) => {
  const slug = window.location.pathname.split('/')[2];
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isFav, setIsFav] = useState(false);
  const [gameDetails, setGameDetails] = useState(null);
  const [error, setError] = useState(null);
  const [comments, setComments] = useState(null);
  const [userNicknames, setUserNicknames] = useState({});
  const [userAvatars, setUserAvatars] = useState({});
  const csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;

  useEffect(() => {
    const getComments = async () => {
      try {
        const response = await fetch(`/api/getComments/${slug}/`);
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        setComments(data);
      } catch (error) {
        console.error('Error fetching comments:', error);
        setError('Error fetching comments. Please try again later.');
      }
    };

    getComments();
  }, [slug]);

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

  const fetchUserNicknames = async () => {
    const newNicknames = {};
    await Promise.all(
      comments.map(async (comment) => {
        if (!userNicknames[comment.user]) {
          const nickname = await getUserNickname(comment.user);
          newNicknames[comment.user] = nickname || comment.user;
        }
      })
    );
    setUserNicknames((prev) => ({ ...prev, ...newNicknames }));
  };

  useEffect(() => {
    fetchUserNicknames();
  }, [comments]);

  const fetchUserAvatars = async () => {
    const newAvatars = {};
    await Promise.all(
      comments.map(async (comment) => {
        if (!userAvatars[comment.user]) {
          const avatarId = comment.user; // Adjust this line based on how the user ID is represented
          const avatar = await getAvatarById(avatarId);
          newAvatars[comment.user] = avatar || '/default-avatar.jpg';
        }
      })
    );
    setUserAvatars((prev) => ({ ...prev, ...newAvatars }));
  };

  useEffect(() => {
    fetchUserAvatars();
  }, [comments]);

  const addFav = async () => {
    try {
      const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken },
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
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken },
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

  const handleComment = async (e) => {
    e.preventDefault();
    const rating = e.target.rating.value;
    const review = e.target.review.value;
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken },
      body: JSON.stringify({ rating, review }),
    };
    const response = await fetch(`/api/addComment/${slug}`, requestOptions);
    const data = await response.json();
    data.status === 'success' ? alert('Comment added successfully') : alert('Error adding comment');
    console.log(data);
    window.location.reload();
  };

  console.log(context)

  return (
    <Container className="mt-4">
      <Card>
        <Card.Img
          variant="top"
          src={gameDetails?.image}
          style={{ maxWidth: '30%', height: 'auto' }}
          className="d-flex justify-content-center mx-auto mt-3"
        />
        <Card.Body>
          <Card.Title className="h2">{gameDetails?.title}</Card.Title>
          <Card.Text className="lead">{gameDetails?.description}</Card.Text>
          <a href={`/game/genre/${gameDetails?.genre}`}>
            <Card.Text className="text-muted">{gameDetails?.genre}</Card.Text>
          </a>
          <div className="mt-3">
            <Badge variant="primary" className="mr-2">
              Views: {context.views}
            </Badge>
            <Badge variant="success" className="mr-2">
              Renters: {context.NumberOfRenters}
            </Badge>
            <Badge variant="danger" className="mr-2">
              Favorites: {context.NumberOfFavorites}
            </Badge>
            <Badge variant="warning" className="mr-2">
              Streamers: {context.NumberOfStreamers}
            </Badge>
            <Badge variant="info">
              Owners: {context.NumberOfOwners}
            </Badge>
            <Badge variant="info">
              Comments: {context.NumberOfComments}
            </Badge>
            
            <Badge variant="info">
            <RatingStars rating={context.AvgRating} /> {context.AvgRating}
            </Badge>
          </div>
          <p></p>

          {isAuthenticated && (
            <Button className="btn btn-info">
              <a href='listing' style={{ color: 'white', textDecoration: 'none' }}>
                Rent the game
              </a>
            </Button>
          )}

          {isAuthenticated && isFav && (
            <Button className="btn btn-success" onClick={removeFav}>
              Remove from Favorites
              <FontAwesomeIcon icon={faHeart} color="red" />
            </Button>
          )}
          {isAuthenticated && !isFav && (
            <Button className="btn btn-info" onClick={addFav}>
              Add to Favorites
              <FontAwesomeIcon icon={faHeart} color="grey" />
            </Button>
          )}

          <Card.Title className="h2" style={{ marginTop: '20px' }}>
            Comments
          </Card.Title>
          <Card.Text className="lead">
            {comments &&
              comments.map((comment) => (
                <Card key={comment.id} style={{ marginTop: '10px' }}>
                  <Card.Body>
                    <a href={`/users/comment/${comment.user}`} className="user-link">
                      <Avatar
                        alt={userNicknames[comment.user]}
                        src={userAvatars[comment.user]}
                        style={{ marginRight: '10px' }}
                      />
                      <h6>{userNicknames[comment.user]}</h6>
                    </a>
                    <RatingStars rating={comment.rating} />
                    <p>{comment.review}</p>
                  </Card.Body>
                </Card>
              ))}
            {comments && comments.length === 0 && <p>No comments yet.</p>}
            {isAuthenticated && (
              <form action={`/api/addComment/${slug}`} method="POST" onSubmit={handleComment}>
                <input type="hidden" name="csrfmiddlewaretoken" value={csrfToken} />
                <div className="form-group">
                  <label htmlFor="rating">Rating</label>
                  <input
                    type="number"
                    className="form-control"
                    id="rating"
                    name="rating"
                    min="1"
                    max="5"
                    required
                  />
                </div>
                <div className="form-group">
                  <label htmlFor="review">Review</label>
                  <textarea
                    className="form-control"
                    id="review"
                    name="review"
                    rows="3"
                    required
                  ></textarea>
                </div>
                <button type="submit" className="btn btn-info">
                  Submit
                </button>
              </form>
            )}
            {!isAuthenticated && (
              <p>
                Please <a href="/login">log in</a> to leave a comment.
              </p>
            )}
          </Card.Text>
        </Card.Body>
        <Card.Footer>
          <small className="text-muted">
            Last updated {gameDetails?.updated_at}
          </small>
        </Card.Footer>
      </Card>
    </Container>
  );
};

export default Detail;

const appDetail = document.getElementById('detail');
document.addEventListener('DOMContentLoaded', function(){
const contextData = JSON.parse(document.getElementById('context').textContent);
render(<Detail context={contextData} />, appDetail);

});

