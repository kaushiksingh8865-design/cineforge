const API_URL = "http://127.0.0.1:8000";

export async function apiFetch(path, options = {}) {
  const token = localStorage.getItem("access_token");

  const headers = {
    ...(options.headers || {}),
  };

  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  const response = await fetch(
    `${API_URL}${path}`,
    {
      ...options,
      headers,
    }
  );

  return response;
}