import axios from "axios";

import {
  expect,
  test,
  describe,
} from "vitest";

import {
  login,
} from "../lib/functions";

describe("login", () => {
  test("stores the DRF token in an axios-instance.", async () => {
    const axiosInst = axios.create({baseURL: "http://localhost:8000/"});
    const username = "eclair";
    const password = "eclair";
    const response = await login(axiosInst, {username, password});
    console.log(response);
  });
});
