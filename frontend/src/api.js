import axios from "axios";

const CORE_API = import.meta.env.VITE_CORE_API_URL || "http://localhost:8000";
const SEARCH_API =
  import.meta.env.VITE_SEARCH_API_URL || "http://localhost:8001";

export const fetchAuthors = () => axios.get(`${CORE_API}/authors/`);

export const fetchBooks = () => axios.get(`${CORE_API}/books/`);

export const createAuthor = (name) =>
  axios.post(`${CORE_API}/authors/`, { name, book_ids: [] });

export const createBook = (title, description, authorIds) =>
  axios.post(`${CORE_API}/books/`, {
    title,
    description,
    author_ids: authorIds,
  });

export const searchAll = (query) =>
  axios.get(`${SEARCH_API}/search/all/`, { params: { query } });

export const reindex = () => axios.post(`${SEARCH_API}/reindex/`);
