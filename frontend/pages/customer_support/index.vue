<template>
  <div class="bg-light min-vh-100">

    <!-- Hero -->
    <header class="bg-white py-5 border-bottom">
      <div class="container text-center">
        <h1 class="display-5 fw-bold text-earth-green">Customer Support</h1>
        <p class="lead text-muted mt-2">We're here to help. Reach out any time.</p>
      </div>
    </header>

    <div class="container py-5">
      <div class="row g-4">

        <!-- Left: Contact Options -->
        <div class="col-md-5">

          <h4 class="fw-bold mb-4">Get in touch</h4>

          <div class="card border-0 shadow-sm rounded-3 mb-3">
            <div class="card-body d-flex align-items-center gap-3 p-3">
              <div class="fs-2">📞</div>
              <div>
                <div class="fw-semibold small">Phone / WhatsApp</div>
                <div class="text-muted small">+255 700 000 000</div>
                <div class="text-muted" style="font-size:0.75rem">Mon–Sat, 8am – 6pm</div>
              </div>
            </div>
          </div>

          <div class="card border-0 shadow-sm rounded-3 mb-3">
            <div class="card-body d-flex align-items-center gap-3 p-3">
              <div class="fs-2">✉️</div>
              <div>
                <div class="fw-semibold small">Email</div>
                <div class="text-muted small">support@essoko.co.tz</div>
                <div class="text-muted" style="font-size:0.75rem">We reply within 24 hours</div>
              </div>
            </div>
          </div>

          <div class="card border-0 shadow-sm rounded-3 mb-4">
            <div class="card-body d-flex align-items-center gap-3 p-3">
              <div class="fs-2">📍</div>
              <div>
                <div class="fw-semibold small">Office</div>
                <div class="text-muted small">Dar es Salaam, Tanzania</div>
                <div class="text-muted" style="font-size:0.75rem">By appointment</div>
              </div>
            </div>
          </div>

          <!-- FAQ quick links -->
          <h5 class="fw-bold mb-3">Common questions</h5>
          <div class="accordion accordion-flush" id="faqAccordion">

            <div class="accordion-item border rounded-3 mb-2">
              <h2 class="accordion-header">
                <button class="accordion-button collapsed rounded-3 small fw-semibold" type="button"
                  data-bs-toggle="collapse" data-bs-target="#faq1">
                  How do I place an order?
                </button>
              </h2>
              <div id="faq1" class="accordion-collapse collapse" data-bs-parent="#faqAccordion">
                <div class="accordion-body small text-muted">
                  Browse available produce on the <nuxt-link to="/listings" class="text-earth-green fw-semibold">Products page</nuxt-link>, click a product, enter your quantity, and confirm your order. You will need to create a consumer account first.
                </div>
              </div>
            </div>

            <div class="accordion-item border rounded-3 mb-2">
              <h2 class="accordion-header">
                <button class="accordion-button collapsed rounded-3 small fw-semibold" type="button"
                  data-bs-toggle="collapse" data-bs-target="#faq2">
                  How do I pick up my order?
                </button>
              </h2>
              <div id="faq2" class="accordion-collapse collapse" data-bs-parent="#faqAccordion">
                <div class="accordion-body small text-muted">
                  Once the godown confirms your order is ready, you can pick it up directly from the godown location shown on your order, or request a transporter to deliver it to you.
                </div>
              </div>
            </div>

            <div class="accordion-item border rounded-3 mb-2">
              <h2 class="accordion-header">
                <button class="accordion-button collapsed rounded-3 small fw-semibold" type="button"
                  data-bs-toggle="collapse" data-bs-target="#faq3">
                  I'm a farmer — how do I sell my produce?
                </button>
              </h2>
              <div id="faq3" class="accordion-collapse collapse" data-bs-parent="#faqAccordion">
                <div class="accordion-body small text-muted">
                  Register as a Farmer on ESSOKO, then deliver your produce to a registered godown near you. The godown will inspect, grade, and accept your produce. You'll receive payment based on the agreed price per kg.
                </div>
              </div>
            </div>

            <div class="accordion-item border rounded-3 mb-2">
              <h2 class="accordion-header">
                <button class="accordion-button collapsed rounded-3 small fw-semibold" type="button"
                  data-bs-toggle="collapse" data-bs-target="#faq4">
                  How do I cancel an order?
                </button>
              </h2>
              <div id="faq4" class="accordion-collapse collapse" data-bs-parent="#faqAccordion">
                <div class="accordion-body small text-muted">
                  You can cancel an order from your <nuxt-link to="/orders" class="text-earth-green fw-semibold">My Orders</nuxt-link> page as long as it is still in <strong>Pending</strong> status. Once confirmed by the godown, cancellation requires contacting support.
                </div>
              </div>
            </div>

          </div>
        </div>

        <!-- Right: Contact Form -->
        <div class="col-md-7">
          <div class="card border-0 shadow-sm rounded-3">
            <div class="card-body p-4">
              <h4 class="fw-bold mb-1">Send us a message</h4>
              <p class="text-muted small mb-4">Fill in the form and we'll get back to you within 24 hours.</p>

              <div v-if="sent" class="alert alert-success">
                ✅ Message sent! Our team will reply shortly.
              </div>

              <template v-if="!sent">
                <div class="row g-3 mb-3">
                  <div class="col-6">
                    <label class="form-label small fw-semibold">Your Name</label>
                    <input v-model="form.name" type="text" class="form-control" placeholder="John Doe" />
                  </div>
                  <div class="col-6">
                    <label class="form-label small fw-semibold">Phone / Email</label>
                    <input v-model="form.contact" type="text" class="form-control" placeholder="+255 xxx or email" />
                  </div>
                </div>

                <div class="mb-3">
                  <label class="form-label small fw-semibold">I am a…</label>
                  <select v-model="form.role" class="form-select">
                    <option value="">Select your role</option>
                    <option value="consumer">Consumer / Family</option>
                    <option value="farmer">Farmer</option>
                    <option value="godown">Godown Operator</option>
                    <option value="transporter">Transporter</option>
                    <option value="other">Other</option>
                  </select>
                </div>

                <div class="mb-3">
                  <label class="form-label small fw-semibold">Subject</label>
                  <select v-model="form.subject" class="form-select">
                    <option value="">Select a subject</option>
                    <option value="order">Order Issue</option>
                    <option value="payment">Payment Issue</option>
                    <option value="account">Account Help</option>
                    <option value="delivery">Delivery Issue</option>
                    <option value="other">Other</option>
                  </select>
                </div>

                <div class="mb-4">
                  <label class="form-label small fw-semibold">Message</label>
                  <textarea
                    v-model="form.message"
                    class="form-control"
                    rows="5"
                    placeholder="Describe your issue or question in detail…"
                  ></textarea>
                </div>

                <div v-if="formError" class="alert alert-danger py-2 small">{{ formError }}</div>

                <button class="btn btn-success w-100" :disabled="submitting" @click="submitForm">
                  <span v-if="submitting">
                    <span class="spinner-border spinner-border-sm me-2"></span>Sending…
                  </span>
                  <span v-else>Send Message</span>
                </button>
              </template>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CustomerSupportPage',
  layout: 'master',
  auth: false,

  data() {
    return {
      form: {
        name: '', contact: '', role: '', subject: '', message: '',
      },
      submitting: false,
      sent: false,
      formError: null,
    }
  },

  methods: {
    async submitForm() {
      this.formError = null
      if (!this.form.name || !this.form.contact || !this.form.message) {
        this.formError = 'Please fill in your name, contact, and message.'
        return
      }
      this.submitting = true
      // Simulate sending (replace with real API call if you have a support endpoint)
      await new Promise(r => setTimeout(r, 1200))
      this.sent = true
      this.submitting = false
    },
  },
}
</script>

<style scoped>
.text-earth-green { color: #2D6A4F; }
.btn-success { background-color: #2D6A4F; border-color: #2D6A4F; }
.btn-success:hover { background-color: #235840; border-color: #235840; }
.accordion-button:not(.collapsed) { color: #2D6A4F; background-color: #f0f7f2; }
.accordion-button:focus { box-shadow: none; }
</style>