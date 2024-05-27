// src/axios.js
import axios from 'axios';

const axiosInstance = axios.create({
  baseURL: 'http://localhost:8080/api', // 这里是你的 Flask API 的基础 URL
  timeout: 1000,
  headers: {'X-Custom-Header': 'foobar'}
});

export default axiosInstance;
