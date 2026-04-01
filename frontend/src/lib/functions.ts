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
  const response = await axiosInst(
    {
      method: "post",
      url: "accounts/login/",
      data: {username, password},
    }
  );
  return response;
}
