import { useState } from "react";
import { createAuthor as apiCreateAuthor } from "../api";
import Modal from "./Modal";

export default function AuthorsTab({ authors, getBookTitle, onAuthorCreated }) {
  const [showModal, setShowModal] = useState(false);
  const [name, setName] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await apiCreateAuthor(name);
      setName("");
      setShowModal(false);
      onAuthorCreated();
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-800">All Authors</h3>
        <button
          onClick={() => setShowModal(true)}
          className="rounded-lg bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-700 transition"
        >
          + Add Author
        </button>
      </div>
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
                      : "\u2014"}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
      <Modal open={showModal} onClose={() => setShowModal(false)} title="Add Author">
        <form onSubmit={handleSubmit} className="flex gap-3">
          <input
            value={name}
            onChange={(e) => setName(e.target.value)}
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
      </Modal>
    </div>
  );
}
