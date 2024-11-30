# docker run -it -p 8000:8000 --name poetry-pyenv-container poetry-pyenv-app
#     exit
# docker login
# docker tag poetry-pyenv-app:0.1.0 uowon/qa-bot:0.1.0
# docker push uowon/qa-bot:0.1.0
# docker ps -a
# docker start poetry-pyenv-container
# docker exec -it poetry-pyenv-container /bin/bash

# poetry run uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload