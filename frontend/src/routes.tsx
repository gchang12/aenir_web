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
      <nav>
        <menu>
          <li><Link to="/accounts/login/">Login</Link></li>
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

export function LoginView() {
  return (
    <>
    <Form method="post">
      <label>
        Username
        <input type="text" name="username" required />
      </label>
      <label>
        Password
        <input type="password" name="password" required />
      </label>
      <button>Submit</button>
    </Form>
    <a href="/accounts/password_reset/">Forgot your password?</a>
    <a href="/accounts/create-account/">Need to register for an account?</a>
    </>
  );
}
