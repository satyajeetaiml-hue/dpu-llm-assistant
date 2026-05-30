import client from "../api/client";

export async function getAdmissionAnalytics() {
  const { data } = await client.get("/api/analytics/admissions");
  return data;
}
