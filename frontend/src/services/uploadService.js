import client from "../api/client";

export async function uploadDocument({ file, category }) {
  const form = new FormData();
  form.append("file", file);
  form.append("category", category);
  const { data } = await client.post("/api/upload", form, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return data;
}
