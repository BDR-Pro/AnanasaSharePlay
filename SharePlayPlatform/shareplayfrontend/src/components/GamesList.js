// src/components/GamesList.js

import React, { useState, useEffect } from 'react';

const GamesList = () => {
  const [games, setGames] = useState([]);

  useEffect(() => {
    // Fetch data from the Django API endpoint
    fetch('/api/games')
      .then(response => response.json())
      .then(data => setGames(data))
      .catch(error => console.error('Error fetching games:', error));
  }, []);

  return (
    <div>
      <h2>Games List</h2>
      <ul>
        {games.map(game => (
          <li key={game.id}>{game.title}</li>
        ))}
      </ul>
    </div>
  );
};

export default GamesList;
