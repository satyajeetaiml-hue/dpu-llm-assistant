import UploadDocuments from "../../components/UploadDocuments/UploadDocuments";

export default function Admin() {
  return (
    <div>
      <h2>Admin — Document Ingestion</h2>
      <p style={{ color: "var(--muted)" }}>
        Upload source documents. Each file is stored in Blob Storage and indexed into
        Azure AI Search for retrieval.
      </p>
      <UploadDocuments />
    </div>
  );
}
