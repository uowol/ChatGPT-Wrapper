### QA-Bot-docker

#### TODO
- [x] 요구하는 파이썬 환경을 저장하는 docker 이미지 만들기
    - [x] pyenv를 활용한 파이썬 환경 생성
    - [x] docker 이미지 생성
- [x] (Prototype) slack bot 만들기
    - slack 봇 생성
    - slack 봇 워크스페이스 초대
    - slack 봇 채널 초대 `/invite @bot-name`
    - slack Event Subscription Enable해주고, Subscribe to bot events에 message.channels 추가
    - ngrok으로 퍼블릭 URL 만들어 slack에 입력하기
- [x] (Prototype) 셀레니움을 활용해 chatgpt.com 접속 및 채팅하기
- [ ] FastAPI 컨테이너 생성 및 실행을 지시하는 윈도우/리눅스 스크립트 작성

#### 배경
요즘 GPT가 일을 잘하긴 함. 어지간한건 PDF 형태로 그냥 넣어서 요약 및 정리할 수 있음.
취업 공고를 정리하는 작업도 생각해보면 주로 정리하는 양식에 맞춰서 정리하는 반복 작업임.
요즘 논문 읽을 때 PDF 던져두고 궁금한 Figure나 수식, 사용된 기술에 대한 세부 설명에 대해 물어보면 곧잘 답함.

#### 구상 중인 내용
Slack이나 디스코드 봇 형태로 제작
쓰레드가 존재하는 형태로, 논문이나 공고 채널에 자료를 던지면 일차적으로 정리해서 반환하고, 더 궁금하거나 이야기를 이어가고 싶다면 해당 스레드에서 진행할 수 있는 방향으로 구상 중.
GPT API는 거의 유료 서비스이므로, 결재해둔 GPT를 써먹기 위해 데탑에 서버를 띄워서 요청을 받아 처리하는 형식으로 갈까 함.
당장 떠오르는 건 FastAPI와 셀레니움? 더 좋은 방법은 없나?
이미지나 PDF는 어떻게 통신해야하지?
논문 요약 및 정리 서비스
취업 공고 요약 및 정리 서비스
