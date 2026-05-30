import { useState } from "react";
import { uploadDocument } from "../../services/uploadService";

const CATEGORIES = ["admissions", "policies", "ciqa", "examination", "syllabus"];

export default function UploadDocuments() {
  const [file, setFile] = useState(null);
  const [category, setCategory] = useState(CATEGORIES[0]);
  const [status, setStatus] = useState(null);
  const [busy, setBusy] = useState(false);

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) return;
    setBusy(true);
    setStatus(null);
    try {
      const result = await uploadDocument({ file, category });
      setStatus(`Indexed ${result.chunks_indexed} chunks from ${result.filename}.`);
    } catch (err) {
      setStatus(err?.response?.data?.detail || err.message);
    } finally {
      setBusy(false);
    }
  };

  return (
    <form onSubmit={handleUpload} style={{ display: "grid", gap: 12, maxWidth: 480 }}>
      <label>
        Category
        <select value={category} onChange={(e) => setCategory(e.target.value)}>
          {CATEGORIES.map((c) => (
            <option key={c} value={c}>
              {c}
            </option>
          ))}
        </select>
      </label>
      <input type="file" accept=".txt,.md" onChange={(e) => setFile(e.target.files[0])} />
      <button type="submit" disabled={busy || !file}>
        {busy ? "Uploading…" : "Upload & Index"}
      </button>
      {status && <p style={{ color: "var(--muted)" }}>{status}</p>}
    </form>
  );
}
