/**
 * SheGlam – Rating (add review after booking completion, display stars)
 */

const API_BASE = window.location.origin;

function authHeaders() {
  const token = localStorage.getItem("sheglam_token");
  return {
    "Content-Type": "application/json",
    ...(token ? { Authorization: "Bearer " + token } : {}),
  };
}

async function addReview(bookingId, rating, comment) {
  const res = await fetch(API_BASE + "/api/review", {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify({
      booking_id: bookingId,
      rating: Math.min(5, Math.max(1, parseInt(rating, 10) || 5)),
      comment: (comment || "").trim(),
    }),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.error || "Failed to add review");
  return data;
}

function renderStars(rating, options) {
  const { editable = false, name = "rating", inputName = "rating" } = options || {};
  const value = Math.min(5, Math.max(0, parseFloat(rating) || 0));
  let html = '<div class="rating-stars" data-rating="' + value + '">';
  for (let i = 1; i <= 5; i++) {
    const filled = i <= value ? " filled" : "";
    if (editable) {
      html += '<label title="' + i + '"><input type="radio" name="' + inputName + '" value="' + i + '">★</label>';
    } else {
      html += '<span class="' + (filled ? "filled" : "") + '">★</span>';
    }
  }
  html += "</div>";
  return html;
}

function getSelectedRating(container) {
  const input = container && container.querySelector('input[name="rating"]:checked');
  return input ? parseInt(input.value, 10) : 0;
}

function bindReviewForm(formEl, onSuccess) {
  if (!formEl) return;
  formEl.addEventListener("submit", async (e) => {
    e.preventDefault();
    const bookingId = (formEl.querySelector('input[name="booking_id"]') || {}).value;
    const rating = getSelectedRating(formEl) || (formEl.querySelector('input[name="rating"]') || {}).value;
    const comment = (formEl.querySelector('textarea[name="comment"]') || {}).value;
    if (!bookingId || !rating) {
      alert("Please select a rating.");
      return;
    }
    try {
      await addReview(bookingId, rating, comment);
      if (onSuccess) onSuccess();
      else formEl.reset();
    } catch (err) {
      alert(err.message || "Failed to submit review");
    }
  });
}
