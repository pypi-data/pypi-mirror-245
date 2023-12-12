import bentoml

if __name__ == '__main__':
    # client = Client.from_url("https://kcai-bentoml-stage.onkakao.net/")
    # client.

    print(bentoml.models.list(tag="iris_clf"))