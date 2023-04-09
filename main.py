import os
from flask import jsonify, make_response
import firebase_admin
from firebase_admin import storage
from llama_index import (
    SimpleDirectoryReader,
    GPTListIndex,
    GPTSimpleVectorIndex,
    LLMPredictor,
    PromptHelper,
    ServiceContext,
)
from langchain import OpenAI

# Get the value of OPENAI_API_KEY from the environment
api_key = os.getenv("OPENAI_API_KEY")
# Use the API key in your code
os.environ["OPENAI_API_KEY"] = api_key

firebase_admin.initialize_app(options={"storageBucket": "simply-nice-app.appspot.com"})


def hello_world(request):
    # Set CORS headers for the preflight request
    if request.method == "OPTIONS":
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Max-Age": "3600",
        }
        return ("", 204, headers)

    # Set CORS headers for the main request
    headers = {"Access-Control-Allow-Origin": "*"}

    input_text = request.args.get("input_text", "")
    try:
        if input_text:
            response, sources = chatbot(input_text)
            return make_response(
                jsonify({"response": response, "sources": sources}), 200, headers
            )
        else:
            response = "Please provide an input text"
            sources = ""
            return make_response(
                jsonify({"response": response, "sources": sources}),
                400,
                headers,
            )
    except KeyError as e:
        print(f"KeyError encountered: {e} {input_text}")
        response = "An error occurred. Please try again later."
        sources = ""
    return make_response(
        jsonify({"response": response, "sources": sources}),
        500,  # Change this status code to 500 to indicate a server-side error
        headers,
    )


def chatbot(input_text):
    # Defining the parameters for the index
    max_input_size = 4096
    num_outputs = 1024
    max_chunk_overlap = 20

    prompt_helper = PromptHelper(
        max_input_size,
        num_outputs,
        max_chunk_overlap,
    )

    llm_predictor = LLMPredictor(
        llm=OpenAI(
            temperature=0.7, model_name="text-davinci-003", max_tokens=num_outputs
        )
    )

    service_context = ServiceContext.from_defaults(
        llm_predictor=llm_predictor, prompt_helper=prompt_helper
    )

    try:
        # Download the index.json file from Firebase Storage
        bucket = storage.bucket()
        blob = bucket.blob("index.json")
        index_json_data = blob.download_as_text()

        index = GPTSimpleVectorIndex.load_from_string(
            index_json_data, service_context=service_context
        )
        print("index.json has been loaded successfully.")
    except Exception as e:
        print("Error loading index.json:", e)
        return "An error occurred. Please try again later.", ""

    response = index.query(input_text, response_mode="default")
    return response.response, response.get_formatted_sources()
