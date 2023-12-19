// src/App.js

import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import GamesPage from './pages/GamesPage';

const App = () => {
  return (
    <Router>
      <Switch>
        <Route path="/games" component={GamesPage} />
        {/* Add more routes for other pages */}
      </Switch>
    </Router>
  );
};

export default App;
