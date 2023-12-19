import React, { useState, useEffect } from 'react';

function NewTransaction() {
  const [selectedUser, setSelectedUser] = useState('');
  const [selectedGame, setSelectedGame] = useState('');
  const [pricePerHour, setPricePerHour] = useState('');
  const [startTime, setStartTime] = useState('');
  const [endTime, setEndTime] = useState('');
  const [users, setUsers] = useState([]);
  const [games, setGames] = useState([]);

  // Fetch users and games from the backend on component mount
  useEffect(() => {
    const fetchUsersAndGames = async () => {
      try {
        // Fetch users
        const usersResponse = await fetch('/api/users/');
        const usersData = await usersResponse.json();
        setUsers(usersData);

        // Fetch games
        const gamesResponse = await fetch('/api/games/');
        const gamesData = await gamesResponse.json();
        setGames(gamesData);
      } catch (error) {
        console.error('Error fetching users and games:', error);
      }
    };

    fetchUsersAndGames();
  }, []);

  const handleInitiateTransaction = async () => {
    try {
      // Perform client-side validation
      if (
        !selectedUser ||
        !selectedGame ||
        !pricePerHour ||
        parseFloat(pricePerHour) <= 0 ||
        !startTime ||
        !endTime
      ) {
        console.error('Please fill in all required fields with valid values.');
        return;
      }

      // Perform API request to initiate a new transaction
      const response = await fetch('/api/newInvoice/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user: selectedUser, // User initiating the transaction
          rented_user: rentedUser, // User for whom the game is being rented
          game: selectedGame,
          price_per_hour: parseFloat(pricePerHour),
          start: startTime,
          end: endTime,
        }),
      });

      if (response.ok) {
        console.log('Transaction initiated successfully!');
        // Reset the form fields after initiating the transaction
        setSelectedUser('');
        setSelectedGame('');
        setPricePerHour('');
        setStartTime('');
        setEndTime('');
      } else {
        console.error('Failed to initiate transaction. Please try again.');
      }
    } catch (error) {
      console.error('Error initiating transaction:', error);
    }
  };

  return (
    <div>
      <h2>Initiate New Transaction</h2>
      <form>
        <label>
          User:
          <select value={selectedUser} onChange={(e) => setSelectedUser(e.target.value)}>
            <option value="">Select User</option>
            {users.map((user) => (
              <option key={user.id} value={user.id}>
                {user.username}
              </option>
            ))}
          </select>
        </label>
        <br />
        <label>
          Game:
          <select value={selectedGame} onChange={(e) => setSelectedGame(e.target.value)}>
            <option value="">Select Game</option>
            {games.map((game) => (
              <option key={game.id} value={game.id}>
                {game.title}
              </option>
            ))}
          </select>
        </label>
        <br />
        <label>
          Price Per Hour:
          <input
            type="number"
            value={pricePerHour}
            onChange={(e) => setPricePerHour(e.target.value)}
          />
        </label>
        <br />
        <label>
          Start Time:
          <input
            type="datetime-local"
            value={startTime}
            onChange={(e) => setStartTime(e.target.value)}
          />
        </label>
        <br />
        <label>
          End Time:
          <input
            type="datetime-local"
            value={endTime}
            onChange={(e) => setEndTime(e.target.value)}
          />
        </label>
        <br />
        <button type="button" onClick={handleInitiateTransaction}>
          Initiate Transaction
        </button>
      </form>
    </div>
  );
}

export default NewTransaction;
