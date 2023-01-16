import React, { useContext } from "react";
import authContext from "./authContext";

// eslint-disable-next-line import/no-anonymous-default-export
export default () => {
  const { setAuthenticated, setAuthenticated2 } = useContext(authContext);
  const handleLogin = () => setAuthenticated({'login' : 'true'});
  const handleLogout = () => setAuthenticated2({'login' : 'false'});

  return (
    <React.Fragment>
      <button onClick={handleLogin}>Auth1</button>
      <button onClick={handleLogout}>Auth2</button>
    </React.Fragment>
  );
};