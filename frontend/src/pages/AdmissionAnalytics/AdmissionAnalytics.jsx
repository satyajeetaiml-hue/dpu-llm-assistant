import Dashboard from "../../components/Dashboard/Dashboard";
import { useFetch } from "../../hooks/useFetch";
import { getAdmissionAnalytics } from "../../services/analyticsService";

export default function AdmissionAnalytics() {
  const { data, loading, error } = useFetch(getAdmissionAnalytics, []);

  return (
    <div>
      <h2>Admission Analytics</h2>
      {loading && <p>Loading…</p>}
      {error && <p style={{ color: "#f87171" }}>{error}</p>}
      {data && <Dashboard data={data} />}
    </div>
  );
}
