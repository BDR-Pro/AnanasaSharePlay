import React, { useState, useEffect } from 'react';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Alert from 'react-bootstrap/Alert';
import axios from 'axios';

const styles = {
  container: {
    height: '100vh',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
  formWrapper: {
    maxWidth: '600px',
    width: '100%',
    padding: '20px',
    borderRadius: '8px',
    boxShadow: '0 0 20px rgba(0, 0, 0, 0.2)',
  },
  label: {
    fontWeight: 'bold',
  },
  input: {
    width: '100%',
    padding: '0.5rem',
    marginBottom: '1rem',
    border: '1px solid #ccc',
    borderRadius: '4px',
    boxSizing: 'border-box',
  },
  button: {
    width: '100%',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    marginTop: '10px',
    marginBottom: '10px',
    height: '50px',
    borderRadius: '5px',
    backgroundColor: '#007bff',
    color: '#fff',
    border: 'none',
    fontSize: '1rem',
    cursor: 'pointer',
  },
  buttonHover: {
    backgroundColor: '#0056b3',
  },
};

const ProfileEdit = () => {
  const [errorMessage, setErrorMessage] = useState(null);
  const [updatedUserData, setUpdatedUserData] = useState(null);
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

    const formData = new FormData();
    const csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;

    formData.append('avatar', event.target.avatar.files[0]);
    formData.append('header', event.target.header.files[0]);
    formData.append('username', event.target.username.value);
    formData.append('email', event.target.email.value);
    formData.append('bio', event.target.bio.value);
    formData.append('password', event.target.password.value);

    try {
      const response = await axios.post('/api/updateProfile/', formData, {
        headers: {
          'X-CSRFToken': csrfToken,
        },
      });

      const updatedUserData = response.data;
      // Update successful
      setErrorMessage(null);
      console.log('Profile update successful!', updatedUserData);
      setUpdatedUserData(updatedUserData);
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
      <div style={styles.container}>
        <div style={styles.formWrapper}>
          {updatedUserData && (
            <Alert variant="success" onClose={() => setUpdatedUserData(null)} dismissible>
              <Alert.Heading>Success</Alert.Heading>
              <p>Your profile has been updated!</p>
              <Button variant="danger" type="submit" style={styles.button} onClick={() => window.location.reload()}>
                Refresh Page
              </Button>
            </Alert>
              
          )
          
          }
          
          <Form encType="multipart/form-data" onSubmit={handleSubmit}>
            <Form.Group controlId="formBasicAvatar">
              <Form.Label>Avatar</Form.Label>
              <Form.Control type="file" name="avatar" />
            </Form.Group>

            <Form.Group controlId="formBasicHeader">
              <Form.Label>Header</Form.Label>
              <Form.Control type="file" name="header" />
            </Form.Group>

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
            
            <Form.Group controlId="formBasicRevenue">
              <Form.Label>Revenue Visibility</Form.Label>
              <Form.Control as="select" defaultValue={userInfo.isRevenuePrivate ? 'private' : 'public'} name="revenueVisibility">
                <option value="private">Private</option>
                <option value="public">Public</option>
              </Form.Control>
            </Form.Group>

            <Form.Group controlId="formBasicPassword">
              <Form.Label>Password</Form.Label>
              <Form.Control type="password" placeholder="Change Your Password" name="password" />
            </Form.Group>

            <Button variant="danger" type="submit" style={styles.button}>
              Save Changes
            </Button>
          </Form>
        </div>
      </div>
    </div>
  );
};

export default ProfileEdit;
