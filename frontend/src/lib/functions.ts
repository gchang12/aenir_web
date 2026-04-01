import axios from "axios";

import {
  BACKEND_URL,
} from "./constants";

const AXIOS_INST = axios.create(
  {
    baseURL: BACKEND_URL,
  },
);

export async function login(axiosInst, {username, password}) {
  const response = await axios.post(BACKEND_URL + "accounts/login", {username, password});
  console.log(response);
}
