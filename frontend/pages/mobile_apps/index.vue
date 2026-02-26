<template>
  <div class="bg-light min-vh-100">

    <!-- Hero -->
    <header class="bg-white py-5 border-bottom">
      <div class="container text-center">
        <h1 class="display-5 fw-bold text-earth-green">ESSOKO Mobile Apps</h1>
        <p class="lead text-muted mt-2">
          Designed for every role in the supply chain — farmers in the field,<br />
          godown operators at the warehouse, transporters on the road.
        </p>
        <div class="d-flex justify-content-center gap-3 mt-4">
          <a href="#" class="btn btn-dark">
            <i class="fab fa-apple me-2"></i>App Store
          </a>
          <a href="#" class="btn btn-success">
            <i class="fab fa-google-play me-2"></i>Google Play
          </a>
        </div>
      </div>
    </header>

    <div class="container py-5">

      <!-- App Cards -->
      <h2 class="display-6 fw-bold text-center mb-2">Three apps. One chain.</h2>
      <p class="text-center text-muted mb-5">Each app is purpose-built for its user.</p>

      <div class="row g-4 mb-5">

        <!-- Farmer App -->
        <div class="col-md-4">
          <div class="card h-100 border-0 shadow-sm rounded-3">
            <div class="card-body p-4">
              <div class="fs-1 mb-3">🌱</div>
              <h4 class="fw-bold">Farmer App</h4>
              <p class="text-muted small">For farmers delivering produce to godowns.</p>
              <hr />
              <ul class="list-unstyled small text-muted">
                <li class="mb-2"><i class="fas fa-check text-success me-2"></i>Record produce deliveries</li>
                <li class="mb-2"><i class="fas fa-check text-success me-2"></i>View payment history</li>
                <li class="mb-2"><i class="fas fa-check text-success me-2"></i>Track accepted / rejected deliveries</li>
                <li class="mb-2"><i class="fas fa-check text-success me-2"></i>See current market prices</li>
                <li class="mb-2"><i class="fas fa-check text-success me-2"></i>Works with low connectivity</li>
              </ul>
            </div>
            <div class="card-footer bg-white border-0 px-4 pb-4">
              <nuxt-link to="/auth/register" class="btn btn-success btn-sm w-100">
                Join as Farmer →
              </nuxt-link>
            </div>
          </div>
        </div>

        <!-- Godown App -->
        <div class="col-md-4">
          <div class="card h-100 border-0 shadow-sm rounded-3">
            <div class="card-body p-4">
              <div class="fs-1 mb-3">🏚️</div>
              <h4 class="fw-bold">Godown App</h4>
              <p class="text-muted small">For warehouse operators managing stock and orders.</p>
              <hr />
              <ul class="list-unstyled small text-muted">
                <li class="mb-2"><i class="fas fa-check text-success me-2"></i>Accept / reject farmer deliveries</li>
                <li class="mb-2"><i class="fas fa-check text-success me-2"></i>Manage stock listings</li>
                <li class="mb-2"><i class="fas fa-check text-success me-2"></i>Confirm incoming orders</li>
                <li class="mb-2"><i class="fas fa-check text-success me-2"></i>Mark orders ready for pickup</li>
                <li class="mb-2"><i class="fas fa-check text-success me-2"></i>Live stock dashboard</li>
              </ul>
            </div>
            <div class="card-footer bg-white border-0 px-4 pb-4">
              <nuxt-link to="/auth/register" class="btn btn-success btn-sm w-100">
                Join as Godown →
              </nuxt-link>
            </div>
          </div>
        </div>

        <!-- Transporter App -->
        <div class="col-md-4">
          <div class="card h-100 border-0 shadow-sm rounded-3">
            <div class="card-body p-4">
              <div class="fs-1 mb-3">🚚</div>
              <h4 class="fw-bold">Transporter App</h4>
              <p class="text-muted small">For transporters picking up and delivering orders.</p>
              <hr />
              <ul class="list-unstyled small text-muted">
                <li class="mb-2"><i class="fas fa-check text-success me-2"></i>Browse open delivery jobs</li>
                <li class="mb-2"><i class="fas fa-check text-success me-2"></i>Assign yourself to a job</li>
                <li class="mb-2"><i class="fas fa-check text-success me-2"></i>Confirm pickup from godown</li>
                <li class="mb-2"><i class="fas fa-check text-success me-2"></i>Confirm delivery to consumer</li>
                <li class="mb-2"><i class="fas fa-check text-success me-2"></i>Track your earnings</li>
              </ul>
            </div>
            <div class="card-footer bg-white border-0 px-4 pb-4">
              <nuxt-link to="/auth/register" class="btn btn-success btn-sm w-100">
                Join as Transporter →
              </nuxt-link>
            </div>
          </div>
        </div>
      </div>

      <!-- How it works on mobile -->
      <div class="card border-0 shadow-sm rounded-3 p-4 mb-5">
        <h4 class="fw-bold mb-4 text-center">How the mobile flow works</h4>
        <div class="row text-center g-3">
          <div class="col-6 col-md-3">
            <div class="fs-2 mb-2">🌱</div>
            <div class="fw-semibold small">Farmer delivers</div>
            <div class="text-muted" style="font-size:0.78rem">Records delivery in app</div>
          </div>
          <div class="col-6 col-md-3">
            <div class="fs-2 mb-2">🏚️</div>
            <div class="fw-semibold small">Godown accepts</div>
            <div class="text-muted" style="font-size:0.78rem">Accepts, grades, lists stock</div>
          </div>
          <div class="col-6 col-md-3">
            <div class="fs-2 mb-2">🛒</div>
            <div class="fw-semibold small">Consumer orders</div>
            <div class="text-muted" style="font-size:0.78rem">Orders online via website</div>
          </div>
          <div class="col-6 col-md-3">
            <div class="fs-2 mb-2">🚚</div>
            <div class="fw-semibold small">Transporter delivers</div>
            <div class="text-muted" style="font-size:0.78rem">Picks up & delivers</div>
          </div>
        </div>
      </div>

      <!-- CTA -->
      <div class="text-center py-3">
        <h4 class="fw-bold mb-2">Ready to join ESSOKO?</h4>
        <p class="text-muted mb-3">Create your account and start using the platform today.</p>
        <nuxt-link to="/auth/register" class="btn btn-success px-5">Get Started</nuxt-link>
      </div>

    </div>
  </div>
</template>

<script>
export default {
  name: 'MobileAppsPage',
  layout: 'master',
  auth: false,
}
</script>

<style scoped>
.text-earth-green { color: #2D6A4F; }
.btn-success { background-color: #2D6A4F; border-color: #2D6A4F; }
.btn-success:hover { background-color: #235840; border-color: #235840; }
</style>