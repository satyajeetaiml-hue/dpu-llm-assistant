import { useEffect, useState } from "react";

// Generic data-fetching hook for simple GET-style service calls.
export function useFetch(fetcher, deps = []) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let active = true;
    setLoading(true);
    fetcher()
      .then((result) => active && setData(result))
      .catch((err) => active && setError(err?.response?.data?.detail || err.message))
      .finally(() => active && setLoading(false));
    return () => {
      active = false;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps);

  return { data, loading, error };
}
