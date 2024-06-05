import axios from 'axios';

const axiosInstance = axios.create({
  baseURL: 'http://testeb-env.eba-3tf5iadp.us-east-1.elasticbeanstalk.com',
  timeout: 1000,
  headers: { 'X-Custom-Header': 'foobar' }
});

export default axiosInstance;
