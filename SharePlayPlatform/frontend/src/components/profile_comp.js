// Import React and other necessary libraries
import React, { useEffect, useState } from 'react';
import { render } from 'react-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faUser, faAt, faEdit,faTrash,faEye, faDollarSign,faCartShopping } from '@fortawesome/free-solid-svg-icons';
import 'bootstrap/dist/css/bootstrap.min.css'; // Import Bootstrap CSS
import { MDBContainer, MDBRow, MDBCol, MDBCard, MDBCardBody, MDBCardText, MDBCardImage } from 'mdb-react-ui-kit';
import ProfileEdit from './ProfileEdit'; // Import the ProfileEdit component
import { Button } from 'react-bootstrap';
import RatingStars from './RatingStars';

// CommonProfile component
const CommonProfile = ({ userInfo, onEditClick, isEditable }) => {
  return (
    <div>
      {/* Header Section */}
      <div className="rounded-top text-white d-flex flex-row" id="background" style={{ backgroundImage: `url(${userInfo.header})`, width: '100%', height: '200px', borderRadius: '10px' }}>
        {/* Avatar and Edit Button */}
        <div className="ms-4 mt-5 d-flex flex-column" style={{ width: '150px' }}>
          <MDBCardImage src={userInfo.avatar} alt="Avatar" className="mt-4 mb-2 img-thumbnail" fluid style={{ width: '150px', zIndex: '1' }} />
          {isEditable ? (
            <Button variant="secondary" style={{ height: '36px', overflow: 'visible' }} onClick={onEditClick}>
              <FontAwesomeIcon icon={faEdit} className="me-2" />
              Edit profile
            </Button>
          ) : null}
        </div>
        {/* User Details */}
        <div className="ms-3" style={{ marginTop: '130px' }}>
          <div style={{ backgroundColor: '#dbd9d9', display: 'inline-block', padding: '8px', borderRadius: '4px' }}>
            <MDBCardText className="mb-0">
              <FontAwesomeIcon icon={faUser} className="me-2" />
              {userInfo.nickname}
            </MDBCardText>
            <MDBCardText className="text-muted mb-0">
              <FontAwesomeIcon icon={faAt} className="me-2" />
              {userInfo.username}
            </MDBCardText>
          </div>
        </div>
      </div>
      {/* Statistics Section */}
      <div className="p-4 text-black" style={{ backgroundColor: '#f8f9fa' }}>
        <div className="d-flex justify-content-end text-center py-1">
          <div>
            <MDBCardText className="mb-1 h5">{userInfo.playedGames}</MDBCardText>
            <MDBCardText className="small text-muted mb-0">Played Games</MDBCardText>
          </div>
          <div className="px-3">
            <MDBCardText className="mb-1 h5">{userInfo.NumberOfListedGames}</MDBCardText>
            <MDBCardText className="small text-muted mb-0">Listed Games</MDBCardText>
          </div>
          <div>
            <MDBCardText className="mb-1 h5">{userInfo.revenue}</MDBCardText>
            <MDBCardText className="small text-muted mb-0">Revenue</MDBCardText>
          </div>
        </div>
      </div>
      {/* Main Content */}
      <MDBCardBody className="text-black p-4">
        <div className="mb-5">
          <p className="lead fw-normal mb-1">About</p>
          <div className="p-4" style={{ backgroundColor: '#f8f9fa' }}>
            <MDBCardText className="font-italic mb-1">{userInfo.bio}</MDBCardText>
          </div>
        </div>
        {/* Recent Played Games Section */}
        <div className="d-flex justify-content-between align-items-center mb-4">
          <MDBCardText className="lead fw-normal mb-0">Recent played games</MDBCardText>
          {userInfo.isCurrentUser ? (
            <MDBCardText className="mb-0">
              <a href="/Profile/rents" className="text-muted">Show all</a>
            </MDBCardText>
          ) : null}
        </div>
        <MDBRow>
          {userInfo.recentlyPlayedGames ? (
            userInfo.recentlyPlayedGames.map((game, index) => (
              <MDBCol lg="3" md="6" className="mb-4 mb-lg-0" key={`game-${index}`}>
                <a href={`/game/${game.game_slug}`}>
                  <div className="card rounded shadow-sm border-0">
                    <div className="card-body p-4"><img src={game.game_avatar} alt="" className="img-fluid d-block mx-auto mb-3" />
                      <p className="small text-muted font-italic">{game.game_title}</p>
                      <p className="small text-muted d-flex align-items-center">
                        <FontAwesomeIcon icon={faDollarSign} className="me-1" />
                        {game.revenue}
                      </p>
                    </div>
                  </div>
                </a>
              </MDBCol>
            ))
          ) : null}
        </MDBRow>
        {/* Games For Rent Section */}
        <div className="d-flex justify-content-between align-items-center mb-4">
          <MDBCardText className="lead fw-normal mb-0">Games For Rent</MDBCardText>
          {userInfo.isCurrentUser ? (
            <MDBCardText className="mb-0">
              <a href={`/Profile/listed/${window.location.pathname.split('/')[2]}`} className="text-muted">Show all</a>
            </MDBCardText>
          ) : null}
        </div>
              <MDBRow>{userInfo.mylistedGames ? (
  userInfo.mylistedGames.map((game, index) => (
    <MDBCol lg="3" md="6" className="mb-4 mb-lg-0" key={`game-${index}`}>
      <div className="card rounded shadow-sm border-0">
        <img src={game.game_avatar} alt="" className="card-img-top img-fluid" />
        <div className="card-body p-4">
          <h5 className="card-title">{game.title}</h5>
          <p className="card-text small text-muted font-italic">{game.game_title}</p>
          <p className="card-text small text-muted d-flex align-items-center">
            <FontAwesomeIcon icon={faDollarSign} className="me-1" />
            {game.price_per_hour}
          </p>
          <div className="d-flex justify-content-between mt-3">
          <a href={`/game/${game.game_slug}`} className="btn btn-info btn-sm">
            <FontAwesomeIcon icon={faEye} className="me-2" />
            View
          </a>
          <div>
            <a href={`/rent-your-game/${game.id}`} className="btn btn-secondary btn-sm me-2">
              <FontAwesomeIcon icon={faCartShopping} className="me-2" />
              Book
            </a>
            {userInfo.isCurrentUser ? (
              <a href={`/delete-your-game/${game.id}`} className="btn btn-danger btn-sm">
                <FontAwesomeIcon icon={faTrash} className="me-2" />
                Delete
              </a>
            ) : null}
          </div>
        </div>

        </div>
      </div>
    </MDBCol>
  ))
) : null}

        </MDBRow>
        {/* Reviews Section */}
        <MDBRow>
          <MDBCardText className="lead fw-normal mb-0">Reviews for the streamer</MDBCardText>
          {userInfo.reviews ? (
            userInfo.reviews.map((review, index) => (
              <MDBCol lg="3" md="6" className="mb-4 mb-lg-0" key={`review-${index}`}>
                <a href={`/user/${review.user}`}>
                  <div className="card rounded shadow-sm border-0">
                    <div className="card-body p-4"><img src={review.user_avatar} alt="" className="img-fluid d-block mx-auto mb-3" />
                      <p className="small">{review.content}</p>
                      <RatingStars rating={review.rating} />
                      <a href={`/game/${review.game_slug}`}>
                        <p className="small text-muted d-flex align-items-center">
                          {review.game_title}
                        </p>
                      </a>
                      <p className="small text-muted d-flex align-items-center">
                        {review.user_nickname}
                      </p>
                    </div>
                  </div>
                </a>
              </MDBCol>
            ))
          ) : null}
        </MDBRow>
      </MDBCardBody>
    </div>
  );
};

// Profile component
const Profile = () => {
  const [userInfo, setUserInfo] = useState({});
  const [isCurrentUser, setIsCurrentUser] = useState(false);
  const [isEditing, setIsEditing] = useState(false);

  const handleEditClick = () => {
    setIsEditing(true);
  };

  useEffect(() => {
    // Simulated fetch request to get user profile data
    // Replace this with your actual fetch logic
    fetch('/api/getProfile/' + window.location.pathname.split('/')[2] + '/')
      .then(response => response.json())
      .then(data => {
        setUserInfo(data);
        if (data.isCurrentUser) {
          setIsCurrentUser(true);
        } else {
          setIsCurrentUser(false);
        }
      });
  }, []);

  return (
    <div className="gradient-custom-2" style={{ backgroundColor: '#edf4f7' }}>
      <MDBContainer className="py-5 h-100">
        <MDBRow className="justify-content-center align-items-center h-100">
          <MDBCol lg="9" xl="7">
            <MDBCard>
              {isEditing ? (
                <ProfileEdit userInfo={userInfo} />
              ) : (
                <CommonProfile userInfo={userInfo} onEditClick={handleEditClick} isEditable={isCurrentUser} />
              )}
            </MDBCard>
          </MDBCol>
        </MDBRow>
      </MDBContainer>
    </div>
  );
};

// Render the Profile component
const profileDiv = document.getElementById('profile');
render(<Profile />, profileDiv);
