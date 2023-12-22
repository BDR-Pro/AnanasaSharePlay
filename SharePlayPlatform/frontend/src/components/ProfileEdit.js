import React, { useState, useEffect } from 'react';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Alert from 'react-bootstrap/Alert';
import { render } from 'react-dom';

const ProfileEdit = () => {
  const [errorMessage, setErrorMessage] = useState(null);
  const [userInfo, setUserInfo] = useState({});

  useEffect(() => {
    // Simulated fetch request to get user profile data
    // Replace this with your actual fetch logic
    fetch('/api/getProfile/' + window.location.pathname.split('/')[2] + '/')
      .then(response => response.json())
      .then(data => {
        setUserInfo(data);
      });
  }, []); // <- Add the dependency array here

  const handleSubmit = async (event) => {
    event.preventDefault();

    const formData = new FormData(event.target);
    const csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;

    try {
      const response = await fetch('/api/updateProfile/', {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrfToken,
        },
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message);
      }

      // Update successful
      setErrorMessage(null);
      console.log('Profile update successful!');
    } catch (error) {
      // Handle error
      setErrorMessage(error.message);
    }
  };

  return (
    <div>
      {errorMessage && (
        <Alert variant="danger" onClose={() => setErrorMessage(null)} dismissible>
          <Alert.Heading>Error</Alert.Heading>
          <p>{errorMessage}</p>
        </Alert>
      )}
      <div className="ProfileEditFormContainer">
        <div className="ProfileEditFormWrapper">
          <Form encType="multipart/form-data" onSubmit={handleSubmit}>
            {/* Include fields for updating profile information */}
            <Form.Group controlId="formBasicUsername">
              <Form.Label>Username</Form.Label>
              <Form.Control type="text" defaultValue={userInfo.username} name="username" />
            </Form.Group>
            <Form.Group controlId="formBasicEmail">
              <Form.Label>Email</Form.Label>
              <Form.Control type="email" defaultValue={userInfo.email} name="email" />
            </Form.Group>
            <Form.Group controlId="formBasicBio">
              <Form.Label>Bio</Form.Label>
              <Form.Control as="textarea" rows={3} defaultValue={userInfo.bio} name="bio" />
            </Form.Group>
            <Form.Group controlId="formBasicAvatar">
              <Form.Label>Avatar</Form.Label>
              <Form.Control type="file" name="avatar" />
            </Form.Group>

            {/* Add this block for the header file input */}
            <Form.Group controlId="formBasicHeader">
              <Form.Label>Header</Form.Label>
              <Form.Control type="file" name="header" />
            </Form.Group>

            {/* ... */}
            <Button variant="primary" type="submit">
              Save Changes
            </Button>
          </Form>
        </div>
      </div>
    </div>
  );
};

export default ProfileEdit;

// Use the ProfileEdit component in your application
const appDiv = document.getElementById('profile');
render(<ProfileEdit />, appDiv);
