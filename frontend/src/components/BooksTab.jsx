import { useState } from "react";
import { createBook as apiCreateBook } from "../api";
import Modal from "./Modal";

export default function BooksTab({ books, authors, getAuthorName, onBookCreated }) {
  const [showModal, setShowModal] = useState(false);
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [selectedAuthorId, setSelectedAuthorId] = useState(
    authors.length > 0 ? authors[0]._id : "",
  );

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await apiCreateBook(title, description, [selectedAuthorId]);
      setTitle("");
      setDescription("");
      setShowModal(false);
      onBookCreated();
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-800">All Books</h3>
        <button
          onClick={() => setShowModal(true)}
          className="rounded-lg bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-700 transition"
        >
          + Add Book
        </button>
      </div>
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
                      : "\u2014"}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
      <Modal open={showModal} onClose={() => setShowModal(false)} title="Add Book">
        <form onSubmit={handleSubmit} className="flex flex-col gap-3">
          <input
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Book title"
            required
            className="rounded-lg border border-gray-300 px-4 py-2.5 text-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 outline-none transition"
          />
          <input
            value={description}
            onChange={(e) => setDescription(e.target.value)}
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
            className="rounded-lg bg-indigo-600 px-5 py-2.5 text-sm font-medium text-white hover:bg-indigo-700 transition"
          >
            Create Book
          </button>
        </form>
      </Modal>
    </div>
  );
}
