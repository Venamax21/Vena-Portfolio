// Load Vue from CDN in your contact.html
const { createApp, ref } = Vue;

createApp({
  setup() {
    // Add all your fields here
    const form = ref({
      first_name: "",
      last_name: "",
      phone_number: "",
      email: "",
      subject: "",
      message: ""
    });

    const success = ref(false);
    const error = ref(false);

    const submitForm = async () => {
  success.value = false
  error.value = false

  try {
    const response = await fetch('/sendmail/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form.value)
    })

    // Check for SendGrid's success code (202) or normal 200
    if (response.status === 200 || response.status === 202) {
      success.value = true
      form.value = { 
        first_name: '', 
        last_name: '', 
        phone_number: '', 
        email: '', 
        subject: '', 
        message: '' 
      }
    } else {
      error.value = true
      console.error("Server returned status:", response.status)
    }
  } catch (err) {
    console.error(err)
    error.value = true
  }
}

    return { form, success, error, submitForm };
  },

  
template: `
  <div class="contact-form max-w-lg mx-auto p-4 bg-white rounded-lg shadow-md">
    <h2 class="text-2xl font-semibold mb-4 text-center">Contact Me</h2>

    <form @submit.prevent="submitForm" class="space-y-3">
      <div class="flex space-x-2">
        <input v-model="form.first_name" type="text" placeholder="First Name" required 
               class="border rounded p-2 w-1/2 text-blue-900 placeholder-blue-400"/>
        <input v-model="form.last_name" type="text" placeholder="Last Name" required 
               class="border rounded p-2 w-1/2 text-blue-900 placeholder-blue-400"/>
      </div>

      <input v-model="form.phone_number" type="tel" placeholder="Phone Number" required 
             class="border rounded p-2 w-full text-blue-900 placeholder-blue-400"/>
      <input v-model="form.email" type="email" placeholder="Email" required 
             class="border rounded p-2 w-full text-blue-900 placeholder-blue-400"/>
      <input v-model="form.subject" type="text" placeholder="Subject" required 
             class="border rounded p-2 w-full text-blue-900 placeholder-blue-400"/>
      <textarea v-model="form.message" placeholder="Your Message" required 
                class="border rounded p-2 w-full h-32 text-blue-900 placeholder-blue-400"></textarea>

      <button type="submit" class="w-full bg-blue-600 text-black py-2 px-4 rounded hover:bg-blue-700 transition">
        Send Message
      </button>
    </form>

    <p v-if="success" class="text-green-600 mt-2 text-center">✅ Message sent successfully!</p>
    <p v-if="error" class="text-red-600 mt-2 text-center">❌ Something went wrong. Try again.</p>
  </div>
`

}).mount("#contact-form");
