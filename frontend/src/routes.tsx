import {
  Outlet,
  Link,
} from "react-router";

export function Root() {
  return (
    <>
    <header>
      <img id="logo" src="/logo.png" />
      <nav>
        <menu>
          <li><Link to="/login/">Login</Link></li>
          <li><Link to="/create-account/">Create Account</Link></li>
        </menu>
      </nav>
    </header>
    <nav>
      <menu>
      </menu>
    </nav>
    <Outlet />
    </>
  );
}
