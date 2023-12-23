// profile.js

import React, { useEffect, useState } from 'react';
import { render } from 'react-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faUser, faAt, faEdit } from '@fortawesome/free-solid-svg-icons';
import 'bootstrap/dist/css/bootstrap.min.css'; // Import Bootstrap CSS
import { MDBContainer, MDBRow, MDBCol, MDBCard, MDBCardBody, MDBCardText, MDBCardImage } from 'mdb-react-ui-kit';
import ProfileEdit from './ProfileEdit'; // Import the ProfileEdit component
import { Button } from 'react-bootstrap';

const CommonProfile = ({ userInfo, onEditClick, isEditable }) => {
  return (
    <div>
      <div className="rounded-top text-white d-flex flex-row" id="background" style={{ backgroundImage: `url(${userInfo.header})`, width: '100%', height: '200px', borderRadius: '10px' }}>
        <div className="ms-4 mt-5 d-flex flex-column" style={{ width: '150px' }}>
          <MDBCardImage src={userInfo.avatar} alt="Avatar" className="mt-4 mb-2 img-thumbnail" fluid style={{ width: '150px', zIndex: '1' }} />
          {isEditable ? (
            <Button variant="secondary" style={{ height: '36px', overflow: 'visible'}} onClick={onEditClick}>
              <FontAwesomeIcon icon={faEdit} className="me-2" />
              Edit profile
            </Button>
          ) : null}
        </div>
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
      <div className="p-4 text-black" style={{ backgroundColor: '#f8f9fa' }}>
        <div className="d-flex justify-content-end text-center py-1">
          <div>
            <MDBCardText className="mb-1 h5">253</MDBCardText>
            <MDBCardText className="small text-muted mb-0">Photos</MDBCardText>
          </div>
          <div className="px-3">
            <MDBCardText className="mb-1 h5">1026</MDBCardText>
            <MDBCardText className="small text-muted mb-0">Followers</MDBCardText>
          </div>
          <div>
            <MDBCardText className="mb-1 h5">478</MDBCardText>
            <MDBCardText className="small text-muted mb-0">Following</MDBCardText>
          </div>
        </div>
      </div>
      <MDBCardBody className="text-black p-4">
        <div className="mb-5">
          <p className="lead fw-normal mb-1">About</p>
          <div className="p-4" style={{ backgroundColor: '#f8f9fa' }}>
            <MDBCardText className="font-italic mb-1">{userInfo.bio}</MDBCardText>
          </div>
        </div>
        <div className="d-flex justify-content-between align-items-center mb-4">
          <MDBCardText className="lead fw-normal mb-0">Recent played games</MDBCardText>
          <MDBCardText className="mb-0"><a href="#!" className="text-muted">Show all</a></MDBCardText>
        </div>
        <MDBRow>
          <MDBCol className="mb-2">
            {/* Add your recent played games content here */}
          </MDBCol>
        </MDBRow>
      </MDBCardBody>
    </div>
  );
};

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
        const currentuser = window.location.pathname.split('/')[2];
        const user = window.location.pathname.split('/')[2];

        if (currentuser === user) {
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

const profileDiv = document.getElementById('profile');
render(<Profile />, profileDiv);
