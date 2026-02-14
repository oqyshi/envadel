import { useState, useEffect, useCallback } from "react";
import { fetchAuthors as apiFetchAuthors, fetchBooks as apiFetchBooks, reindex } from "./api";
import SearchTab from "./components/SearchTab";
import BooksTab from "./components/BooksTab";
import AuthorsTab from "./components/AuthorsTab";

const TABS = [
  { id: "search", label: "Search" },
  { id: "all-books", label: "Books" },
  { id: "all-authors", label: "Authors" },
];

function App() {
  const [activeTab, setActiveTab] = useState(() => {
    const hash = window.location.hash.slice(1);
    return TABS.some((t) => t.id === hash) ? hash : "search";
  });
  const [authors, setAuthors] = useState([]);
  const [books, setBooks] = useState([]);
  const [reindexing, setReindexing] = useState(false);

  const fetchAuthors = useCallback(async () => {
    try {
      const res = await apiFetchAuthors();
      setAuthors(res.data);
    } catch (e) {
      console.error("Failed to load authors", e);
    }
  }, []);

  const fetchBooks = useCallback(async () => {
    try {
      const res = await apiFetchBooks();
      setBooks(res.data);
    } catch (e) {
      console.error("Failed to load books", e);
    }
  }, []);

  useEffect(() => {
    fetchAuthors();
    fetchBooks();
  }, [fetchAuthors, fetchBooks]);

  const handleReindex = async () => {
    setReindexing(true);
    try {
      const res = await reindex();
      alert(`Reindex complete: ${res.data.indexed.books} books, ${res.data.indexed.authors} authors`);
    } catch (e) {
      console.error(e);
      alert("Reindex failed");
    } finally {
      setReindexing(false);
    }
  };

  const getAuthorName = useCallback(
    (authorId) => {
      const author = authors.find((a) => a._id === authorId);
      return author ? author.name : authorId;
    },
    [authors],
  );

  const getBookTitle = useCallback(
    (bookId) => {
      const book = books.find((b) => b._id === bookId);
      return book ? book.title : bookId;
    },
    [books],
  );

  const renderTabContent = () => {
    switch (activeTab) {
      case "search":
        return <SearchTab getBookTitle={getBookTitle} />;
      case "all-books":
        return (
          <BooksTab
            books={books}
            authors={authors}
            getAuthorName={getAuthorName}
            onBookCreated={fetchBooks}
          />
        );
      case "all-authors":
        return (
          <AuthorsTab
            authors={authors}
            getBookTitle={getBookTitle}
            onAuthorCreated={fetchAuthors}
          />
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
              onClick={() => { setActiveTab(tab.id); window.location.hash = tab.id; }}
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
