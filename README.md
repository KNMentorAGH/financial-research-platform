# [Project Name]

Ten projekt został wygenerowany z szablonu organizacji **KNMentorAGH** - nieprzestrzeganie opisanych tu zasad spowoduje automatyczne zablokowanie procesu integracji kodu.

## 🛠️ Standardy pracy
Projekt korzysta z globalnych standardów. Zanim zaczniesz, zapoznaj się z:
- [Zasady współpracy (Contributing)](https://github.com/KNMentorAGH/.github/blob/main/.github/CONTRIBUTING.md)
- [Baza wiedzy (SOLID, VSA, Naming)](https://github.com/KNMentorAGH/.github/tree/main/compendium)

## 🚀 Szybki start
1. **Instalacja narzędzi**:
   - **Python**: Zainstaluj rozszerzenie **Ruff** w swoim IDE.
   - **C#**: Skonfiguruj edytor tak, aby respektował ustawienia z pliku `.editorconfig`.
2. **Czyszczenie szablonu**: Aby uniknąć błędów w procesach CI/CD, usuń zbędne pliki konfiguracyjne:
   - Jeśli projekt jest w **Pythonie** — usuń plik `.editorconfig`.
   - Jeśli projekt jest w **C#** — usuń plik `pyproject.toml`.
3. **Konwencja**: Stosuj **Conventional Commits** (`typ: opis`).

## Zarządzanie gałęziami
Stosujemy model Feature Branching. Nazwa każdej gałęzi musi spełniać wzorzec: `<typ>/<krótki-opis-kebab-case>`.
- **Dozwolone typy**: `feat`, `feature`, `fix`, `docs`, `refactor`, `test`, `chore`, `build`, `ci`.
- **Przykład**: `feat/add-user-repository`.

## Automatyzacja i Pull Request
Proces PR jest w pełni zautomatyzowany i wymusza następujące kroki:

1. **Auto-Format**: Po wysłaniu kodu bot automatycznie poprawi formatowanie. Jeśli bot doda commit, wykonaj `git pull` przed dalszą pracą.
2. **Quality Gates**: PR zostanie zablokowany, jeśli nie zaliczy wszystkich bram jakości: `naming`, `format`, `build` oraz `test`.
3. **Etykiety**: Wymagane jest nadanie dokładnie jednej etykiety: `major`, `minor` lub `patch`.
4. **Code Review**:
   - Wymagane zatwierdzenie przez **Code Ownera**.
   - **Stale Reviews**: Nowy commit na gałęzi automatycznie anuluje poprzednie zatwierdzenia — lider musi sprawdzić kod ponownie.
   - **Dyskusje**: Wszystkie wątki Code Review muszą zostać oznaczone jako rozwiązane (`resolved`).
5. **Merge**: Stosujemy metodę **Squash and Merge**. Twoja historia zostanie spłaszczona do jednego, czystego commita na gałęzi `main`.