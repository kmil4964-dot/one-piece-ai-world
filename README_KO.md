# ONE PIECE AI WORLD — Android 시작 프로젝트

이 프로젝트는 렌을 주인공으로 하는 원피스 장기 RP/세계 시뮬레이터의 초기 버전입니다.

## 현재 포함 기능
- Android 앱 (Kotlin + Jetpack Compose)
- AU 이름, 시작 시점, 렌 프로필, 세계 현황 메모 저장
- 최근 대화 로컬 저장
- OpenAI Responses API 연결
- GitHub Actions를 이용한 APK 자동 빌드
- 렌의 대사/행동을 AI가 임의로 대신하지 않도록 하는 RP 지침
- 원작 고증 + 렌의 개입에 따른 역사 변화 + 독립적인 NPC/세력 운영 방향

## 중요한 제한
이것은 초기 MVP입니다. 아직 다음 기능은 구현되지 않았습니다.
- 여러 AU를 별도 프로필로 저장/전환하는 완성형 관리 화면
- 인물/세력/사건/관계/시간 데이터베이스
- 자동 사건 시뮬레이션 엔진
- 장기 기억 검색/요약/충돌 검증
- S/M/P/O 자동 장부 및 내보내기
- 백엔드 프록시를 통한 API 키 보호

현재 API 키는 개인 휴대폰의 앱 저장소에 저장됩니다. 개인 테스트용으로만 사용하고 APK를 타인에게 배포하지 마세요. 더 안전한 다중 사용자/배포 버전은 서버 백엔드가 필요합니다.

## 휴대폰만으로 APK 만들기
1. GitHub 계정을 만듭니다: https://github.com/signup
2. 새 Private 저장소를 만듭니다.
3. 이 ZIP의 **압축을 푼 모든 파일과 폴더**를 저장소에 업로드합니다. ZIP 파일 자체만 업로드하면 안 됩니다.
4. 저장소의 Actions 탭을 엽니다.
5. `Build Android APK` 워크플로를 선택하고 `Run workflow`를 누릅니다.
6. 실행이 성공하면 페이지 아래 Artifacts에서 `OnePieceAIWorld-debug-apk`를 다운로드합니다.
7. ZIP 압축을 풀고 `app-debug.apk`를 눌러 설치합니다.
8. 삼성 갤럭시에서 설치 권한을 요청하면 다운로드에 사용한 브라우저/파일 앱의 '알 수 없는 앱 설치'를 허용합니다.

## API 설정
1. https://platform.openai.com/api-keys 에서 API 키를 만듭니다.
2. 앱의 API 설정 탭에 키를 입력합니다.
3. API 모델 이름을 계정에서 사용할 수 있는 모델 ID로 설정합니다.
4. API 사용료는 ChatGPT 구독과 별도입니다.

## 프로젝트 파일 업로드 팁
GitHub 웹사이트에서 Add file → Upload files를 누르고, 압축을 푼 폴더 안의 파일들을 업로드합니다. `.github/workflows/android.yml` 경로가 정확히 유지되어야 자동 빌드가 실행됩니다.
