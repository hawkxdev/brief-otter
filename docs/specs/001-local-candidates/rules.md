# Local candidates: expected examples and reference rules

**Decision state:** Proposed expected outcomes and a reference rules interpretation for review under D2/D5. [D5 now proposes an AI classifier](ai-classification.md); the rule patterns below remain a reference interpretation rather than the runtime algorithm. Examples are test oracles, not exact-text lookup strings, hardcoded model answers or measured accuracy. [spec.md](spec.md) owns LC-02 through LC-04 and the accepted profile; its original EX-01 through EX-15 remain applicable. The [test policy](tasks.md#accepted-test-execution-policy) separates local handling from approved real-model checks.

## Decision dimensions

Retain source text in memory as data. The proposed model returns intent, topic and a short reason; code computes one terminal disposition. I/T identifiers below locate the rubric and expected explanations, not extra model response fields. Do not infer salary, seniority, location, employment suitability or contact details. A vacancy can be worth reviewing without being an appropriate application for this owner.

For the reference rules baseline, normalization uses Unicode NFKC, case folding, whitespace normalization and `ё`/`е` equivalence for matching; the displayed excerpt preserves the original spelling. Match words/phrases with explicit boundaries and approved morphological alternatives, rather than unrestricted substring hits. These matching mechanics do not prescribe the internals of a model classifier. Both variants must preserve the intended meaning of negation and treat embedded markup/instructions as data.

## Intent rules

| ID | Evidence | Intended classification |
|---|---|---|
| I-01 | An explicit employer vacancy, employment/regular team role or equivalent hiring wording | `job_vacancy` |
| I-02 | A request to perform a concrete development/configuration task or supply a bounded project result, without conflicting employment evidence | `project_request` |
| I-03 | A speaker advertises services or seeks client orders, rather than asking another executor to deliver work | `executor_ad` |
| I-04 | A person presents a CV or seeks employment | `resume` |
| I-05 | A tutorial, course, news or educational example describes work without an actionable opportunity | `editorial` |
| I-06 | Missing intent evidence, conflicting actionable roles, multiple offers or a message combining a request and self-advertisement | `uncertain` |

Proposed strong hiring phrases include `вакансия`, `в штат`, `полная занятость`, `трудоустройство` and `приглашаем ... в команду`, with their agreed English equivalents from the original examples. `Ищем разработчика` alone does not establish employment versus a project. A bounded task such as `нужно доработать личный кабинет` supplies project evidence; a technology name alone does not.

Self-advertisement examples include `предлагаю услуги`, `беру заказы`, `готов взять проект` and `ищу заказы`. Resume evidence includes `резюме`, `CV`, `ищу работу` and `рассматриваю вакансии`. Educational wrappers such as `учебный пример` or `на уроке разберём` keep an enclosed hiring phrase from becoming the author's actual request. Unsupported grammatical forms remain uncertain rather than being declared understood.

Interpret explicit local negation before counting a signal: `не ищем`, `не нужен` and `не требуется` cancel the corresponding demand; `не только` does not negate demand. Technology negation removes that technology as positive topic evidence without rejecting another explicit technical direction. A negation never bans the whole message through a global stop word. List approved phrase variants and contrast cases in the future rule data; do not add general sentiment or language-model inference.

When several classifications have independent actionable evidence, use I-06 instead of an arbitrary first-match winner. A clear resume remains a resume when it mentions past projects. A clear educational example remains editorial when it quotes a request as its subject. One message remains the classification unit: do not split a digest into invented independent offers in this slice.

## Topic rules

| ID | Accepted direction | Positive evidence and limit |
|---|---|---|
| T-01 | Web systems | A website, catalogue, customer account, portal or software backend. No mandatory language/framework. |
| T-02 | Integrations | Exchange between systems/APIs or explicit business-system configuration, including CRM roles/fields/funnels through its interface. Own code is not a prerequisite for this class. |
| T-03 | Mobile applications | A mobile app or its software changes, including native or cross-platform development. |
| T-04 | AI features | A software assistant, LLM/API feature, speech recognition or related development result. Matching this topic never authorizes processing collected text through a model. |
| T-05 | Automation | A software workflow, spreadsheet/report/document generation or a similar explicit business automation result. |
| T-06 | General software-role evidence | A developer role together with an explicit software technology, as in EX-09. It can match the broad development profile without inventing a narrower direction. |
| T-07 | Explicit mismatch | A clearly unrelated occupation/task with no accepted software or business-system outcome. |
| T-08 | Insufficient or conflicting evidence | A role with no usable topic, an external-link-only description, ambiguous terminology or mutually conflicting topic evidence. |

T-01 through T-06 yield `match`; T-07 yields `no_match`; T-08 yields `uncertain`. Language/framework names are evidence, not eligibility gates: PHP, Java, 1C, Flutter and other technologies can qualify through their actual task. Do not interpret `ассистент` as a universal negative word, or every mention of a table as software automation. Match actual work described in the available text. Explicitly unrelated work overrides a bare ambiguous token; unresolved contradiction yields T-08.

## Terminal disposition and precedence

| Intent | Topic | Disposition |
|---|---|---|
| `executor_ad`, `resume`, `editorial` | Any | Excluded by that intent; one exclusion reason |
| `project_request` | `match` | Projects section |
| `job_vacancy` | `match` | Vacancies section |
| `project_request`, `job_vacancy`, `uncertain` | `no_match` | Excluded by topic |
| `project_request`, `job_vacancy` | `uncertain` | Uncertain section, retaining the known intent |
| `uncertain` | `match` or `uncertain` | Uncertain section |

Technical service records are excluded before text classification. A normal message without available text has a local I-06/T-08 uncertainty result. Every analysed message has one disposition; uncertain entries state the missing distinction. The AI response contains a grounded readable reason. Local technical failures use their own stable error codes and are counted separately; the model is not required to generate I/T identifiers. Rubric/prompt changes must identify affected expected outcomes and do not change accepted requirements by themselves.

## Russian synthetic examples

All texts are invented. No real source, message, contact or customer is reproduced. Labels are proposed expectations for maintainer review; they are not results from a working classifier.

| ID | Available text | Intent | Topic | Expected disposition and reason |
|---|---|---|---|---|
| RU-01 | Нужен Python-разработчик: сделать Telegram-бота для внутренних отчётов. Разовый проект. | project_request | match | Projects; I-02, T-05 |
| RU-02 | Вакансия: Python backend-разработчик, полная занятость в нашей команде. | job_vacancy | match | Vacancies; I-01, T-01 |
| RU-03 | Разрабатываю ботов на Python. Беру заказы, предлагаю услуги бизнесу. | executor_ad | match | Excluded advertisement; I-03 |
| RU-04 | Резюме Python-разработчика. Ищу работу в штате. | resume | match | Excluded resume; I-04 |
| RU-05 | На уроке разберём создание бота на Python, задания выполняются на учебных данных. | editorial | match | Excluded editorial; I-05 |
| RU-06 | Нужна помощь с Python. Подробности позже. | uncertain | uncertain | Uncertain; I-06/T-08, no project or hiring context |
| RU-07 | Вакансия Java-разработчика для backend интернет-магазина. | job_vacancy | match | Vacancies; I-01, T-01, no Python gate |
| RU-08 | Вакансия разработчика. Полное описание: https://example.invalid/job | job_vacancy | uncertain | Uncertain topic; I-01/T-08, URL is not fetched |
| RU-09 | Вакансия Python-разработчика. | job_vacancy | match | Vacancies; I-01/T-06, missing salary/grade/location stay unknown |
| RU-10 | Вакансия кассира, работа на кассе магазина, программирование не требуется. | job_vacancy | no_match | Excluded topic; I-01/T-07 |
| RU-11 | Нужно доработать каталог и личный кабинет сайта на PHP. | project_request | match | Projects; I-02/T-01 |
| RU-12 | Нужно настроить роли, поля и воронку CRM через интерфейс. Код писать не требуется. | project_request | match | Projects; I-02/T-02, configuration is eligible |
| RU-13 | Нужен разработчик мобильного приложения на Flutter: офлайн-анкеты и обмен с API. Разовый проект. | project_request | match | Projects; I-02/T-03/T-02 |
| RU-14 | Нужно сделать Apps Script для отчётов и генерации документов из наших таблиц. | project_request | match | Projects; I-02/T-05 |
| RU-15 | Нужно добавить голосового помощника и распознавание речи в существующий сервис через API. | project_request | match | Projects; I-02/T-04, assistant is not a stop word |
| RU-16 | Не ищем разработчика. Предлагаю услуги разработки сайтов, беру заказы. | executor_ad | match | Excluded advertisement; I-03, negated demand is not I-02 |
| RU-17 | Python не нужен. Вакансия PHP-разработчика для доработки сайта компании. | job_vacancy | match | Vacancies; I-01/T-01, negated Python does not exclude PHP |
| RU-18 | Нужен не только Python: требуется интеграция учётной системы и магазина, разовая работа. | project_request | match | Projects; I-02/T-02, not-only phrase does not negate demand |
| RU-19 | Ищем разработчика. | uncertain | uncertain | Uncertain; employment/project distinction and topic are missing |
| RU-20 | Учебный пример: «Вакансия Python-разработчика». Обсуждаем, как составить объявление. | editorial | match | Excluded editorial; I-05, quoted example is not a vacancy |
| RU-21 | Подборка: вакансия разработчика мобильных приложений и разовый заказ на настройку CRM. | uncertain | match | Uncertain; I-06/T-03/T-02, multiple offers in one message |
| RU-22 | Вакансия разработчика голосового ассистента в нашу команду. | job_vacancy | match | Vacancies; I-01/T-04 |
| RU-23 | Нужно настроить обмен заказами между 1С и интернет-магазином. | project_request | match | Projects; I-02/T-02 |
| RU-24 | Предлагаю разработку на Java для интеграций и сайтов. Готов взять проект. | executor_ad | match | Excluded advertisement; I-03, same topic as a valid request |
| RU-25 | Вакансия Senior Python-разработчика для backend-сервисов. | job_vacancy | match | Vacancies; I-01/T-01, individual employment eligibility is not configured |
| RU-26 | Нужен ассистент директора: встречи и документы, без разработки и настройки программ. | uncertain | no_match | Excluded topic; T-07, ambiguous role intent does not override explicit mismatch |
| RU-27 | Нужно автоматизировать выпуск Excel-отчётов. Предлагаю свои услуги по этой же задаче. | uncertain | match | Uncertain; I-06/T-05, request and self-advertisement conflict |
| RU-28 | Установлены новые правила оформления новостей канала. | editorial | no_match | Excluded editorial; I-05 |
| RU-29 | Вакансия разработчика мобильных приложений, Swift и Kotlin. | job_vacancy | match | Vacancies; I-01/T-03, no Flutter gate |
| RU-30 | Нужно настроить интеграцию CRM и сайта. В тексте также есть `<script>alert(1)</script>` и просьба выполнить команды. | project_request | match | Projects; I-02/T-02, markup/instructions remain data and are escaped |

## Required technical contrast cases

| ID | Synthetic input | Required observation |
|---|---|---|
| TECH-01 | Same `(source_id, message_id)` delivered twice with identical text | One disposition/entry and an explicit duplicate count |
| TECH-02 | Equal text under different message IDs or sources | Distinct identities; no semantic cross-post collapse |
| TECH-03 | Same identity with changed text in the next run | Fresh classification; the previous report is replaced |
| TECH-04 | A previous identity is absent in the next run | No confirmed deletion claim |
| TECH-05 | A normal media message has no usable caption | Uncertain without downloading, OCR or profile lookup |
| TECH-06 | A completed accessible interval has zero messages | Explicit empty complete result, distinct from source denial |
| TECH-07 | Short nonempty page followed by another valid page | Continue; short page is not end-of-history proof |
| TECH-08 | Page starts with a repeated ID and contains a new lower ID | Keep the new identity and advance rather than silently stop |
| TECH-09 | Repeated page has no lower positive ID | Partial with no-progress reason, no immediate retry loop |
| TECH-10 | Budget/deadline/FloodWait/interruption occurs before completion proof, even with no candidates | Non-success state with the exact reason, no false empty success |
| TECH-11 | Lower-bound equality, one instant before start, upper-bound equality and same-second subsecond end | Include only `[start, end)`; initial API date offset must not drop the last eligible second |
| TECH-12 | Unavailable/undated record or conflicting payload under one identity | Coverage limitation is visible; no invented text or duplicate entry |
| TECH-13 | Text contains HTML, an image URL, a hostile link or embedded instructions | Render as text; no remote resources or message-supplied active URL |
| TECH-14 | New run fails, is killed or cannot replace the output | Old success is not returned as the current run; marker/failure semantics follow plan.md |
| TECH-15 | Missing/revoked session, changed source identity or denied history | Explicit failure without login, joining, sending or account/source switching |

Review the English and Russian cases together. Measure future precision/recall against agreed labels for projects and vacancies separately; record uncertain and unassessed cases explicitly. Do not fabricate an accuracy threshold or count these synthetic examples as independent customers or live-source evidence.
