from chatbot_app.response_modules.literature_responses import LiteratureResponses

def test_essay(topic):
    query = f"write an essay on {topic}"
    result = LiteratureResponses.generate_literature_response(query)
    print(result)

if __name__ == "__main__":
    test_essay("Climate Change")
    test_essay("Artificial Intelligence")
    test_essay("Gender")
