# Product Requirements Document (PRD) - SheGlam

## 1. Problem Statement
Finding reliable, high-quality makeup artists for special occasions is often a fragmented and stressful process. Users struggle with availability, pricing transparency, and trust, while talented artists lack a centralized platform to showcase their work and manage bookings efficienty.

## 2. Target Audience
-   **Clients**: Women aged 18-45 looking for makeup services for weddings, parties, photoshoots, or casual events.
-   **Artists**: Professional makeup artists and hairstylists seeking a digital platform to grow their business and manage clients.

## 3. Core Features

### User Features
-   **Registration/Login**: Secure email-based signup.
-   **Search & Discovery**: Filter artists by category, price range, and location.
-   **Artist Profiles**: View portfolios, read reviews, and check pricing.
-   **Booking Management**: Request bookings, view status updates, and history.
-   **Reviews**: Rate and review artists after service completion.

### Artist Features
-   **Portfolio Management**: Upload photos of past work.
-   **Service Listing**: Define services and pricing.
-   **Booking Control**: Accept or reject booking requests.
-   **Dashboard**: View earnings and upcoming appointments.

### Admin Features
-   **User/Artist Management**: Verify artist credentials and manage user accounts.
-   **Platform Oversight**: Monitor bookings and resolve disputes.

## 4. Technical Architecture

### Frontend
-   **Architecture**: Server-side rendered templates with lightweight client-side interactivity.
-   **Key Libraries**: Tailwind CSS (Styling), FontAwesome (Icons).

### Backend
-   **Framework**: Flask (Python).
-   **API Design**: RESTful routes for scalable interaction.
-   **Authentication**: JWT (JSON Web Tokens) for stateless auth.

### Database
-   **System**: MongoDB (NoSQL).
-   **Collections**: `users` (clients/artists/admins), `bookings`, `reviews`.

## 5. User Flows

### Booking Flow
1.  User logs in and searches for artists.
2.  User views an artist profile and clicks "Book Now".
3.  User fills out booking details (date, time, service type).
4.  Artist receives notification and approves/rejects the request.
5.  User is notified of the status change.

### Onboarding Flow
1.  User signs up as Client or Artist.
2.  **Artists** are required to upload credentials (certificate/ID) for verification.
3.  Admin reviews artist submission and approves account.
4.  Artist can now accept bookings.

## 6. Future Roadmap
-   **Payment Integration**: Secure in-app payments via Stripe/Razorpay.
-   **Real-time Chat**: Direct messaging between clients and artists.
-   **Mobile App**: Native iOS and Android applications.
-   **AI Recommendations**: Personalized artist suggestions based on user style preferences.
