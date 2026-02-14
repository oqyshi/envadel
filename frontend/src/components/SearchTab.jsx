import { useState } from "react";
import { searchAll } from "../api";

export default function SearchTab({ getBookTitle }) {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState({ books: [], authors: [] });

  const handleSearch = async (e) => {
    e.preventDefault();
    try {
      const res = await searchAll(query);
      setResults(res.data);
    } catch (e) {
      console.error(e);
    }
  };

  const hasResults = results.books.length > 0 || results.authors.length > 0;

  return (
    <div className="p-6">
      <h3 className="text-lg font-semibold text-emerald-600 mb-4">
        Search Books & Authors
      </h3>
      <form onSubmit={handleSearch} className="flex gap-3">
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search by title, description, or author name..."
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
      <div className="mt-5 space-y-5">
        {results.books.length > 0 && (
          <div>
            <h4 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-2">
              Books
            </h4>
            <div className="space-y-3">
              {results.books.map((book, idx) => (
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
            </div>
          </div>
        )}
        {results.authors.length > 0 && (
          <div>
            <h4 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-2">
              Authors
            </h4>
            <div className="space-y-3">
              {results.authors.map((author, idx) => (
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
            </div>
          </div>
        )}
        {!hasResults && query && (
          <p className="text-sm text-gray-400 italic">No results found</p>
        )}
      </div>
    </div>
  );
}
