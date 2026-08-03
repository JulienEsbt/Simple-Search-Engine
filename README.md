# Simple TF-IDF Search Engine

> **Status: Academic project (2022)** — a small information-retrieval exercise,
> not a maintained search product.

This project implements a basic search engine for a collection of TED talk
transcripts. It was developed by Julien Esterbet and Hugo Legeard as part of an
academic assignment.

## What it demonstrates

- loading transcript and URL pairs from CSV;
- text normalisation and tokenisation with regular expressions;
- an inverted index from terms to documents;
- term-frequency and inverse-document-frequency calculations;
- multi-keyword intersection and TF-IDF result ranking;
- a command-line search loop;
- a small Tkinter interface that opens selected result URLs.

## Repository contents

- `TP1 Final Version.py` — command-line implementation;
- `TP1 Final Version Graphic Interface.py` — Tkinter experiment;
- `DocUtilisateur.pdf` — original user documentation;
- `tp1_sujet.pdf` — assignment brief.

## Current limitations

- the TED transcript CSV dataset is not included;
- both scripts contain absolute paths from the original development machines;
- the graphical version still depends partly on terminal input;
- indexing is rebuilt in memory at every launch;
- tokenisation is intentionally simple and does not use stemming or stop words;
- no automated tests or dependency manifest are provided.

## Reproducing the exercise

The code uses only the Python standard library. To run it, obtain a CSV file
whose first two columns contain a transcript and its URL, then replace the
hard-coded dataset path near the top of the chosen script.

```bash
python3 "TP1 Final Version.py"
```

The project is kept public for its algorithmic and educational value. It should
not be presented as a complete or current search-engine product.

## License

No open-source license has been selected. The assignment brief and external TED
dataset remain subject to their respective terms.
