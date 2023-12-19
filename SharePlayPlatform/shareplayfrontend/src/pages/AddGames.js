import React, { useState } from 'react';

function AddGames() {
  const [gameTitle, setGameTitle] = useState('');
  const [description, setDescription] = useState('');
  const [image, setImage] = useState(null); // Use state to handle file input
  const [hourlyPrice, setHourlyPrice] = useState('');

  const handleAddGame = async () => {
    try {
      // Perform client-side validation
      if (!gameTitle || !description || !image || !hourlyPrice) {
        console.error('Please fill in all fields.');
        return;
      }

      // Construct form data to include the image file
      const formData = new FormData();
      formData.append('title', gameTitle);
      formData.append('description', description);
      formData.append('image', image);
      formData.append('hourlyPrice', parseFloat(hourlyPrice)); // Ensure hourlyPrice is a number

      // Perform API request to add the game to the backend
      const response = await fetch('/api/addGame/', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        console.log('Game added successfully!');
        // Reset the form fields after adding the game
        setGameTitle('');
        setDescription('');
        setImage(null);
        setHourlyPrice('');
      } else {
        console.error('Failed to add game. Please try again.');
      }
    } catch (error) {
      console.error('Error adding game:', error);
    }
  };

  return (
    <div>
      <h2>Add Game</h2>
      <form encType="multipart/form-data">
        <label>
          Game Title:
          <input type="text" value={gameTitle} onChange={(e) => setGameTitle(e.target.value)} />
        </label>
        <br />
        <label>
          Description:
          <textarea value={description} onChange={(e) => setDescription(e.target.value)} />
        </label>
        <br />
        <label>
          Image:
          <input type="file" accept="image/*" onChange={(e) => setImage(e.target.files[0])} />
        </label>
        <br />
        <label>
          Hourly Price:
          <input
            type="number"
            value={hourlyPrice}
            onChange={(e) => setHourlyPrice(e.target.value)}
          />
        </label>
        <br />
        <button type="button" onClick={handleAddGame}>
          Add Game
        </button>
      </form>
    </div>
  );
}

export default AddGames;
