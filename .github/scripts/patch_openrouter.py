from pathlib import Path
import re
p = Path("app/src/main/java/com/onepiece/world/MainActivity.kt")
s = p.read_text(encoding="utf-8")
def once(old, new, label):
    global s
    n = s.count(old)
    if n != 1: raise SystemExit(f"{label}: expected one match, got {n}")
    s = s.replace(old, new, 1)
default_models = (
    "cognitivecomputations/dolphin-mistral-24b-venice-edition:free\\n"
    "inclusionai/ling-3.2-flash:free\\n"
    "baidu/ernie-5.5-flash-preview:free\\n"
    "google/gemma-4-31b-it:free\\n"
    "recursive/flint-v1.0:free\\n"
    "nvidia/nemotron-3.5-lightning:free\\n"
    "openrouter/free"
)
once('    var model by remember { mutableStateOf(getValue("model", "gpt-6")) }',
     '    var modelChain by remember { mutableStateOf(getValue("model_chain", "' + default_models + '")) }',
     "model state")
pattern = re.compile(
    r'                                    val answer = withContext\(Dispatchers\.IO\) \{.*?'
    r'                                    \}\n'
    r'                                    lines\.add\(ChatLine\("assistant", answer\)\)',
    re.S
)
replacement = r'''                                    val answerResult = withContext(Dispatchers.IO) {
                                        val models = modelChain.lines().map { it.trim() }.filter { it.isNotBlank() }.distinct()
                                        if (models.isEmpty()) throw IllegalStateException("모델 목록을 한 개 이상 입력해 줘.")
                                        var lastError = "사용 가능한 모델이 없어."
                                        var completed: Pair<String, String>? = null
                                        for (modelId in models) {
                                            try {
                                                val messages = JSONArray().put(JSONObject().put("role", "user").put("content", prompt))
                                                val body = JSONObject().put("model", modelId).put("messages", messages).put("temperature", 0.8).put("max_tokens", 4096)
                                                val request = Request.Builder()
                                                    .url("https://openrouter.ai/api/v1/chat/completions")
                                                    .addHeader("Authorization", "Bearer $apiKey")
                                                    .addHeader("Content-Type", "application/json")
                                                    .addHeader("HTTP-Referer", "https://github.com/kmil4964-dot/one-piece-ai-world")
                                                    .addHeader("X-Title", "ONE PIECE AI WORLD")
                                                    .post(body.toString().toRequestBody("application/json".toMediaType()))
                                                    .build()
                                                client.newCall(request).execute().use { response ->
                                                    val raw = response.body?.string().orEmpty()
                                                    if (!response.isSuccessful) {
                                                        lastError = "모델 $modelId 오류 \${response.code}: $raw"
                                                        if (response.code == 401 || response.code == 402) throw IllegalStateException(lastError)
                                                    } else {
                                                        val json = JSONObject(raw)
                                                        val choices = json.optJSONArray("choices") ?: JSONArray()
                                                        val message = choices.optJSONObject(0)?.optJSONObject("message")
                                                            ?: throw IllegalStateException("모델 $modelId 응답에 message가 없어.")
                                                        val content = message.opt("content")
                                                        val text = when (content) {
                                                            is String -> content
                                                            is JSONArray -> (0 until content.length()).mapNotNull { i ->
                                                                content.optJSONObject(i)?.optString("text")?.takeIf { it.isNotBlank() }
                                                            }.joinToString("\n")
                                                            else -> ""
                                                        }
                                                        if (text.isBlank()) throw IllegalStateException("모델 $modelId 응답에 텍스트가 없어.")
                                                        completed = Pair(text, modelId)
                                                    }
                                                }
                                                if (completed != null) break
                                            } catch (e: Exception) {
                                                if (e.message?.contains("오류 401") == true || e.message?.contains("오류 402") == true) throw e
                                                lastError = e.message ?: "모델 $modelId 호출 실패"
                                            }
                                        }
                                        completed ?: throw IllegalStateException("모든 무료 모델 호출 실패. 마지막 오류: $lastError")
                                    }
                                    lines.add(ChatLine("assistant", answerResult.first))'''
s, n = pattern.subn(replacement, s, count=1)
if n != 1: raise SystemExit(f"API request block: expected one match, got {n}")
once('                                    status = "응답 완료"',
     '                                    status = "응답 완료 · \${answerResult.second}"',
     "success status")
old_ui = '''                    Text("OpenAI API 연결", style = MaterialTheme.typography.titleMedium)
                    OutlinedTextField(apiKey, { apiKey = it }, Modifier.fillMaxWidth(), label = { Text("API 키") }, singleLine = true)
                    OutlinedTextField(model, { model = it }, Modifier.fillMaxWidth(), label = { Text("API 모델 이름") }, singleLine = true)
                    Button(onClick = {
                        saveValue("api_key", apiKey.trim()); saveValue("model", model.trim())
                        status = "API 설정을 기기에 저장했어."
                    }) { Text("API 설정 저장") }
                    Text("API 키는 이 휴대폰 앱 내부에 저장돼. 개인 테스트용으로만 사용하고 다른 사람에게 APK를 배포하지 마. ChatGPT 구독과 API 사용료는 별도야.")
                    Text("모델 이름은 네 API 계정에서 사용 가능한 모델 ID로 입력해야 해. 기본값이 작동하지 않으면 API 플랫폼에서 사용 가능한 모델을 확인해 바꿔 줘.")
                    Text("API 키 발급: https://platform.openai.com/api-keys")'''
new_ui = '''                    Text("OpenRouter 무료 모델 연결", style = MaterialTheme.typography.titleMedium)
                    OutlinedTextField(apiKey, { apiKey = it }, Modifier.fillMaxWidth(), label = { Text("OpenRouter API 키") }, singleLine = true)
                    OutlinedTextField(modelChain, { modelChain = it }, Modifier.fillMaxWidth(), label = { Text("모델 우선순위 (한 줄에 모델 ID 하나)") }, minLines = 7)
                    Button(onClick = {
                        saveValue("api_key", apiKey.trim()); saveValue("model_chain", modelChain.trim())
                        status = "OpenRouter 설정을 기기에 저장했어."
                    }) { Text("API 설정 저장") }
                    Text("첫 모델부터 순서대로 요청하고, 429·모델 미지원·서버 오류가 나면 다음 모델을 자동으로 시도해. 모델 목록은 직접 수정할 수 있어.")
                    Text("무료 모델도 제공자별 호출 제한이 있어. 모델 목록이 바뀌면 최신 OpenRouter 목록으로 수정해 줘.")
                    Text("API 키 발급: https://openrouter.ai/keys")'''
once(old_ui, new_ui, "API settings UI")
s = s.replace("\\" + chr(36) + "{", chr(36) + "{")
p.write_text(s, encoding="utf-8")
print("OpenRouter patch applied")
