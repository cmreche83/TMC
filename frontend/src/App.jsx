import React from 'react';
import './App.css';
import UserList from './components/Users';

const App = () => {
  return (
    <div className="App">
      <header className="App-header">
        <h1>User Management</h1>
      </header>
      <main>
        <UserList />
      </main>
    </div>
  );
};

export default App;