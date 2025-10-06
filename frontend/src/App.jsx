import { useState } from "react";
import axios from "axios";

function App() {
  const [name, setName] = useState("");
  const [desc, setDesc] = useState("");
  const [file, setFile] = useState(null);
  const [queryText, setQueryText] = useState("");
  const [queryFile, setQueryFile] = useState(null);
  const [results, setResults] = useState([]);

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
      <div className="max-w-3xl mx-auto bg-white p-6 rounded-2xl shadow-lg">
        <h1 className="text-3xl font-bold text-purple-700 mb-4">📤 Upload Item</h1>
        <div className="flex flex-col space-y-3 mb-6">
          <input 
            placeholder="Name" 
            value={name} 
            onChange={e => setName(e.target.value)} 
            className="p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-purple-400"
          />
          <input 
            placeholder="Description" 
            value={desc} 
            onChange={e => setDesc(e.target.value)} 
            className="p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-purple-400"
          />
          <input 
            type="file" 
            onChange={e => setFile(e.target.files[0])} 
            className="p-2"
          />
          <button 
            onClick={uploadItem} 
            className="bg-purple-500 hover:bg-purple-600 text-white font-semibold py-2 rounded-md transition"
          >
            Upload
          </button>
        </div>

        <h1 className="text-3xl font-bold text-purple-700 mb-4">🔍 Search Item</h1>
        <div className="flex flex-col space-y-3 mb-6">
          <input 
            placeholder="Search text" 
            value={queryText} 
            onChange={e => setQueryText(e.target.value)} 
            className="p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-purple-400"
          />
          <input 
            type="file" 
            onChange={e => setQueryFile(e.target.files[0])} 
            className="p-2"
          />
          <button 
            onClick={searchItem} 
            className="bg-purple-500 hover:bg-purple-600 text-white font-semibold py-2 rounded-md transition"
          >
            Search
          </button>
        </div>

        <h2 className="text-2xl font-bold text-purple-600 mb-4">Results:</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {results.map(r => (
            <div key={r.id} className="bg-purple-50 p-4 rounded-xl shadow-md hover:shadow-lg transition">
              {r.image_url && (
                <img 
                  src={`http://localhost:8000${r.image_url}`} 
                  alt={r.name} 
                  className="w-full h-48 object-cover rounded-lg mb-3"
                />
              )}
              <p className="text-lg font-semibold text-purple-700">{r.name}</p>
              <p className="text-purple-600 mb-2">{r.description}</p>
              <p className="text-purple-800 font-medium">Similarity: {r.score.toFixed(3)}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default App;
