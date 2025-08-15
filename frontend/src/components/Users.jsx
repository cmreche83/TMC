import React, { useEffect, useState } from 'react';
import api from "../api.js";
import AddUserForm from './AddUserForm';


const UserList = () => {
  let [users, setUsers] = useState([]);

  const fetchUsers = async () => {
    try {
      const response = await api.get('/users');
      console.log("response data")
      console.log(response.data)
      setUsers(response.data);
    } catch (error) {
      console.error("Error fetching users", error);
    }
  };

  const addUser = async (userValues) => {
    try {
      await api.post('/users/create', { firstname: userValues.userFirstName, lastname: userValues.userLastName, date_of_birth: userValues.userDateOfBirth });
      fetchUsers();  // Refresh the list ...
    } catch (error) {
      console.error("Error adding user", error);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  const deleteUser = async (id) => {
    try {
      await api.delete('/user/'+id);
      fetchUsers();fetchUsers();
    } catch (error) {
      console.error("Error deleting user", error);
    }
  };
    
  return (
    <div>
      <h2>Users List</h2>
      <table>
        <tbody>
        <tr>
          <th>First Name</th>
          <th>Last Name</th>
          <th>Age</th>
          <th>Date Of Birth</th>
          <th></th>
        </tr>
        {users.map((user, index) => (
          <tr key={index}>
            <td>{user.firstname}</td>
            <td>{user.lastname}</td>
            <td>{user.age}</td>
            <td>{user.date_of_birth}</td>
            <td><button type="button" onClick={() => deleteUser(user.id)}>-</button></td>
          </tr>
        ))}
        </tbody>
      </table>
      <hr></hr>
      <AddUserForm addUser={addUser} />
    </div>
  );
};

export default UserList;