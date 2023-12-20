import React, { useState } from 'react';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Alert from 'react-bootstrap/Alert';
import { render } from 'react-dom';

function SignUp() {
  const [errorMessage, setErrorMessage] = useState(null);

  const handleSubmit = async (event) => {
    event.preventDefault();

    const formData = new FormData(event.target);

    try {
      const response = await fetch('/users/register/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken, // Make sure to have csrfToken available
        },
        body: JSON.stringify({
          nickname: formData.get('nickname'),
          email: formData.get('email'),
          password: formData.get('password'),
          avatar: formData.get('avatar'),
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message);
      }

      // Registration successful
      setErrorMessage(null);
      console.log('Registration successful!');
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
    <div className='SignUpFormContainer'>
    <div className='SignUpFormWrapper'>
      <Form onSubmit={handleSubmit}>
        <Form.Group className="mb-3" controlId="formBasicNickname">
          <Form.Label>Nick Name</Form.Label>
          <Form.Control type="text" name="nickname" placeholder="Enter name" />
          <Form.Text className="text-muted">NickName to make you unique</Form.Text>
        </Form.Group>

        <Form.Group className="mb-3" controlId="formBasicEmail">
          <Form.Label>Email address</Form.Label>
          <Form.Control type="email" name="email" placeholder="Enter email" />
          <Form.Text className="text-muted">
            We'll never share your email with anyone else.
          </Form.Text>
        </Form.Group>

        <Form.Group className="mb-3" controlId="formBasicPassword">
          <Form.Label>Password</Form.Label>
          <Form.Control type="password" name="password" placeholder="Password" />
        </Form.Group>

        <Form.Group controlId="formFile" className="mb-3">
          <Form.Label>Avatar</Form.Label>
          <Form.Control type="file" name="avatar" />
        </Form.Group>

        <Button variant="primary" type="submit">
          Submit
        </Button>
      </Form>
    </div>
    </div>
    </div>
  );
}

export default SignUp;

const appDiv = document.getElementById('app');
render(<SignUp />, appDiv);
