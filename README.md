## Rails app + AI Python + Pyro 5

This is a demo Ruby on Rails 8 application showcasing a simple chat interface, designed for educational and experimental purposes.

### Features

- Ruby on Rails 8 setup
- Tailwind CSS for modern UI styling
- HTMX for dynamic, real-time form submission and chat updates
- Example Q&A pairs about Ruby programming (in Spanish and English) loaded via seeds
- Minimal, clean layout with responsive design
- PWA-ready structure (manifest included)

### Requirements

- Ruby 3.2 or newer
- Node.js (for asset building, if needed)
- SQLite3 (default database)
- Bundler

### Setup

1. **Clone the repository:**
   ```sh
   git clone <your-repo-url>
   cd rails8_app
   ```

2. **Install dependencies:**
   ```sh
    bundle install
   ```

3. **Set up the database:**
   ```sh
    bin/rails db:setup
    bin/rails db:seed
   ```

4. **Run the server:**
   ```sh
    bin/dev
   ```

5. Visit [http://localhost:3000](http://localhost:3000) in your browser.

### Development

- Main chat UI is in [`app/views/home/index.html.erb`](app/views/home/index.html.erb)
- Q&A pairs are seeded from [`db/seeds.rb`](db/seeds.rb)
- Styles are managed with Tailwind CSS ([`app/assets/tailwind/application.css`](app/assets/tailwind/application.css))
- JavaScript logic is in [`app/javascript/application.js`](app/javascript/application.js)

### Testing

To run the test suite:

```sh
bin/rails test
```

### Deployment

- The app is ready for deployment with Docker and Kamal.
- See [`Dockerfile`](Dockerfile) and Kamal configuration in `.kamal/`.

### License

This project is for demonstration and educational use.
