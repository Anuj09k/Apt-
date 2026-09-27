import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || "http://127.0.0.1:8000";

// Exported for the streaming chat, which uses fetch rather than axios: EventSource cannot
// POST, and the conversation has to go up with the request.
export const API_BASE = `${BACKEND_URL}/api`;

export const api = axios.create({
  baseURL: API_BASE,
  withCredentials: true,
});

/** The auth headers axios adds by interceptor, for callers that bypass axios. */
export const authHeaders = () => {
  const token = localStorage.getItem("aptimizer_token");
  return token ? { Authorization: `Bearer ${token}` } : {};
};

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("aptimizer_token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

export function apiError(detail, fallback = "Something went wrong. Please try again.") {
  if (detail == null) return fallback;
  if (typeof detail === "string") return detail;
  if (Array.isArray(detail))
    return detail.map((e) => (e && typeof e.msg === "string" ? e.msg : JSON.stringify(e))).join(" ");
  if (detail && typeof detail.msg === "string") return detail.msg;
  return String(detail);
}

export async function downloadFile(path, filename) {
  try {
    const res = await api.get(path, { responseType: "blob" });

    // Handle case where server returned a JSON error payload disguised as a blob
    if (res.data instanceof Blob && res.data.type && res.data.type.includes("application/json")) {
      const text = await res.data.text();
      try {
        const json = JSON.parse(text);
        throw new Error(json.detail || "Server error occurred during export.");
      } catch (parseErr) {
        throw new Error(text || "Export failed.");
      }
    }

    const blob = res.data instanceof Blob ? res.data : new Blob([res.data]);
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = filename || "download";
    link.style.display = "none";
    document.body.appendChild(link);
    link.click();

    // Do NOT revoke immediately: Chromium requires the blob URL to remain active while downloading
    setTimeout(() => {
      if (link.parentNode) {
        link.parentNode.removeChild(link);
      }
      window.URL.revokeObjectURL(url);
    }, 45000);
  } catch (err) {
    if (err.response && err.response.data instanceof Blob) {
      try {
        const text = await err.response.data.text();
        const json = JSON.parse(text);
        err.message = json.detail || err.message;
      } catch (_) {}
    }
    throw err;
  }
}

/** Push the site layout engine's packed blocks into the project's tower list.
 *
 *  The engine decides how many buildings the land takes and how many floors each carries,
 *  so Apartment Planning and the 3D model read those numbers from here rather than each
 *  keeping their own. `siteLayout` is the layout the caller just computed — it is sent
 *  because it is usually still ahead of the autosaved copy on the server.
 */
export const syncTowersFromLayout = async (projectId, siteLayout) => {
  if (!projectId) return null;
  const { data } = await api.post(`/projects/${projectId}/towers/sync-from-layout`, {
    site_layout: siteLayout || null,
  });
  return data;
};
