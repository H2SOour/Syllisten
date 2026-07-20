# Copyright (c) 2026 Siyuan Liu
# SPDX-License-Identifier: MIT

from __future__ import annotations

import asyncio
import difflib
import html
import json
import re
import unicodedata
from typing import Any

import streamlit as st
import streamlit.components.v1 as components
import edge_tts
from openai import OpenAI

APP_NAME = "Syllisten"
APP_VERSION = "4.3.3"
DEVELOPER = "Siyuan Liu"
PROJECT_LICENSE = "MIT License"

THEMES: dict[str, dict[str, str]] = {
    "Ocean": {"bg":"#F4F7FB","surface":"#FFFFFF","surface2":"#EAF1F8","text":"#172033","muted":"#5D6B82","primary":"#356A8A","primary2":"#244F69","border":"#D8E2EC","good":"#2F7D65","warn":"#9A6B22","bad":"#A34848","mark":"#DCEEDC","replace":"#F7E7B7","delete":"#F3D6D6"},
    "Sand": {"bg":"#F7F3EC","surface":"#FFFCF7","surface2":"#EFE6D8","text":"#2E2924","muted":"#756A60","primary":"#8A6244","primary2":"#66452F","border":"#DED2C3","good":"#4F7861","warn":"#9B6B22","bad":"#A24E45","mark":"#DDEBDD","replace":"#F3DFB4","delete":"#F0D6D0"},
    "Sage": {"bg":"#F1F5F1","surface":"#FBFDFB","surface2":"#E1EBE2","text":"#1F2C24","muted":"#647268","primary":"#557B63","primary2":"#395945","border":"#D1DED3","good":"#2E785C","warn":"#8B6B2B","bad":"#9B4D4D","mark":"#D8EBD8","replace":"#F0E1B8","delete":"#EFD4D4"},
    "Night": {"bg":"#11161D","surface":"#18212B","surface2":"#222E3A","text":"#EDF3F8","muted":"#AAB8C5","primary":"#78A9C4","primary2":"#9BC6DC","border":"#334353","good":"#72B79D","warn":"#D0A85B","bad":"#D88787","mark":"#234C42","replace":"#584A28","delete":"#5A3035"},
    "Color-safe": {"bg":"#F6F7F8","surface":"#FFFFFF","surface2":"#E8EEF2","text":"#1A1A1A","muted":"#60666B","primary":"#0072B2","primary2":"#005A8C","border":"#CFD8DE","good":"#0072B2","warn":"#E69F00","bad":"#CC79A7","mark":"#CDEAF6","replace":"#F7DFA7","delete":"#E9C5DA"},
}

DEFAULT_LOCALES = {"zh":"zh-CN","ja":"ja-JP","en":"en-GB","es":"es-ES","fr":"fr-FR"}
LANGUAGE_NAMES_EN = {"zh":"Chinese","ja":"Japanese","en":"English","es":"Spanish","fr":"French"}
SUPPORTED_CODES = set(DEFAULT_LOCALES)

I18N = {'en': {'ui_name': 'English',
        'title': 'Focused listening and dictation',
        'subtitle': 'Paste text, split it into listening units, play each sentence, and compare your dictation.',
        'theme': 'Theme',
        'ui_language': 'Interface language',
        'settings': 'Settings',
        'speed': 'Speech rate',
        'mode': 'Text analysis',
        'local_mode': 'Rule-based mode',
        'api_mode': 'Use my OpenAI API key',
        'local_help': 'No external AI request. Text is segmented with built-in rules on the app server.',
        'api_help': 'Your text is sent to OpenAI only with the API key you enter for this session. This app has no developer API key and cannot charge the developer’s OpenAI account.',
        'api_key': 'OpenAI API key',
        'api_placeholder': 'sk-…',
        'api_notice': 'The key is held only in this Streamlit session state. Do not enter a ChatGPT password.',
        'clear_key': 'Clear API key',
        'source_text': 'Study text',
        'source_placeholder': 'Paste text in Chinese, Japanese, English, Spanish or French…',
        'generate': 'Create exercise',
        'clear': 'Clear',
        'hidden': 'Text hidden. Listen first, then type what you heard.',
        'show': 'Show text',
        'unit': 'Listening unit',
        'answer': 'Your dictation',
        'answer_placeholder': 'Type what you heard…',
        'compare': 'Compare',
        'compare_note': 'Score ignores case, spacing and most punctuation.',
        'score': 'Match',
        'perfect': 'Essentially correct.',
        'close': 'Mostly correct; review the highlighted differences.',
        'retry': 'Clear differences remain. Listen again at a slower rate.',
        'difference': 'Difference',
        'standard': 'Show reference text',
        'language': 'Detected language',
        'locale': 'Speech locale',
        'units': 'Units',
        'method': 'Method',
        'gpt_method': 'OpenAI semantic segmentation',
        'rule_method': 'Rule-based segmentation',
        'empty': 'Paste text before creating an exercise.',
        'start': 'Paste text and select Create exercise.',
        'analysis_error': 'Text analysis failed',
        'play': 'Play',
        'stop': 'Stop',
        'voice_ready': 'A matching regional voice is preferred.',
        'voice_missing': 'No matching voice is installed. Add the language voice in your operating-system settings.',
        'menu': 'About & notices',
        'about': 'About',
        'version': 'Version',
        'developer': 'Developer',
        'license': 'Project license',
        'components': 'Third-party components',
        'privacy': 'Data handling',
        'legal': 'Legal notice',
        'ack': 'I have read and accept the notice',
        'continue': 'Continue',
        'notice_title': 'Use notice',
        'nonprofit': 'Non-commercial educational prototype',
        'nonprofit_body': 'This deployment is provided without charge for learning, demonstration and portfolio purposes. This statement does not represent registration as a '
                          'nonprofit organization and does not override applicable law or third-party terms.',
        'notice_body': 'Syllisten is an independent educational software prototype. It is not affiliated with, endorsed by, or an official product of OpenAI, Streamlit, Apple, '
                       'Microsoft, Google, any browser vendor, or any speech provider. Use the application only with text you are legally permitted to process. Do not submit '
                       'confidential, regulated, unlawful, infringing, or personal data unless you have a lawful basis and understand the relevant service terms. In rule-based '
                       'mode, text is processed by the application server and is not intentionally sent to OpenAI. In API mode, the submitted text is sent to OpenAI under the API '
                       'account associated with the key you provide. Speech is generated primarily through the third-party edge-tts package, an unofficial client for Microsoft Edge online speech synthesis. Sentences selected for reading may therefore be transmitted to Microsoft-operated online speech infrastructure. Browser Web Speech API speech is used only as a fallback, and its processing location depends on the browser, operating system and selected voice. The application does not guarantee accuracy, '
                       'availability, pronunciation, scoring, security, privacy, fitness for a particular purpose, or uninterrupted operation. Outputs and scores are educational '
                       'aids and must not be relied on for legal, medical, financial, academic certification, immigration, employment or other high-stakes decisions. You are '
                       'responsible for API charges, content rights, device and browser configuration, and compliance with all applicable laws and third-party terms. API keys are '
                       'intended to remain in the current session only, but no internet service can promise absolute security. Use a restricted project key, set spending limits, '
                       'and revoke the key after use when appropriate. The software is provided “as is” without warranties, to the maximum extent permitted by law.',
        'must_accept': 'Please accept the notice to continue.',
        'footer': 'Independent educational prototype. Use only content you are authorized to process.',
        'key_missing': 'Enter an OpenAI API key or switch to rule-based mode.',
        'not_saved': 'Not written to the repository or application database by this app.',
        'delete_session': 'Closing the session normally clears session state; use Clear API key before leaving a shared device.',
        'module_openai': 'OpenAI Python SDK — API requests in user-key mode; Apache-2.0 license.',
        'module_streamlit': 'Streamlit — web interface and session handling; Apache-2.0 license.',
        'module_webspeech': 'edge-tts — unofficial client for Microsoft Edge online speech synthesis; availability and service behavior may change. Web Speech API is used only as a fallback.',
        'module_python': 'Python standard library — text processing and comparison.',
        'source_note': 'Publishing source code is optional for this architecture, but the repository includes license and third-party notices for transparency.',
        'no_key_log': 'The app is designed not to print or intentionally persist the full API key. Hosting-platform logs and infrastructure remain subject to the operator’s '
                      'configuration.',
        'analysis_mode': 'Analysis mode',
        'supported_only': 'Only Chinese, Japanese, English, Spanish and French are supported.',
        'unsupported_language': 'This text appears to be in an unsupported language. Syllisten currently supports Chinese, Japanese, English, Spanish and French only.',
        'notice_language': 'Notice language',
        'supported_languages': 'Supported study languages',
        'supported_list': 'Chinese · Japanese · English · Spanish · French'},
 'zh': {'ui_name': '简体中文',
        'title': '多语言精听与听写',
        'subtitle': '粘贴文本，生成逐句精听单元，完成听写并查看差异。',
        'theme': '主题',
        'ui_language': '界面语言',
        'settings': '设置',
        'speed': '朗读速度',
        'mode': '文本分析方式',
        'local_mode': '规则模式',
        'api_mode': '使用我的 OpenAI API Key',
        'local_help': '不调用外部 AI。文本由应用服务器使用内置规则断句。',
        'api_help': '仅使用你在本次会话中输入的 API Key 将文本发送至 OpenAI。本应用不配置开发者 API Key，不会产生开发者账户费用。',
        'api_key': 'OpenAI API Key',
        'api_placeholder': 'sk-…',
        'api_notice': 'Key 仅保存在当前 Streamlit 会话状态中。请勿输入 ChatGPT 密码。',
        'clear_key': '清除 API Key',
        'source_text': '学习文本',
        'source_placeholder': '粘贴中文、日语、英语、西班牙语或法语文本……',
        'generate': '生成练习',
        'clear': '清空',
        'hidden': '原文已隐藏。请先播放，再输入听到的内容。',
        'show': '显示原文',
        'unit': '精听单元',
        'answer': '你的听写',
        'answer_placeholder': '输入你听到的句子……',
        'compare': '确认比对',
        'compare_note': '评分忽略大小写、空格和大部分标点。',
        'score': '匹配度',
        'perfect': '基本完全正确。',
        'close': '整体正确，请查看高亮差异。',
        'retry': '仍有明显差异，建议降低速度后重听。',
        'difference': '差异',
        'standard': '查看标准答案',
        'language': '识别语言',
        'locale': '朗读地区',
        'units': '听写单元',
        'method': '处理方式',
        'gpt_method': 'OpenAI 语义断句',
        'rule_method': '规则断句',
        'empty': '请先粘贴文本。',
        'start': '粘贴文本后点击“生成练习”。',
        'analysis_error': '文本分析失败',
        'play': '播放',
        'stop': '停止',
        'voice_ready': '优先选择与文本地区匹配的语音。',
        'voice_missing': '未检测到匹配语音，请在系统设置中安装该语言语音。',
        'menu': '关于与声明',
        'about': '关于',
        'version': '版本',
        'developer': '开发者',
        'license': '项目许可证',
        'components': '第三方模块',
        'privacy': '数据处理',
        'legal': '法律与使用声明',
        'ack': '我已阅读并接受上述说明',
        'continue': '继续使用',
        'notice_title': '使用须知',
        'nonprofit': '非商业教育原型声明',
        'nonprofit_body': '本部署免费提供，仅用于学习、演示和个人作品展示。本声明不表示本项目已登记为非营利组织，也不能排除适用法律或第三方条款。',
        'notice_body': 'Syllisten 是独立开发的教育软件原型，并非 '
                       'OpenAI、Streamlit、Apple、Microsoft、Google、任何浏览器厂商或语音服务提供方的官方产品，也未获得其背书。使用者仅可提交其依法有权处理的文本；在未具备合法依据并充分理解相关服务条款的情况下，不得提交机密信息、受监管信息、违法内容、侵权内容或个人数据。规则模式下，文本由本应用服务器处理，应用不会主动将文本发送至 '
                       'OpenAI。API 模式下，所提交文本将使用使用者提供的 API Key 发送至 OpenAI，并受该 API 账户及 OpenAI 适用条款约束。朗读主要通过第三方 edge-tts 软件包生成。该软件包是 Microsoft Edge 在线语音合成服务的非官方客户端，因此用于朗读的句子可能会传输至 Microsoft 运营的在线语音基础设施。浏览器 Web Speech API 仅作为备用方案，其处理位置取决于浏览器、操作系统及所选语音。本应用不保证识别、断句、发音、评分、可用性、安全性、隐私性、特定用途适用性或持续无故障运行。所有结果和评分仅供学习参考，不得用于法律、医疗、金融、学历认证、移民、就业或其他高风险决策。使用者自行承担 API '
                       '费用、内容权利审查、设备与浏览器配置，以及遵守适用法律和第三方条款的责任。API Key 设计为仅在当前会话中使用，但任何联网服务均无法承诺绝对安全；建议使用受限项目 Key、设置消费上限，并在必要时于使用后撤销。软件在法律允许的最大范围内按“现状”提供，不附带任何明示或默示保证。',
        'must_accept': '请先阅读并接受使用须知。',
        'footer': '独立教育软件原型。请仅处理你有权使用的内容。',
        'key_missing': '请输入 OpenAI API Key，或切换到规则模式。',
        'not_saved': '本应用不会主动将 Key 写入代码仓库或应用数据库。',
        'delete_session': '关闭会话通常会清除会话状态；在共享设备上离开前请主动点击“清除 API Key”。',
        'module_openai': 'OpenAI Python SDK——用户 Key 模式下发送 API 请求；Apache-2.0 许可证。',
        'module_streamlit': 'Streamlit——Web 界面与会话管理；Apache-2.0 许可证。',
        'module_webspeech': 'edge-tts——用于访问 Microsoft Edge 在线语音合成服务的非官方客户端；服务可用性与行为可能发生变化。Web Speech API 仅作为备用。',
        'module_python': 'Python 标准库——文本处理与差异比对。',
        'source_note': '本架构并不因免责而必须公开源代码；本项目仍提供许可证与第三方声明，以提高透明度。',
        'no_key_log': '程序设计上不会打印或主动持久化完整 API Key；托管平台日志与基础设施仍取决于部署者配置。',
        'analysis_mode': '分析模式',
        'supported_only': '目前仅支持中文、日语、英语、西班牙语和法语。',
        'unsupported_language': '检测到的文本语言不在支持范围内。Syllisten 目前仅支持中文、日语、英语、西班牙语和法语。',
        'notice_language': '须知语言',
        'supported_languages': '支持的学习语言',
        'supported_list': '中文 · 日语 · 英语 · 西班牙语 · 法语'},
 'ja': {'ui_name': '日本語',
        'title': '多言語リスニング・ディクテーション',
        'subtitle': 'テキストを貼り付け、文ごとに再生し、書き取りを比較します。',
        'theme': 'テーマ',
        'ui_language': '表示言語',
        'settings': '設定',
        'speed': '再生速度',
        'mode': 'テキスト解析',
        'local_mode': 'ルールベース',
        'api_mode': '自分の OpenAI API Key を使用',
        'local_help': '外部 AI を使用せず、アプリサーバー上のルールで分割します。',
        'api_help': '入力した API Key を使い、テキストを OpenAI に送信します。',
        'api_key': 'OpenAI API Key',
        'api_placeholder': 'sk-…',
        'api_notice': 'Key は現在のセッションでのみ使用します。ChatGPT のパスワードは入力しないでください。',
        'clear_key': 'API Key を削除',
        'source_text': '学習テキスト',
        'source_placeholder': '中国語、日本語、英語、スペイン語、フランス語のテキストを貼り付け…',
        'generate': '練習を作成',
        'clear': 'クリア',
        'hidden': '原文は非表示です。再生後、聞こえた文を入力してください。',
        'show': '原文を表示',
        'unit': 'リスニング単位',
        'answer': '書き取り',
        'answer_placeholder': '聞こえた文を入力…',
        'compare': '比較',
        'compare_note': '大文字小文字、空白、多くの句読点を除いて採点します。',
        'score': '一致率',
        'perfect': 'ほぼ正解です。',
        'close': '概ね正解です。差分を確認してください。',
        'retry': '差分があります。速度を下げて再度聞いてください。',
        'difference': '差分',
        'standard': '正解を見る',
        'language': '検出言語',
        'locale': '音声ロケール',
        'units': '単位数',
        'method': '処理方法',
        'gpt_method': 'OpenAI による意味分割',
        'rule_method': 'ルール分割',
        'empty': '先にテキストを入力してください。',
        'start': 'テキストを貼り付けて「練習を作成」を押してください。',
        'analysis_error': '解析に失敗しました',
        'play': '再生',
        'stop': '停止',
        'voice_ready': '地域に合う音声を優先します。',
        'voice_missing': '対応音声がありません。OS 設定で追加してください。',
        'menu': '情報と通知',
        'about': '概要',
        'version': 'バージョン',
        'developer': '開発者',
        'license': 'ライセンス',
        'components': '外部コンポーネント',
        'privacy': 'データ処理',
        'legal': '利用上の注意',
        'ack': '上記を読み、同意します',
        'continue': '続行',
        'notice_title': '利用上の注意',
        'nonprofit': '非営利・教育目的での提供に関する声明',
        'nonprofit_body': '本アプリケーションは、学習、技術的実証およびポートフォリオ提示を目的として、無償かつ非営利で提供されます。この記載は、運営者または本プロジェクトが法的に非営利法人として登録されていることを意味せず、適用法令、第三者の利用規約またはライセンス上の義務を免除するものではありません。',
        'notice_body': 'Syllisten '
                       'は独立して開発された教育用ソフトウェアの試作版です。OpenAI、Streamlit、Apple、Microsoft、Google、ブラウザ提供者、音声提供者その他の第三者と提携し、承認を受け、またはそれらの公式製品として提供されるものではありません。利用者は、自らが適法に処理する権限を有するテキストのみを入力してください。適法な根拠がなく、関連する規約およびリスクを十分に理解していない場合、秘密情報、規制対象情報、違法または権利侵害となる内容、個人情報もしくはセンシティブ情報を入力しないでください。ルールベースモードでは、入力テキストは本アプリケーションのサーバー上で内蔵ルールにより処理され、OpenAI '
                       'へ意図的に送信されません。API モードでは、利用者が提供した API Key に紐づくアカウントを使用して入力テキストが OpenAI に送信され、当該アカウントおよび OpenAI の適用規約に従って処理されます。音声は主として、Microsoft Edge のオンライン音声合成を利用する非公式クライアントである第三者製パッケージ edge-tts により生成されます。そのため、読み上げ対象の文が Microsoft の運営するオンライン音声基盤へ送信される場合があります。ブラウザの Web Speech API は予備手段としてのみ使用され、処理場所はブラウザ、オペレーティングシステムおよび選択音声に依存します。本アプリケーションは、言語判定、文分割、発音、採点、翻訳的解釈、可用性、継続性、安全性、プライバシー、特定目的への適合性またはエラーの不存在を保証しません。結果および採点は学習補助のみを目的とし、法律、医療、金融、学位・資格認定、入国管理、採用その他の重大な判断に使用してはなりません。API '
                       '利用料金、入力内容に関する権利確認、端末およびブラウザの設定、ならびに適用法令、第三者の規約およびライセンスの遵守は利用者の責任です。API Key '
                       'は現在のセッション内でのみ使用するよう設計されていますが、インターネット上のサービスについて絶対的な安全性を保証することはできません。利用範囲を制限したプロジェクト Key '
                       'を使用し、利用上限を設定し、必要に応じて使用後に失効させてください。本ソフトウェアは、適用法令で認められる最大限の範囲において、明示または黙示の保証なく「現状有姿」で提供されます。',
        'must_accept': '利用上の注意に同意してください。',
        'footer': '独立した教育用プロトタイプです。権利を有するコンテンツのみ使用してください。',
        'key_missing': 'API Key を入力するか、ルールベースに切り替えてください。',
        'not_saved': 'Key はリポジトリやアプリのデータベースに保存しません。',
        'delete_session': '共有端末では終了前に Key を削除してください。',
        'module_openai': 'OpenAI Python SDK — API リクエスト。Apache-2.0。',
        'module_streamlit': 'Streamlit — UI とセッション管理。Apache-2.0。',
        'module_webspeech': 'edge-tts — Microsoft Edge のオンライン音声合成を利用する非公式クライアントです。利用可能性や挙動は変更される場合があります。Web Speech API は予備機能としてのみ使用します。',
        'module_python': 'Python 標準ライブラリ — テキスト処理。',
        'source_note': '免責のためにソース公開が必須ではありませんが、透明性のため通知を含めています。',
        'no_key_log': '完全な Key を意図的に記録しない設計です。',
        'analysis_mode': '解析モード',
        'supported_only': '現在対応している言語は、中国語、日本語、英語、スペイン語、フランス語のみです。',
        'unsupported_language': '対応していない言語のテキストが検出されました。Syllisten は現在、中国語、日本語、英語、スペイン語、フランス語のみに対応しています。',
        'notice_language': '表示言語',
        'supported_languages': '対応学習言語',
        'supported_list': '中国語・日本語・英語・スペイン語・フランス語'},
 'es': {'ui_name': 'Español',
        'title': 'Escucha intensiva y dictado',
        'subtitle': 'Pega un texto, divídelo en unidades, escucha cada frase y compara tu dictado.',
        'theme': 'Tema',
        'ui_language': 'Idioma de la interfaz',
        'settings': 'Ajustes',
        'speed': 'Velocidad de lectura',
        'mode': 'Análisis del texto',
        'local_mode': 'Modo basado en reglas',
        'api_mode': 'Usar mi clave de API de OpenAI',
        'local_help': 'No se realiza ninguna solicitud a una IA externa. El texto se segmenta mediante reglas integradas en el servidor de la aplicación.',
        'api_help': 'El texto se envía a OpenAI utilizando la clave de API introducida para esta sesión.',
        'api_key': 'Clave de API de OpenAI',
        'api_placeholder': 'sk-…',
        'api_notice': 'La clave se mantiene únicamente en el estado de esta sesión de Streamlit. No introduzcas tu contraseña de ChatGPT.',
        'clear_key': 'Borrar clave de API',
        'source_text': 'Texto de estudio',
        'source_placeholder': 'Pega un texto en chino, japonés, inglés, español o francés…',
        'generate': 'Crear ejercicio',
        'clear': 'Borrar',
        'hidden': 'El texto está oculto. Escucha primero y escribe después lo que hayas oído.',
        'show': 'Mostrar texto',
        'unit': 'Unidad de escucha',
        'answer': 'Tu dictado',
        'answer_placeholder': 'Escribe lo que has oído…',
        'compare': 'Comparar',
        'compare_note': 'La puntuación ignora mayúsculas, espacios y la mayoría de los signos de puntuación.',
        'score': 'Coincidencia',
        'perfect': 'Prácticamente correcto.',
        'close': 'En general correcto; revisa las diferencias resaltadas.',
        'retry': 'Persisten diferencias claras. Vuelve a escuchar a menor velocidad.',
        'difference': 'Diferencias',
        'standard': 'Mostrar texto de referencia',
        'language': 'Idioma detectado',
        'locale': 'Configuración regional de voz',
        'units': 'Unidades',
        'method': 'Método',
        'gpt_method': 'Segmentación semántica mediante OpenAI',
        'rule_method': 'Segmentación basada en reglas',
        'empty': 'Pega un texto antes de crear el ejercicio.',
        'start': 'Pega un texto y selecciona «Crear ejercicio».',
        'analysis_error': 'No se pudo analizar el texto',
        'play': 'Reproducir',
        'stop': 'Detener',
        'voice_ready': 'Se dará prioridad a una voz de la región correspondiente.',
        'voice_missing': 'No hay instalada una voz compatible. Añádela en los ajustes del sistema operativo.',
        'menu': 'Información y avisos',
        'about': 'Acerca de',
        'version': 'Versión',
        'developer': 'Desarrollador',
        'license': 'Licencia del proyecto',
        'components': 'Componentes de terceros',
        'privacy': 'Tratamiento de datos',
        'legal': 'Aviso legal',
        'ack': 'He leído y acepto este aviso',
        'continue': 'Continuar',
        'notice_title': 'Condiciones de uso',
        'nonprofit': 'Declaración de uso educativo y no lucrativo',
        'nonprofit_body': 'Esta aplicación se ofrece gratuitamente y sin ánimo de lucro con fines educativos, de demostración técnica y de presentación de portafolio. Esta '
                          'declaración no implica que el proyecto o su responsable estén constituidos legalmente como entidad sin ánimo de lucro, ni exime del cumplimiento de la '
                          'legislación aplicable, las licencias o las condiciones de terceros.',
        'notice_body': 'Syllisten es un prototipo de software educativo desarrollado de forma independiente. No está afiliado, patrocinado, aprobado ni presentado como '
                       'producto oficial de OpenAI, Streamlit, Apple, Microsoft, Google, proveedores de navegadores, proveedores de voz ni otros terceros. Utiliza únicamente '
                       'textos que tengas derecho legal a procesar. No introduzcas información confidencial, regulada, ilícita, infractora, personal o sensible salvo que '
                       'dispongas de una base jurídica válida y comprendas plenamente las condiciones y los riesgos correspondientes. En el modo basado en reglas, el texto se '
                       'procesa mediante reglas integradas en el servidor de la aplicación y no se envía deliberadamente a OpenAI. En el modo API, el texto se envía a OpenAI '
                       'mediante la clave de API proporcionada por el usuario y queda sujeto a la cuenta asociada y a las condiciones aplicables de OpenAI. La voz se genera principalmente mediante el paquete de terceros edge-tts, un cliente no oficial del servicio de síntesis de voz en línea de Microsoft Edge. Por ello, las frases destinadas a la lectura pueden transmitirse a infraestructura de voz en línea operada por Microsoft. La Web Speech API del navegador se utiliza únicamente como alternativa, y el lugar de procesamiento depende del navegador, del sistema operativo y de la voz seleccionada. La aplicación no garantiza la exactitud de la detección de idioma, la segmentación, la '
                       'pronunciación o la puntuación, ni la disponibilidad, continuidad, seguridad, privacidad, idoneidad para un fin concreto o ausencia de errores. Los '
                       'resultados y las puntuaciones son únicamente ayudas educativas y no deben utilizarse para decisiones jurídicas, médicas, financieras, de certificación '
                       'académica, migratorias, laborales ni otras decisiones de alto riesgo. El usuario es responsable de los cargos de la API, de verificar los derechos sobre '
                       'el contenido, de la configuración del dispositivo y del navegador, y del cumplimiento de la legislación, las licencias y las condiciones de terceros '
                       'aplicables. La clave de API está diseñada para permanecer únicamente durante la sesión actual; no obstante, ningún servicio conectado a Internet puede '
                       'garantizar una seguridad absoluta. Utiliza una clave de proyecto restringida, establece límites de gasto y revócala después de su uso cuando proceda. El '
                       'software se proporciona «tal cual», sin garantías expresas ni implícitas, en la máxima medida permitida por la ley.',
        'must_accept': 'Debes aceptar el aviso para continuar.',
        'footer': 'Prototipo educativo independiente. Utiliza únicamente contenido que estés autorizado a procesar.',
        'key_missing': 'Introduce una clave de API de OpenAI o cambia al modo basado en reglas.',
        'not_saved': 'La aplicación no guarda deliberadamente la clave en el repositorio ni en una base de datos.',
        'delete_session': 'Al cerrar la sesión normalmente se elimina su estado; en un dispositivo compartido, pulsa «Borrar clave de API» antes de salir.',
        'module_openai': 'SDK de Python de OpenAI — solicitudes API en el modo de clave del usuario; licencia Apache-2.0.',
        'module_streamlit': 'Streamlit — interfaz web y gestión de sesiones; licencia Apache-2.0.',
        'module_webspeech': 'edge-tts — cliente no oficial para la síntesis de voz en línea de Microsoft Edge; su disponibilidad y funcionamiento pueden cambiar. Web Speech API se utiliza solo como alternativa.',
        'module_python': 'Biblioteca estándar de Python — procesamiento de texto y comparación.',
        'source_note': 'La publicación del código fuente no es obligatoria para limitar la responsabilidad en esta arquitectura; el repositorio incluye licencias y avisos de '
                       'terceros por transparencia.',
        'no_key_log': 'La aplicación está diseñada para no imprimir ni conservar deliberadamente la clave completa. Los registros de la plataforma y la infraestructura dependen '
                      'de la configuración del operador.',
        'analysis_mode': 'Modo de análisis',
        'supported_only': 'Solo se admiten chino, japonés, inglés, español y francés.',
        'unsupported_language': 'El texto parece estar en un idioma no compatible. Syllisten solo admite actualmente chino, japonés, inglés, español y francés.',
        'notice_language': 'Idioma del aviso',
        'supported_languages': 'Idiomas de estudio compatibles',
        'supported_list': 'Chino · Japonés · Inglés · Español · Francés'},
 'fr': {'ui_name': 'Français',
        'title': 'Écoute intensive et dictée',
        'subtitle': 'Collez un texte, divisez-le en unités d’écoute, écoutez chaque phrase et comparez votre dictée.',
        'theme': 'Thème',
        'ui_language': 'Langue de l’interface',
        'settings': 'Paramètres',
        'speed': 'Vitesse de lecture',
        'mode': 'Analyse du texte',
        'local_mode': 'Mode fondé sur des règles',
        'api_mode': 'Utiliser ma clé API OpenAI',
        'local_help': 'Aucune requête n’est adressée à une IA externe. Le texte est segmenté au moyen de règles intégrées sur le serveur de l’application.',
        'api_help': 'Votre texte est envoyé à OpenAI uniquement au moyen de la clé API que vous saisissez pendant cette session. L’application ne contient aucune clé API du développeur et ne peut entraîner de frais sur son compte.',
        'api_key': 'Clé API OpenAI',
        'api_placeholder': 'sk-…',
        'api_notice': 'La clé est conservée uniquement dans l’état de cette session Streamlit. Ne saisissez pas votre mot de passe ChatGPT.',
        'clear_key': 'Effacer la clé API',
        'source_text': 'Texte d’étude',
        'source_placeholder': 'Collez un texte en chinois, japonais, anglais, espagnol ou français…',
        'generate': 'Créer l’exercice',
        'clear': 'Effacer',
        'hidden': 'Le texte est masqué. Écoutez d’abord, puis saisissez ce que vous avez entendu.',
        'show': 'Afficher le texte',
        'unit': 'Unité d’écoute',
        'answer': 'Votre dictée',
        'answer_placeholder': 'Saisissez ce que vous avez entendu…',
        'compare': 'Comparer',
        'compare_note': 'Le score ne tient pas compte des majuscules, des espaces ni de la plupart des signes de ponctuation.',
        'score': 'Correspondance',
        'perfect': 'Réponse pratiquement exacte.',
        'close': 'Réponse globalement correcte ; examinez les différences surlignées.',
        'retry': 'Des différences importantes subsistent. Réécoutez à une vitesse plus lente.',
        'difference': 'Différences',
        'standard': 'Afficher le texte de référence',
        'language': 'Langue détectée',
        'locale': 'Paramètre régional de la voix',
        'units': 'Unités',
        'method': 'Méthode',
        'gpt_method': 'Segmentation sémantique par OpenAI',
        'rule_method': 'Segmentation fondée sur des règles',
        'empty': 'Collez un texte avant de créer l’exercice.',
        'start': 'Collez un texte, puis sélectionnez « Créer l’exercice ».',
        'analysis_error': 'Échec de l’analyse du texte',
        'play': 'Lire',
        'stop': 'Arrêter',
        'voice_ready': 'Une voix correspondant à la région sera privilégiée.',
        'voice_missing': 'Aucune voix compatible n’est installée. Ajoutez-la dans les réglages du système d’exploitation.',
        'menu': 'À propos et mentions',
        'about': 'À propos',
        'version': 'Version',
        'developer': 'Développeur',
        'license': 'Licence du projet',
        'components': 'Composants tiers',
        'privacy': 'Traitement des données',
        'legal': 'Mentions légales',
        'ack': 'J’ai lu et j’accepte le présent avis',
        'continue': 'Continuer',
        'notice_title': 'Conditions d’utilisation',
        'nonprofit': 'Déclaration d’usage éducatif et non lucratif',
        'nonprofit_body': 'Cette application est mise à disposition gratuitement et sans but lucratif à des fins d’apprentissage, de démonstration technique et de présentation de '
                          'portfolio. Cette déclaration ne signifie pas que le projet ou son responsable est juridiquement constitué en organisme à but non lucratif et ne '
                          'dispense pas du respect des lois, licences ou conditions de tiers applicables.',
        'notice_body': 'Syllisten est un prototype de logiciel éducatif développé de manière indépendante. Il n’est ni affilié, ni parrainé, ni approuvé, ni présenté comme un '
                       'produit officiel d’OpenAI, Streamlit, Apple, Microsoft, Google, d’un fournisseur de navigateur, d’un fournisseur de voix ou de tout autre tiers. '
                       'N’utilisez que des textes que vous êtes légalement autorisé à traiter. Ne soumettez pas d’informations confidentielles, réglementées, illicites, '
                       'contrefaisantes, personnelles ou sensibles, sauf si vous disposez d’une base juridique valable et comprenez pleinement les conditions et les risques '
                       'applicables. En mode fondé sur des règles, le texte est traité par des règles intégrées sur le serveur de l’application et n’est pas volontairement '
                       'transmis à OpenAI. En mode API, le texte est transmis à OpenAI au moyen de la clé API fournie par l’utilisateur et relève du compte associé ainsi que des '
                       'conditions applicables d’OpenAI. La voix est générée principalement au moyen du paquet tiers edge-tts, client non officiel du service de synthèse vocale en ligne de Microsoft Edge. Les phrases destinées à la lecture peuvent donc être transmises à une infrastructure vocale en ligne exploitée par Microsoft. La Web Speech API du navigateur n’est utilisée qu’en solution de secours ; le lieu de traitement dépend du navigateur, du système d’exploitation et de la voix sélectionnée. L’application ne garantit ni l’exactitude de la '
                       'détection de langue, de la segmentation, de la prononciation ou de la notation, ni la disponibilité, la continuité, la sécurité, la confidentialité, '
                       'l’adéquation à un usage particulier ou l’absence d’erreurs. Les résultats et les scores constituent uniquement des aides pédagogiques et ne doivent pas '
                       'servir à des décisions juridiques, médicales, financières, de certification académique, d’immigration, d’emploi ou à toute autre décision à risque élevé. '
                       'L’utilisateur est responsable des frais d’API, de la vérification des droits relatifs au contenu, de la configuration de son appareil et de son '
                       'navigateur, ainsi que du respect des lois, licences et conditions de tiers applicables. La clé API est conçue pour ne rester disponible que pendant la '
                       'session en cours ; toutefois, aucun service connecté à Internet ne peut garantir une sécurité absolue. Utilisez une clé de projet restreinte, définissez '
                       'des plafonds de dépense et révoquez-la après utilisation lorsque cela est approprié. Le logiciel est fourni « en l’état », sans garantie expresse ou '
                       'implicite, dans toute la mesure permise par la loi.',
        'must_accept': 'Vous devez accepter l’avis pour continuer.',
        'footer': 'Prototype éducatif indépendant. N’utilisez que du contenu que vous êtes autorisé à traiter.',
        'key_missing': 'Saisissez une clé API OpenAI ou passez au mode fondé sur des règles.',
        'not_saved': 'L’application n’enregistre pas volontairement la clé dans le dépôt ni dans une base de données.',
        'delete_session': 'La fermeture de la session efface normalement son état ; sur un appareil partagé, sélectionnez « Effacer la clé API » avant de partir.',
        'module_openai': 'SDK Python d’OpenAI — requêtes API en mode clé utilisateur ; licence Apache-2.0.',
        'module_streamlit': 'Streamlit — interface web et gestion de session ; licence Apache-2.0.',
        'module_webspeech': 'edge-tts — client non officiel donnant accès à la synthèse vocale en ligne de Microsoft Edge ; sa disponibilité et son fonctionnement peuvent évoluer. Web Speech API n’est utilisé qu’en solution de secours. '
                            'l’utilisateur.',
        'module_python': 'Bibliothèque standard Python — traitement et comparaison de texte.',
        'source_note': 'La publication du code source n’est pas obligatoire pour limiter la responsabilité dans cette architecture ; le dépôt contient néanmoins les licences et '
                       'mentions de tiers par souci de transparence.',
        'no_key_log': 'L’application est conçue pour ne pas imprimer ni conserver volontairement la clé complète. Les journaux de la plateforme et l’infrastructure dépendent de '
                      'la configuration de l’exploitant.',
        'analysis_mode': 'Mode d’analyse',
        'supported_only': 'Seuls le chinois, le japonais, l’anglais, l’espagnol et le français sont pris en charge.',
        'unsupported_language': 'Le texte semble être rédigé dans une langue non prise en charge. Syllisten prend actuellement en charge uniquement le chinois, le japonais, '
                                'l’anglais, l’espagnol et le français.',
        'notice_language': 'Langue de l’avis',
        'supported_languages': 'Langues d’étude prises en charge',
        'supported_list': 'Chinois · Japonais · Anglais · Espagnol · Français'}}


# Labels added here keep the main translation table readable while ensuring the
# English-accent control is fully localized in every supported interface language.
_ACCENT_I18N = {
    "en": {"english_accent": "English pronunciation", "british_english": "British English", "american_english": "American English"},
    "zh": {"english_accent": "英语发音", "british_english": "英式英语", "american_english": "美式英语"},
    "ja": {"english_accent": "英語の発音", "british_english": "イギリス英語", "american_english": "アメリカ英語"},
    "es": {"english_accent": "Pronunciación del inglés", "british_english": "Inglés británico", "american_english": "Inglés estadounidense"},
    "fr": {"english_accent": "Prononciation de l’anglais", "british_english": "Anglais britannique", "american_english": "Anglais américain"},
}
for _lang, _labels in _ACCENT_I18N.items():
    I18N[_lang].update(_labels)


def tr(lang: str, key: str) -> str:
    return I18N.get(lang, I18N["en"]).get(key, I18N["en"].get(key, key))


def t(key: str) -> str:
    return tr(st.session_state.get("ui_lang", "en"), key)


def init_state() -> None:
    defaults = {"analysis":None,"answers":{},"checked":{},"show_text":{},"theme":"Ocean","source_text":"","ui_lang":"en","accepted_notice":False,"analysis_mode":"local","user_api_key":"","english_accent":"en-GB"}
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def inject_theme(name: str) -> None:
    c = THEMES[name]
    st.markdown(f"""<style>
    :root{{--bg:{c['bg']};--surface:{c['surface']};--surface2:{c['surface2']};--text:{c['text']};--muted:{c['muted']};--primary:{c['primary']};--primary2:{c['primary2']};--border:{c['border']};--mark:{c['mark']};--replace:{c['replace']};--delete:{c['delete']};}}
    .stApp{{background:var(--bg);color:var(--text)}} [data-testid='stHeader']{{background:transparent}} [data-testid='stSidebar']{{background:var(--surface);border-right:1px solid var(--border)}}
    h1,h2,h3,h4,p,label,span,div{{color:var(--text)}} .ll-hero{{padding:1.2rem 1.4rem;border:1px solid var(--border);border-radius:18px;background:linear-gradient(135deg,var(--surface),var(--surface2));margin-bottom:1rem}}
    .ll-brand{{font-size:.78rem;letter-spacing:.09em;font-weight:750;color:var(--primary)}} .ll-title{{font-size:1.85rem;font-weight:760;margin:.2rem 0 .35rem}} .ll-sub{{color:var(--muted);line-height:1.6}}
    .ll-hidden,.ll-note{{padding:.8rem 1rem;border-radius:12px;background:var(--surface2);border:1px dashed var(--border);color:var(--muted)}}
    .ll-answer{{padding:.8rem 1rem;border-radius:12px;background:var(--surface2);line-height:1.8}} .ll-answer mark{{background:var(--mark)}} .ll-answer .replace{{background:var(--replace)}} .ll-answer del{{background:var(--delete)}}
    [data-testid='stVerticalBlockBorderWrapper']{{background:var(--surface);border-color:var(--border)!important;border-radius:16px}} .stButton>button{{border-radius:11px}} .stButton>button[kind='primary']{{background:var(--primary);border-color:var(--primary);color:white}}
    .stTextArea textarea,.stTextInput input,.stSelectbox [data-baseweb='select']{{background:var(--surface)!important;color:var(--text)!important;border-color:var(--border)!important}}
    .ll-footer{{font-size:.78rem;color:var(--muted);line-height:1.5}} hr{{border-color:var(--border)!important}}
    </style>""", unsafe_allow_html=True)


def fallback_segment(text: str, language_code: str | None = None) -> list[str]:
    """Split text without losing Chinese or Japanese punctuation.

    CJK writing normally has no space after 。！？, so a whitespace-based regular
    expression cannot find those boundaries. This scanner closes a unit directly
    after CJK terminal punctuation while keeping closing quotation marks attached.
    For Latin-script languages, a full stop is treated as a boundary only when it
    is followed by whitespace or the end of the paragraph, reducing accidental
    splits inside abbreviations and decimal numbers.
    """
    cleaned = re.sub(r"[ \t]+", " ", text.strip())
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    if not cleaned:
        return []

    code = (language_code or "").lower().split("-")[0]
    cjk = code in {"zh", "ja"}
    closing_marks = set('\"\'”’」』】）)]》〉')
    terminal_cjk = set("。！？!?；;")
    terminal_latin = set(".!?;")
    units: list[str] = []

    for paragraph in re.split(r"\n+", cleaned):
        paragraph = paragraph.strip()
        if not paragraph:
            continue
        start = 0
        i = 0
        length = len(paragraph)
        while i < length:
            ch = paragraph[i]
            is_boundary = False
            if cjk and ch in terminal_cjk:
                is_boundary = True
            elif not cjk and ch in terminal_latin:
                # Exclamation and question marks are unambiguous. Periods and
                # semicolons close a unit only before whitespace or paragraph end.
                if ch in "!?":
                    is_boundary = True
                else:
                    j = i + 1
                    while j < length and paragraph[j] in closing_marks:
                        j += 1
                    is_boundary = j >= length or paragraph[j].isspace()

            if is_boundary:
                end = i + 1
                while end < length and paragraph[end] in terminal_cjk:
                    end += 1
                while end < length and paragraph[end] in closing_marks:
                    end += 1
                unit = paragraph[start:end].strip()
                if unit:
                    units.append(unit)
                start = end
                while start < length and paragraph[start].isspace():
                    start += 1
                i = start
                continue
            i += 1

        tail = paragraph[start:].strip()
        if tail:
            units.append(tail)
    return units


def heuristic_language(text: str) -> tuple[str, str, str]:
    # Reject scripts that are clearly outside the five supported languages.
    if re.search(r"[\u0400-\u052f\u0600-\u06ff\u0900-\u097f\u0e00-\u0e7f\uac00-\ud7af]", text):
        raise ValueError(t("unsupported_language"))
    if re.search(r"[\u3040-\u30ff]", text):
        code = "ja"
    elif re.search(r"[\u4e00-\u9fff]", text):
        code = "zh"
    else:
        lower = f" {text.casefold()} "
        spanish_markers = ("¿", "¡", "ñ", " el ", " la ", " los ", " las ", " que ", " una ", " para ", " por ", " con ", " del ", " como ")
        french_markers = ("ç", "œ", " le ", " la ", " les ", " des ", " une ", " est ", " avec ", " pour ", " dans ", " que ", " du ")
        spanish_score = sum(marker in lower for marker in spanish_markers) + 2 * len(re.findall(r"[áíóúñ¿¡]", lower))
        french_score = sum(marker in lower for marker in french_markers) + 2 * len(re.findall(r"[àâçèêëîïôùûüÿœ]", lower))
        if spanish_score >= 2 and spanish_score > french_score:
            code = "es"
        elif french_score >= 2 and french_score > spanish_score:
            code = "fr"
        else:
            code = "en"
    return LANGUAGE_NAMES_EN[code], code, DEFAULT_LOCALES[code]


def validate_locale(code: str, locale: str) -> str:
    code = (code or "en").lower().split("-")[0]
    if code not in SUPPORTED_CODES:
        raise ValueError(t("unsupported_language"))
    candidate = (locale or "").strip().replace("_", "-")
    return candidate if candidate.lower().startswith(code + "-") else DEFAULT_LOCALES[code]


def analyze_text(text: str, mode: str, api_key: str) -> dict[str, Any]:
    if mode == "local":
        name, code, locale = heuristic_language(text)
        return {"language_name":name,"language_code":code,"locale":locale,"sentences":fallback_segment(text, code),"used_gpt":False}
    if not api_key.strip():
        raise ValueError(t("key_missing"))
    client = OpenAI(api_key=api_key.strip())
    instructions = """Return JSON only: {\"language_name\":\"English language name\",\"language_code\":\"ISO 639-1\",\"locale\":\"BCP-47 native regional locale\",\"sentences\":[\"original sentence\"]}. Preserve all wording, spelling, punctuation and capitalization. Do not translate, correct, summarize or add content. The only supported languages are Chinese (zh), Japanese (ja), English (en), Spanish (es), and French (fr). If the input is not predominantly one of those languages, return language_code as "unsupported" and an empty sentences array. Detect the likely regional variety. Split at natural sentence boundaries; split very long sentences only at natural clause boundaries."""
    response = client.responses.create(model="gpt-5-mini", instructions=instructions, input=text, text={"format":{"type":"json_object"}})
    data = json.loads(response.output_text)
    code = str(data.get("language_code", "en")).lower().split("-")[0]
    if code not in SUPPORTED_CODES:
        raise ValueError(t("unsupported_language"))
    sentences = [str(x).strip() for x in data.get("sentences", []) if str(x).strip()] or fallback_segment(text, code)
    return {"language_name":data.get("language_name") or LANGUAGE_NAMES_EN[code],"language_code":code,"locale":validate_locale(code,str(data.get("locale",""))),"sentences":sentences,"used_gpt":True}


def normalize(text: str) -> str:
    value = unicodedata.normalize("NFKC", text).casefold().strip()
    return "".join(ch for ch in value if ch.isalnum())


def similarity(reference: str, answer: str) -> float:
    return difflib.SequenceMatcher(None, normalize(reference), normalize(answer)).ratio()


def diff_html(reference: str, answer: str) -> str:
    out=[]
    for tag,i1,i2,j1,j2 in difflib.SequenceMatcher(None,answer,reference).get_opcodes():
        a=html.escape(answer[i1:i2]); r=html.escape(reference[j1:j2])
        if tag=="equal": out.append(r)
        elif tag=="insert": out.append(f"<mark>{r}</mark>")
        elif tag=="delete": out.append(f"<del>{a}</del>")
        else: out.append(f"<del>{a}</del><span class='replace'>{r}</span>")
    return "".join(out)


PREFERRED_EDGE_VOICES = {
    "zh-CN": "zh-CN-XiaoxiaoNeural",
    "ja-JP": "ja-JP-NanamiNeural",
    "en-GB": "en-GB-SoniaNeural",
    "en-US": "en-US-JennyNeural",
    "es-ES": "es-ES-ElviraNeural",
    "fr-FR": "fr-FR-DeniseNeural",
}


def _edge_rate(speed: float) -> str:
    percent = round((float(speed) - 1.0) * 100)
    return f"{percent:+d}%"


async def _edge_audio_async(text: str, locale: str, speed: float) -> bytes:
    language = locale.split("-")[0].lower()
    voice = PREFERRED_EDGE_VOICES.get(locale, PREFERRED_EDGE_VOICES.get(DEFAULT_LOCALES.get(language, "en-GB"), "en-GB-SoniaNeural"))
    communicator = edge_tts.Communicate(text=text, voice=voice, rate=_edge_rate(speed))
    chunks: list[bytes] = []
    async for chunk in communicator.stream():
        if chunk.get("type") == "audio":
            chunks.append(chunk["data"])
    if not chunks:
        raise RuntimeError("No audio was returned by the speech service.")
    return b"".join(chunks)


@st.cache_data(show_spinner=False, max_entries=256)
def edge_audio(text: str, locale: str, speed: float) -> bytes:
    return asyncio.run(_edge_audio_async(text, locale, speed))


def browser_speech_fallback(text: str, locale: str, speed: float, key: str) -> None:
    sid = re.sub(r"[^a-zA-Z0-9_-]", "", key)
    components.html(f"""<!doctype html><html><head><meta charset='utf-8'><style>body{{margin:0;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}}.bar{{display:flex;gap:8px;align-items:center;flex-wrap:wrap}}button{{border:1px solid #AAB8C5;border-radius:10px;padding:7px 13px;background:white;cursor:pointer}}.s{{font-size:12px;color:#667582;flex:1}}</style></head><body><div class='bar'><button id='p{sid}'>{html.escape(t('play'))}</button><button id='x{sid}'>{html.escape(t('stop'))}</button><span class='s' id='s{sid}'>{html.escape(t('voice_ready'))}</span></div><script>
    const text={json.dumps(text,ensure_ascii=False)}, locale={json.dumps(locale)}, rate={float(speed)}; const status=document.getElementById('s{sid}');
    function choose(){{const all=speechSynthesis.getVoices();const exact=all.filter(v=>(v.lang||'').toLowerCase()===locale.toLowerCase());if(exact.length)return exact.find(v=>v.localService)||exact[0];const p=locale.split('-')[0].toLowerCase();const same=all.filter(v=>(v.lang||'').toLowerCase().split('-')[0]===p);return same.find(v=>v.localService)||same[0]||null;}}
    document.getElementById('p{sid}').onclick=()=>{{speechSynthesis.cancel();const v=choose();if(!v){{status.textContent={json.dumps(t('voice_missing'),ensure_ascii=False)};return;}}const u=new SpeechSynthesisUtterance(text);u.lang=locale;u.voice=v;u.rate=rate;u.onstart=()=>status.textContent=v.name+' · '+v.lang;u.onend=()=>status.textContent=v.name+' · '+v.lang;speechSynthesis.speak(u);}};
    document.getElementById('x{sid}').onclick=()=>speechSynthesis.cancel(); speechSynthesis.onvoiceschanged=()=>speechSynthesis.getVoices();
    </script></body></html>""", height=45, scrolling=False)


def speech_component(text: str, locale: str, speed: float, key: str) -> None:
    try:
        audio = edge_audio(text, locale, round(float(speed), 2))
        st.audio(audio, format="audio/mpeg")
    except Exception:
        st.caption("Natural voice unavailable; using the browser voice fallback.")
        browser_speech_fallback(text, locale, speed, key)


def render_sentence(index: int, sentence: str, locale: str, speed: float) -> None:
    with st.container(border=True):
        a,b=st.columns([5,1.3],vertical_alignment="center")
        a.markdown(f"### {index+1:02d} · {t('unit')}")
        shown=b.toggle(t("show"),value=st.session_state.show_text.get(index,False),key=f"show_{index}")
        st.session_state.show_text[index]=shown
        if shown:
            st.info(sentence)
        else:
            st.markdown(f"<div class='ll-hidden'>{html.escape(t('hidden'))}</div>", unsafe_allow_html=True)
        speech_component(sentence,locale,speed,f"s{index}")
        answer=st.text_area(t("answer"),value=st.session_state.answers.get(index,""),key=f"answer_{index}",height=82,placeholder=t("answer_placeholder"))
        st.session_state.answers[index]=answer
        c,d=st.columns([1.25,4],vertical_alignment="center")
        if c.button(t("compare"),key=f"check_{index}",use_container_width=True): st.session_state.checked[index]=True
        d.caption(t("compare_note"))
        if st.session_state.checked.get(index):
            score=similarity(sentence,answer); st.progress(score,text=f"{t('score')}: {score*100:.1f}%")
            if score >= 0.98:
                st.success(t("perfect"))
            elif score >= 0.85:
                st.warning(t("close"))
            else:
                st.error(t("retry"))
            st.markdown(f"<div class='ll-answer'><strong>{html.escape(t('difference'))}</strong><br>{diff_html(sentence,answer)}</div>",unsafe_allow_html=True)
            with st.expander(t("standard")): st.write(sentence)


def show_notice() -> None:
    @st.dialog(APP_NAME, width="large")
    def notice_dialog() -> None:
        notice_lang = st.selectbox(
            "Language / 语言 / 言語 / Idioma / Langue",
            options=list(I18N.keys()),
            format_func=lambda x: I18N[x]["ui_name"],
            index=list(I18N.keys()).index(st.session_state.get("notice_lang", st.session_state.ui_lang)),
            key="notice_language_picker",
        )
        st.session_state.notice_lang = notice_lang

        # Use the selected notice language directly so every paragraph, label and
        # button changes together on the same Streamlit rerun.
        st.subheader(tr(notice_lang, "notice_title"))
        st.markdown(f"**{tr(notice_lang, 'nonprofit')}**")
        st.write(tr(notice_lang, "nonprofit_body"))
        st.divider()
        st.write(tr(notice_lang, "notice_body"))
        st.caption(f"{tr(notice_lang, 'supported_languages')}: {tr(notice_lang, 'supported_list')}")
        accepted = st.checkbox(tr(notice_lang, "ack"), key=f"notice_checkbox_{notice_lang}")
        if st.button(tr(notice_lang, "continue"), type="primary", disabled=not accepted, use_container_width=True):
            st.session_state.ui_lang = notice_lang
            st.session_state.ui_lang_picker = notice_lang
            st.session_state.accepted_notice = True
            st.rerun()
    notice_dialog()



def clear_exercise_state() -> None:
    st.session_state.analysis = None
    st.session_state.answers = {}
    st.session_state.checked = {}
    st.session_state.show_text = {}


def on_analysis_mode_change() -> None:
    # A result generated in one mode must never remain visible after switching modes.
    clear_exercise_state()


def on_ui_language_change() -> None:
    st.session_state.ui_lang = st.session_state.ui_lang_picker


def sidebar(speed_default: float=0.9) -> float:
    with st.sidebar:
        st.header(t("settings"))
        speed=st.slider(t("speed"),.5,1.5,speed_default,.05)
        st.divider()
        st.subheader(t("analysis_mode"))
        mode=st.radio(
            t("mode"),
            options=["local", "api"],
            format_func=lambda x: t("local_mode") if x == "local" else t("api_mode"),
            key="analysis_mode",
            on_change=on_analysis_mode_change,
        )
        st.caption(t("local_help") if mode=="local" else t("api_help"))
        if mode=="api":
            key=st.text_input(t("api_key"),value=st.session_state.user_api_key,type="password",placeholder=t("api_placeholder"))
            st.session_state.user_api_key=key
            st.caption(t("api_notice")); st.caption(t("not_saved"))
            if st.button(t("clear_key"),use_container_width=True):
                st.session_state.user_api_key=""; st.rerun()
        st.divider()
        with st.expander(t("menu"),expanded=False):
            st.markdown(f"**{APP_NAME}**  \\n{t('developer')}: {DEVELOPER}  \\n{t('license')}: {PROJECT_LICENSE}")
            st.markdown(f"**{t('components')}**")
            st.caption(t("module_streamlit")); st.caption(t("module_openai")); st.caption(t("module_webspeech")); st.caption(t("module_python"))
            st.markdown(f"**{t('privacy')}**")
            st.caption(t("no_key_log")); st.caption(t("delete_session"))
            st.markdown(f"**{t('legal')}**")
            st.caption(t("source_note"))
            if st.button(t("notice_title"),key="reopen_notice",use_container_width=True):
                st.session_state.accepted_notice=False; st.rerun()
    return speed


def main() -> None:
    st.set_page_config(page_title=APP_NAME,page_icon="🎧",layout="wide",initial_sidebar_state="expanded")
    init_state()
    top1,top2,top3=st.columns([5,1.25,1.45],vertical_alignment="top")
    with top2:
        if "ui_lang_picker" not in st.session_state:
            st.session_state.ui_lang_picker = st.session_state.ui_lang
        st.selectbox(
            t("ui_language"),
            options=list(I18N.keys()),
            format_func=lambda x: I18N[x]["ui_name"],
            key="ui_lang_picker",
            on_change=on_ui_language_change,
        )
    with top3:
        st.session_state.theme=st.selectbox(t("theme"),list(THEMES),index=list(THEMES).index(st.session_state.theme),key="theme_picker")
    inject_theme(st.session_state.theme)
    if not st.session_state.accepted_notice:
        show_notice()
        st.stop()
    with top1:
        st.markdown(f"<div class='ll-hero'><div class='ll-brand'>{APP_NAME.upper()}</div><div class='ll-title'>{html.escape(t('title'))}</div><div class='ll-sub'>{html.escape(t('subtitle'))}</div></div>",unsafe_allow_html=True)
    speed=sidebar()
    st.caption(f"{t('supported_languages')}: {t('supported_list')}")
    text=st.text_area(t("source_text"),value=st.session_state.source_text,height=200,placeholder=t("source_placeholder"))
    st.session_state.source_text=text
    a,b,_=st.columns([1.45,1.05,4.5])
    analyze=a.button(t("generate"),type="primary",use_container_width=True)
    if b.button(t("clear"),use_container_width=True):
        clear_exercise_state(); st.session_state.source_text=""; st.rerun()
    if analyze:
        if not text.strip(): st.warning(t("empty"))
        else:
            try:
                st.session_state.analysis=analyze_text(text,st.session_state.analysis_mode,st.session_state.user_api_key)
                st.session_state.answers={}; st.session_state.checked={}; st.session_state.show_text={}
            except Exception as exc: st.error(f"{t('analysis_error')}: {exc}")
    data=st.session_state.analysis
    if not data:
        st.markdown(f"<div class='ll-note'>{html.escape(t('start'))}</div>",unsafe_allow_html=True)
    else:
        sentences=data.get("sentences",[])
        language_code=data.get("language_code","en")
        locale=validate_locale(language_code,data.get("locale",""))
        if language_code == "en":
            accent_options = ["en-GB", "en-US"]
            current_accent = st.session_state.get("english_accent", "en-GB")
            if current_accent not in accent_options:
                current_accent = "en-GB"
            selected_accent = st.selectbox(
                t("english_accent"),
                options=accent_options,
                index=accent_options.index(current_accent),
                format_func=lambda value: t("british_english") if value == "en-GB" else t("american_english"),
                key="english_accent_selector",
            )
            st.session_state.english_accent = selected_accent
            locale = selected_accent
        x,y,z=st.columns(3); x.metric(t("language"),data.get("language_name","—")); y.metric(t("locale"),locale); z.metric(t("units"),len(sentences))
        st.caption(f"{t('method')}: {t('gpt_method') if data.get('used_gpt') else t('rule_method')}")
        st.divider()
        for i,sentence in enumerate(sentences): render_sentence(i,sentence,locale,speed)
    st.divider(); st.markdown(f"<div class='ll-footer'>{html.escape(t('footer'))}</div>",unsafe_allow_html=True)

if __name__ == "__main__":
    main()
