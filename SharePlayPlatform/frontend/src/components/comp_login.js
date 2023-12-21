import React, { useState } from 'react';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Alert from 'react-bootstrap/Alert';
import { render } from 'react-dom';

function LoginForm() {
  const [showAlert, setShowAlert] = useState(false);
  const [alertMessage, setAlertMessage] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();

    const formData = new FormData(event.target);

    try {
      const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
      const response = await fetch('/users/login/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({
          username: formData.get('username'),
          password: formData.get('password'),
        }),
      });

      const jsonResponse = await response.json(); // Parse the JSON response

      if (response.ok) {
        // Handle success (optional)
        console.log('Form data sent successfully!');
      } else {
        // Handle unsuccessful login
        setShowAlert(true);
        setAlertMessage('Email or password is wrong. Please try again or sign up.');
      }
    } catch (error) {
      // Handle error
      console.error('Error sending form data:', error);
    }
  };

  return (
    <div className="FormContainer">
      <div className="FormWrapper">
        {showAlert && (
          <Alert variant="danger" onClose={() => setShowAlert(false)} dismissible>
            <Alert.Heading>Email or password are wrong!</Alert.Heading>
            <p>{alertMessage}</p>
          </Alert>
        )}
        <Form method="POST" onSubmit={handleSubmit}>
          <Form.Group className="mb-3" controlId="formBasicEmail">
            <Form.Label>Username</Form.Label>
            <Form.Control type="text" name="username" id="username" placeholder="Enter Username" />
            <Form.Text className="text-muted">
            </Form.Text>
          </Form.Group>

          <Form.Group className="mb-3" controlId="formBasicPassword">
            <Form.Label>Password</Form.Label>
            <Form.Control type="password" id="password" name="password" placeholder="Password" />
          </Form.Group>

          <Button variant="primary" type="submit">
            Submit
          </Button>
        </Form>
      </div>
    </div>
  );
}

const appLogin = document.getElementById('app');
render(<LoginForm />, appLogin);
