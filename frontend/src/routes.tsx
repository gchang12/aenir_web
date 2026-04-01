import {
  Outlet,
  Link,
  Form,
} from "react-router";

import {
  Username,
} from "./lib/functions";

export function Root() {
  const username = Username.get();
  return (
    <>
    <header>
      <img id="logo" src="/logo.png" />
      <div id="user_status">
        {username == null ? (
          <>
          <span id="username">You are not logged in.</span>
          <a href="/accounts/login/">Login</a>
          </>
        ) : (
          <>
          <span id="username">{username}</span>
          <a href="/accounts/logout/">Logout</a>
          </>
        )}
      </div>
    </header>
    <Outlet />
    </>
  );
}
