def _context_instruction_question(doc):
    parts = []
    if doc.get("instruction"):
        parts.append(doc["instruction"])
    parts.append(doc["question"])
    return "\n".join(parts)


def _choice_labels(doc):
    labels = doc.get("choices", {}).get("label")
    if labels:
        return labels
    return [chr(choice_id + 97) for choice_id in doc["choices"]["id"]]


def doc_to_text_00(doc):
    doc_text = doc['instruction'] + "\n"
    doc_text += "\n【問題】\n" + doc["question"] + "\n"
    doc_text += "\n【選択肢】\n"
    for choice_label, choice_text in zip(_choice_labels(doc), doc["choices"]["text"]):
        doc_text += choice_label + ": " + choice_text + "\n"
    doc_text += "\n【答え】\n"
    return doc_text


def doc_to_target_alphabet(doc):
    return _choice_labels(doc)[int(doc["answer"])]


def doc_to_choices_alphabet(doc):
    return _choice_labels(doc)


def doc_to_text_01(doc):
    q_doc_text = _context_instruction_question(doc) + "\n"
    return f"[問題]:{q_doc_text}[選択肢]:[{', '.join(doc['choices']['text'])}]\n[答え]:"


def doc_to_target_01(doc):
    return [
        choice_text
        for choice_id, choice_text in zip(doc["choices"]["id"], doc["choices"]["text"])
        if choice_id == doc["answer"]
    ][0]


def doc_to_choices_01(doc):
    choices = doc["choices"]["text"]
    return choices


def doc_to_text_01_2(doc):
    q_doc_text = _context_instruction_question(doc) + "\n"
    choice_doc_text = []
    for choice_label, choice_text in zip(_choice_labels(doc), doc["choices"]["text"]):
        choice_doc_text.append(choice_label + ":" + choice_text)
    return f"[問題]:{q_doc_text}[選択肢]:[{', '.join(choice_doc_text)}]\n[答え]:"


def doc_to_text_02(doc):
    q_doc_text = _context_instruction_question(doc) + "\n"
    choices = ",".join(
        [
            f"{idx}.{choice}"
            for idx, choice in zip(doc["choices"]["id"], doc["choices"]["text"])
        ]
    )
    return f"質問:{q_doc_text}" f"選択肢:{choices}\n" "回答:"


def doc_to_target_02(doc):
    return [
        str(choice_id)
        for choice_id in doc["choices"]["id"]
        if choice_id == doc["answer"]
    ][0]


def doc_to_choices_02(doc):
    return [str(choice) for choice in doc["choices"]["id"]]


def doc_to_text_02_1(doc):
    q_doc_text = _context_instruction_question(doc) + "\n"
    choices = "\n".join([f"- {choice}" for choice in doc["choices"]["text"]])
    return f"質問:{q_doc_text}選択肢:\n{choices}\n回答:"


def doc_to_text_03(doc):
    q_doc_text = _context_instruction_question(doc) + "\n"
    choices = "\n".join([f"- {choice}" for choice in doc["choices"]["text"]])
    input_text = f"{q_doc_text}" + f"出力は以下から選択してください：\n{choices}"
    return f"### 入力:\n{input_text}\n\n### 応答:\n"


def doc_to_text_04(doc, SEP="<NL>"):
    q_doc_text = _context_instruction_question(doc)
    choices = SEP.join([f"- {choice}" for choice in doc["choices"]["text"]])
    input_text = f"質問：{q_doc_text}{SEP}" + f"選択肢：{SEP}{choices}"
    return f"ユーザー: {input_text}{SEP}システム: "


def doc_to_text_05(doc):
    return doc_to_text_04(doc, SEP="\n")


def doc_to_text_06(doc):
    instruction = "与えられた選択肢の中から、最適な答えを選んでください。"
    q_doc_text = _context_instruction_question(doc)
    choices = "\n".join([f"- {choice}" for choice in doc["choices"]["text"]])
    input_text = f"質問：{q_doc_text}" + f"出力は以下から選択してください：\n{choices}"
    return f"{instruction}\n\n{input_text} [/INST] "
