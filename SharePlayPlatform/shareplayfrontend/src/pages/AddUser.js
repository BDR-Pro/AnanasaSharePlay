import React, { useState } from 'react';

function AddUser() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [nickname, setNickname] = useState('');

  const handleAddUser = async () => {
    try {
      // Perform client-side validation
      if (!username || !email || !nickname) {
        console.error('Please fill in all fields.');
        return;
      }

      // Perform API request to add the user to the backend
      const response = await fetch('/api/addUser/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username,
          email,
          nickname,
        }),
      });

      if (response.ok) {
        console.log('User added successfully!');
        // Reset the form fields after adding the user
        setUsername('');
        setEmail('');
        setNickname('');
      } else {
        console.error('Failed to add user. Please try again.');
      }
    } catch (error) {
      console.error('Error adding user:', error);
    }
  };

  return (
    <div>
      <h2>Add User</h2>
      <form>
        <label>
          Username:
          <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} />
        </label>
        <br />
        <label>
          Email:
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
        </label>
        <br />
        <label>
          Nickname:
          <input type="text" value={nickname} onChange={(e) => setNickname(e.target.value)} />
        </label>
        <br />
        <button type="button" onClick={handleAddUser}>
          Add User
        </button>
      </form>
    </div>
  );
}

export default AddUser;
