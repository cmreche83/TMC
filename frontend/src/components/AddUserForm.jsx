import React, { useState } from 'react';

const AddUserForm = ({ addUser }) => {
  const [userValues, setUserValues] = useState({});

  const handleSubmit = (event) => {
    event.preventDefault();
    if (userValues) {
      console.log("Submitted");
      addUser(userValues);
      setUserValues({});
    }
  };
  
  const handleChange = (event) => {
    const name = event.target.name;
    const value = event.target.value;
    setUserValues(values => ({...values, [name]: value}))
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        name="userFirstName"
        value={userValues.userFirstName || ""}
        onChange={handleChange}
        placeholder="User firstname"
      />
      <input
        type="text"
        name="userLastName"
        value={userValues.userLastName || ""}
        onChange={handleChange}
        placeholder="User lastname"
      />
      <input
        type="text"
        name="userDateOfBirth"
        value={userValues.userDateOfBirth || ""}
        onChange={handleChange}
        placeholder="date of birth dd-mm-yyyy"
      />
      <button type="submit">Add User</button>
    </form>
  );
};

export default AddUserForm;