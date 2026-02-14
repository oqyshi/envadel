import { useState, useEffect } from "react";
import axios from "axios";

const CORE_API = import.meta.env.VITE_CORE_API_URL || "http://localhost:8000";
const SEARCH_API =
  import.meta.env.VITE_SEARCH_API_URL || "http://localhost:8001";

const TABS = [
  { id: "search-books", label: "Search Books" },
  { id: "search-authors", label: "Search Authors" },
  { id: "all-books", label: "All Books" },
  { id: "all-authors", label: "All Authors" },
  { id: "add-author", label: "Add Author" },
  { id: "add-book", label: "Add Book" },
];

function App() {
  const [activeTab, setActiveTab] = useState("search-books");

  const [authors, setAuthors] = useState([]);
  const [books, setBooks] = useState([]);
  const [authorName, setAuthorName] = useState("");

  const [bookTitle, setBookTitle] = useState("");
  const [bookDesc, setBookDesc] = useState("");
  const [selectedAuthorId, setSelectedAuthorId] = useState("");

  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [reindexing, setReindexing] = useState(false);

  useEffect(() => {
    fetchAuthors();
    fetchBooks();
  }, []);

  const fetchAuthors = async () => {
    try {
      const res = await axios.get(`${CORE_API}/authors/`);
      setAuthors(res.data);
      if (res.data.length > 0 && !selectedAuthorId)
        setSelectedAuthorId(res.data[0]._id);
    } catch (e) {
      console.error("Failed to load authors", e);
    }
  };

  const fetchBooks = async () => {
    try {
      const res = await axios.get(`${CORE_API}/books/`);
      setBooks(res.data);
    } catch (e) {
      console.error("Failed to load books", e);
    }
  };

  const createAuthor = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`${CORE_API}/authors/`, {
        name: authorName,
        book_ids: [],
      });
      setAuthorName("");
      fetchAuthors();
      alert("Author created!");
    } catch (e) {
      console.error(e);
    }
  };

  const createBook = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`${CORE_API}/books/`, {
        title: bookTitle,
        description: bookDesc,
        author_ids: [selectedAuthorId],
      });
      setBookTitle("");
      setBookDesc("");
      fetchBooks();
      alert("Book created!");
    } catch (e) {
      console.error(e);
    }
  };

  const handleSearch = async (e, index) => {
    e.preventDefault();
    try {
      const res = await axios.get(
        `${SEARCH_API}/search/?query=${searchQuery}&index=${index}`,
      );
      setSearchResults(res.data);
    } catch (e) {
      console.error(e);
    }
  };

  const handleReindex = async () => {
    setReindexing(true);
    try {
      const res = await axios.post(`${SEARCH_API}/reindex/`);
      alert(`Reindex complete: ${res.data.indexed.books} books, ${res.data.indexed.authors} authors`);
    } catch (e) {
      console.error(e);
      alert("Reindex failed");
    } finally {
      setReindexing(false);
    }
  };

  const getAuthorName = (authorId) => {
    const author = authors.find((a) => a._id === authorId);
    return author ? author.name : authorId;
  };

  const getBookTitle = (bookId) => {
    const book = books.find((b) => b._id === bookId);
    return book ? book.title : bookId;
  };

  const renderTabContent = () => {
    switch (activeTab) {
      case "search-books":
        return (
          <div className="p-6">
            <h3 className="text-lg font-semibold text-emerald-600 mb-4">
              Search Books (Elasticsearch)
            </h3>
            <form
              onSubmit={(e) => handleSearch(e, "books")}
              className="flex gap-3"
            >
              <input
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search by title or description..."
                required
                className="flex-1 rounded-lg border border-gray-300 px-4 py-2.5 text-sm focus:border-emerald-500 focus:ring-2 focus:ring-emerald-200 outline-none transition"
              />
              <button
                type="submit"
                className="rounded-lg bg-emerald-600 px-5 py-2.5 text-sm font-medium text-white hover:bg-emerald-700 transition"
              >
                Search
              </button>
            </form>
            <div className="mt-5 space-y-3">
              {searchResults.map((book, idx) => (
                <div
                  key={idx}
                  className="rounded-lg border border-gray-100 bg-gray-50 p-4"
                >
                  <p className="font-medium text-gray-900">{book.title}</p>
                  <p className="mt-1 text-sm text-gray-500">
                    {book.description}
                  </p>
                </div>
              ))}
              {searchResults.length === 0 && searchQuery && (
                <p className="text-sm text-gray-400 italic">
                  No results found
                </p>
              )}
            </div>
          </div>
        );

      case "search-authors":
        return (
          <div className="p-6">
            <h3 className="text-lg font-semibold text-emerald-600 mb-4">
              Search Authors (Elasticsearch)
            </h3>
            <form
              onSubmit={(e) => handleSearch(e, "authors")}
              className="flex gap-3"
            >
              <input
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search by author name..."
                required
                className="flex-1 rounded-lg border border-gray-300 px-4 py-2.5 text-sm focus:border-emerald-500 focus:ring-2 focus:ring-emerald-200 outline-none transition"
              />
              <button
                type="submit"
                className="rounded-lg bg-emerald-600 px-5 py-2.5 text-sm font-medium text-white hover:bg-emerald-700 transition"
              >
                Search
              </button>
            </form>
            <div className="mt-5 space-y-3">
              {searchResults.map((author, idx) => (
                <div
                  key={idx}
                  className="rounded-lg border border-gray-100 bg-gray-50 p-4"
                >
                  <p className="font-medium text-gray-900">{author.name}</p>
                  {author.book_ids && author.book_ids.length > 0 && (
                    <p className="mt-1 text-sm text-gray-500">
                      Books: {author.book_ids.map(getBookTitle).join(", ")}
                    </p>
                  )}
                </div>
              ))}
              {searchResults.length === 0 && searchQuery && (
                <p className="text-sm text-gray-400 italic">
                  No results found
                </p>
              )}
            </div>
          </div>
        );

      case "all-books":
        return (
          <div className="p-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">
              All Books
            </h3>
            {books.length === 0 ? (
              <p className="text-sm text-gray-400 italic">No books yet</p>
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b-2 border-gray-200">
                      <th className="px-4 py-3 text-left font-semibold text-gray-600">
                        Title
                      </th>
                      <th className="px-4 py-3 text-left font-semibold text-gray-600">
                        Description
                      </th>
                      <th className="px-4 py-3 text-left font-semibold text-gray-600">
                        Authors
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    {books.map((book) => (
                      <tr
                        key={book._id}
                        className="border-b border-gray-100 hover:bg-gray-50 transition"
                      >
                        <td className="px-4 py-3 font-medium text-gray-900">
                          {book.title}
                        </td>
                        <td className="px-4 py-3 text-gray-500">
                          {book.description}
                        </td>
                        <td className="px-4 py-3 text-gray-500">
                          {book.author_ids
                            ? book.author_ids.map(getAuthorName).join(", ")
                            : "—"}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        );

      case "all-authors":
        return (
          <div className="p-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">
              All Authors
            </h3>
            {authors.length === 0 ? (
              <p className="text-sm text-gray-400 italic">No authors yet</p>
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b-2 border-gray-200">
                      <th className="px-4 py-3 text-left font-semibold text-gray-600">
                        Name
                      </th>
                      <th className="px-4 py-3 text-left font-semibold text-gray-600">
                        Books
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    {authors.map((author) => (
                      <tr
                        key={author._id}
                        className="border-b border-gray-100 hover:bg-gray-50 transition"
                      >
                        <td className="px-4 py-3 font-medium text-gray-900">
                          {author.name}
                        </td>
                        <td className="px-4 py-3 text-gray-500">
                          {author.book_ids && author.book_ids.length > 0
                            ? author.book_ids.map(getBookTitle).join(", ")
                            : "—"}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        );

      case "add-author":
        return (
          <div className="p-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">
              Add Author
            </h3>
            <form onSubmit={createAuthor} className="flex gap-3">
              <input
                value={authorName}
                onChange={(e) => setAuthorName(e.target.value)}
                placeholder="Author name (e.g. George Martin)"
                required
                className="flex-1 rounded-lg border border-gray-300 px-4 py-2.5 text-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 outline-none transition"
              />
              <button
                type="submit"
                className="rounded-lg bg-indigo-600 px-5 py-2.5 text-sm font-medium text-white hover:bg-indigo-700 transition"
              >
                Create
              </button>
            </form>
          </div>
        );

      case "add-book":
        return (
          <div className="p-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">
              Add Book
            </h3>
            <form onSubmit={createBook} className="flex flex-col gap-3 max-w-md">
              <input
                value={bookTitle}
                onChange={(e) => setBookTitle(e.target.value)}
                placeholder="Book title"
                required
                className="rounded-lg border border-gray-300 px-4 py-2.5 text-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 outline-none transition"
              />
              <input
                value={bookDesc}
                onChange={(e) => setBookDesc(e.target.value)}
                placeholder="Description"
                required
                className="rounded-lg border border-gray-300 px-4 py-2.5 text-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 outline-none transition"
              />
              <select
                value={selectedAuthorId}
                onChange={(e) => setSelectedAuthorId(e.target.value)}
                required
                className="rounded-lg border border-gray-300 px-4 py-2.5 text-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 outline-none transition bg-white"
              >
                {authors.map((a) => (
                  <option key={a._id} value={a._id}>
                    {a.name}
                  </option>
                ))}
              </select>
              <button
                type="submit"
                className="self-start rounded-lg bg-indigo-600 px-5 py-2.5 text-sm font-medium text-white hover:bg-indigo-700 transition"
              >
                Create Book
              </button>
            </form>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="mx-auto max-w-4xl px-4 py-8">
        <div className="flex items-center justify-between mb-8">
          <h1 className="text-3xl font-bold text-gray-900">
            Microservice Library
          </h1>
          <button
            onClick={handleReindex}
            disabled={reindexing}
            className="rounded-lg bg-amber-500 px-4 py-2 text-sm font-medium text-white hover:bg-amber-600 disabled:opacity-50 transition"
          >
            {reindexing ? "Reindexing..." : "Sync to Search"}
          </button>
        </div>

        <div className="flex flex-wrap gap-1 border-b border-gray-200">
          {TABS.map((tab) => (
            <button
              key={tab.id}
              onClick={() => {
                setActiveTab(tab.id);
                setSearchResults([]);
                setSearchQuery("");
              }}
              className={`px-4 py-2.5 text-sm font-medium rounded-t-lg transition ${
                activeTab === tab.id
                  ? "bg-white text-gray-900 border border-gray-200 border-b-white -mb-px"
                  : "text-gray-500 hover:text-gray-700 hover:bg-gray-100"
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>

        <div className="rounded-b-xl bg-white border border-t-0 border-gray-200 shadow-sm">
          {renderTabContent()}
        </div>
      </div>
    </div>
  );
}

export default App;
