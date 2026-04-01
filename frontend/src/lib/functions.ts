import axios from "axios";

import {
  BACKEND_URL,
} from "./constants";

export class Username {
  static set(username) {
    localStorage.setItem("username", username);
  }
  static get() {
    return localStorage.getItem("username");
  }
  static async fetch() {
    const response = await axios.get(BACKEND_URL + "accounts/api/get_username", {withCredentials: true});
    //console.log(response);
    //axios.default.headers.post['X-CSRF-Token'] = response.data._csrf;
    return response.data.username;
  }
}
