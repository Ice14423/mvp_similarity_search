import { useState } from "react";
import axios from "axios";

function App() {
  const [name, setName] = useState("");
  const [desc, setDesc] = useState("");
  const [file, setFile] = useState(null);
  const [filePreview, setFilePreview] = useState(null); // preview upload
  const [queryText, setQueryText] = useState("");
  const [queryFile, setQueryFile] = useState(null);
  const [queryFilePreview, setQueryFilePreview] = useState(null); // preview search
  const [results, setResults] = useState([]);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);
    setFilePreview(selectedFile ? URL.createObjectURL(selectedFile) : null);
  };

  const handleQueryFileChange = (e) => {
    const selectedFile = e.target.files[0];
    setQueryFile(selectedFile);
    setQueryFilePreview(selectedFile ? URL.createObjectURL(selectedFile) : null);
  };

  const uploadItem = async () => {
    try {
      const formData = new FormData();
      formData.append("name", name);
      formData.append("description", desc);
      if (file) formData.append("file", file);

      await axios.post("http://localhost:8000/upload", formData);
      alert("Uploaded!");
      setName("");
      setDesc("");
      setFile(null);
      setFilePreview(null);
    } catch (err) {
      console.error(err);
      alert("Upload failed");
    }
  };

  const searchItem = async () => {
    try {
      const formData = new FormData();
      if (queryText) formData.append("text", queryText);
      if (queryFile) formData.append("file", queryFile);

      const res = await axios.post("http://localhost:8000/search", formData);
      setResults(res.data.results);
    } catch (err) {
      console.error(err);
      alert("Search failed");
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-r from-pink-200 via-purple-200 to-blue-200 p-6">
      <div className="max-w-xl mx-auto bg-white p-4 rounded-2xl shadow-lg">

        {/* Upload */}
        <h1 className="text-2xl font-bold text-purple-700 mb-4">📤 Upload Item</h1>
        <div className="flex flex-col space-y-3 mb-6">
          <input
            placeholder="Name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-purple-400"
          />
          <input
            placeholder="Description"
            value={desc}
            onChange={(e) => setDesc(e.target.value)}
            className="p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-purple-400"
          />
          <input
            type="file"
            onChange={handleFileChange}
            className="p-2"
          />
          {filePreview && (
            <img
              src={filePreview}
              alt="Preview"
              className="w-full rounded-lg mb-3"
              style={{ height: "auto" }}
            />
          )}
          <button
            onClick={uploadItem}
            className="bg-purple-500 hover:bg-purple-600 text-white font-semibold py-2 rounded-md transition"
          >
            Upload
          </button>
        </div>

        {/* Search */}
        <h1 className="text-2xl font-bold text-purple-700 mb-4">🔍 Search Item</h1>
        <div className="flex flex-col space-y-3 mb-6">
          <input
            placeholder="Search text"
            value={queryText}
            onChange={(e) => setQueryText(e.target.value)}
            className="p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-purple-400"
          />
          <input
            type="file"
            onChange={handleQueryFileChange}
            className="p-2"
          />
          {queryFilePreview && (
            <img
              src={queryFilePreview}
              alt="Search Preview"
              className="w-full rounded-lg mb-3"
              style={{ height: "auto" }}
            />
          )}
          <button
            onClick={searchItem}
            className="bg-purple-500 hover:bg-purple-600 text-white font-semibold py-2 rounded-md transition"
          >
            Search
          </button>
        </div>

        {/* Results */}
        <h2 className="text-xl font-bold text-purple-600 mb-4">Results:</h2>
        <div className="grid grid-cols-1 gap-4">
          {results.map(r => (
            <div key={r.id} className="bg-purple-50 p-4 rounded-xl shadow-md hover:shadow-lg transition">
              {r.image_base64 && (
                <img
                  src={`data:image/png;base64,${r.image_base64}`}
                  alt={r.name}
                  className="w-full rounded-lg mb-3"
                  style={{ height: "auto" }}
                />
              )}
              <p className="font-semibold">{r.name}</p>
              <p>{r.description}</p>
              <p>Similarity: {r.score.toFixed(3)}</p>
              {r.text_vector && (
                <p className="text-sm text-gray-700">
                  Text vector: {r.text_vector.slice(0,2).join(", ")} ... {r.text_vector.slice(-2).join(", ")}
                </p>
              )}
              {r.image_vector && (
                <p className="text-sm text-gray-700">
                  Image vector: {r.image_vector.slice(0,2).join(", ")} ... {r.image_vector.slice(-2).join(", ")}
                </p>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default App;
