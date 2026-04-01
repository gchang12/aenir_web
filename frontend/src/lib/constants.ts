import Cookies from "js-cookie";

export const csrftoken = Cookies.get("csrftoken");

export const BACKEND_URL = "http://localhost:8000/";
