import {
  Outlet,
  Link,
  Form,
} from "react-router";

export function Root() {
  return (
    <>
    <header>
      <img id="logo" src="/logo.png" />
      <div id="user_status">
        <a to="/accounts/login/">Login</a>
        <a to="/accounts/logout/">Logout</a>
      </div>
    </header>
    <Outlet />
    </>
  );
}
