# Custom-Knowledge-Based Querying with ChatGPT

This project is a Python backend service that runs on Google Cloud Functions. It utilizes ChatGPT to provide custom knowledge-based querying by reading an `index.json` file from Firebase Storage and using it as a Llama index for generating responses.

## Features

-   Reads `index.json` file from Firebase Storage and uses it as a Llama index
-   Provides custom knowledge-based querying powered by ChatGPT
-   Accepts `input_text` as an API parameter and generates a relevant response along with the source of the information

## Installation & Deployment

This project is designed to be deployed as a Google Cloud Function. Follow the official [Google Cloud Functions documentation](https://cloud.google.com/functions/docs) to set up and deploy the function.

Deploy using script below in the command line:

`gcloud functions deploy hello_world --runtime python310 --trigger-http --allow-unauthenticated --entry-point hello_world --source . --set-env-vars OPENAI_API_KEY=YOUR_SECRET_KEY --memory 1024MB`

Change YOUR_SECRET_KEY to your own OpenAI secret key

### Prerequisites

-   A Google Cloud account with billing enabled
-   Firebase Storage configured with an `index.json` file
-   Google Cloud SDK installed on your local machine
-   OpenAI API key

### Setup

1. Clone this repository.
2. Install the required dependencies with `pip install -r requirements.txt`.
3. Set the `OPENAI_API_KEY` environment variable in your Google Cloud Function configuration.
4. Configure the `storageBucket` option in `firebase_admin.initialize_app()` to match your Firebase Storage bucket.
5. Deploy the function to Google Cloud Functions following their documentation.

## Usage

Make a GET request to the deployed Cloud Function with an `input_text` query parameter. The response will be a JSON object containing a generated response and the source of the information.

## http

GET https://&lt;your-cloud-function-url&gt;/hello_world?input_text=&lt;your-query-text&gt;

## Contributing

Fork the project.
Create a new branch (git checkout -b feature_branch).
Commit your changes (git commit -am 'Add a new feature').
Push to the branch (git push origin feature_branch).
Create a new Pull Request.

## License
This project is licensed under the MIT License.  
