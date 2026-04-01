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
        <a href="/accounts/login/">Login</a>
        <a href="/accounts/logout/">Logout</a>
      </div>
    </header>
    <Outlet />
    </>
  );
}
