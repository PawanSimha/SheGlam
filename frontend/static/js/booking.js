/**
 * SheGlam – Booking (create, list, accept, complete)
 */

const API_BASE = window.location.origin;

function authHeaders() {
  const token = localStorage.getItem("sheglam_token");
  return {
    "Content-Type": "application/json",
    ...(token ? { Authorization: "Bearer " + token } : {}),
  };
}

async function createBooking(artistId, date, time, requirements) {
  const res = await fetch(API_BASE + "/api/booking", {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify({
      artist_id: artistId,
      date,
      time,
      requirements: requirements || "",
    }),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.error || "Failed to create booking");
  return data;
}

async function fetchBookings() {
  const res = await fetch(API_BASE + "/api/bookings", {
    method: "GET",
    headers: authHeaders(),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.error || "Failed to fetch bookings");
  return Array.isArray(data) ? data : [];
}

async function updateBookingStatus(bookingId, status) {
  const res = await fetch(API_BASE + "/api/booking/" + bookingId + "/status", {
    method: "PUT",
    headers: authHeaders(),
    body: JSON.stringify({ status }),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.error || "Failed to update booking");
  return data;
}

function statusBadgeClass(status) {
  const map = { requested: "badge-requested", accepted: "badge-accepted", completed: "badge-completed" };
  return "badge " + (map[status] || "badge-requested");
}

function renderBookingsList(bookings, options) {
  const { onAccept, onComplete, showArtistName, showUserName } = options || {};
  if (!bookings.length) return "<p class=\"text-muted\">No bookings.</p>";
  const role = localStorage.getItem("sheglam_role");
  let html = "<ul class=\"list-none\" style=\"list-style:none; padding:0;\">";
  bookings.forEach((b) => {
    const id = b._id;
    const status = b.status || "requested";
    let actions = "";
    if (role === "artist" && status === "requested") {
      actions = " <button type=\"button\" class=\"btn btn-primary btn-sm accept-booking\" data-id=\"" + id + "\">Accept</button>";
    }
    if (role === "artist" && (status === "requested" || status === "accepted")) {
      actions += " <button type=\"button\" class=\"btn btn-secondary btn-sm complete-booking\" data-id=\"" + id + "\">Mark complete</button>";
    }
    const name = showArtistName ? (b.artist_name || "Artist") : (b.user_id || "User");
    html += "<li class=\"card mt-1\"><strong>" + name + "</strong> – " + (b.date || "") + " " + (b.time || "") +
      " <span class=\"" + statusBadgeClass(status) + "\">" + status + "</span>" + actions + "</li>";
  });
  html += "</ul>";
  return html;
}

function bindBookingButtons(container) {
  if (!container) return;
  container.addEventListener("click", async (e) => {
    const acceptBtn = e.target.closest(".accept-booking");
    const completeBtn = e.target.closest(".complete-booking");
    const id = (acceptBtn || completeBtn)?.dataset?.id;
    if (!id) return;
    try {
      if (acceptBtn) await updateBookingStatus(id, "accepted");
      else if (completeBtn) await updateBookingStatus(id, "completed");
      if (typeof window.loadBookings === "function") window.loadBookings();
    } catch (err) {
      alert(err.message || "Action failed");
    }
  });
}
