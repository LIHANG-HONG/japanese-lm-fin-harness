import json

import datasets

_DESCRIPTION = (
    "A subset of digital-go-jp/lawqa_jp selection.json filtered to entries whose "
    "filename includes 金商法."
)
_CITATION = "https://github.com/digital-go-jp/lawqa_jp"
_LICENSE = "公共データ利用規約（第1.0版）"
_HOMEPAGE = "https://github.com/digital-go-jp/lawqa_jp"


class LawqaJpFin(datasets.GeneratorBasedBuilder):
    """Financial Instruments and Exchange Act subset of the lawqa_jp dataset."""

    VERSION = datasets.Version("0.0.1")
    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="lawqa_jp_fin",
            version=VERSION,
            description="The lawqa_jp financial subset dataset.",
        ),
    ]

    def _info(self):
        features = datasets.Features(
            {
                "id": datasets.Value("int32"),
                "filename": datasets.Value("string"),
                "question": datasets.Value("string"),
                "context": datasets.Value("string"),
                "instruction": datasets.Value("string"),
                "choices": {
                    "id": datasets.features.Sequence(datasets.Value("int32")),
                    "label": datasets.features.Sequence(datasets.Value("string")),
                    "text": datasets.features.Sequence(datasets.Value("string")),
                },
                "answer": datasets.Value("int32"),
                "answer_label": datasets.Value("string"),
                "references": datasets.features.Sequence(datasets.Value("string")),
            }
        )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TEST,  # type: ignore
                gen_kwargs={
                    "filepath": dl_manager.download("data.json"),
                    "split": datasets.Split.TEST,
                },
            )
        ]

    def _generate_examples(self, filepath, split):
        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)

        for row in data["data"]:
            yield row["id"], row


if __name__ == "__main__":
    LawqaJpFin().download_and_prepare()
