# codex_processor

Система для подготовки документов СтудЧР.

## Как работает

Превращает маркдаун вида

```
---
title: Регламент музыкальных стульев
---

## § Общие положения

§§ Музыкальные стулья — это кайфово.

§§ok Оргкомитет всегда прав.

§§ Когда оргкомитет неправ, см. п. <^^ok>
```

в готовый докмент вида

<img src="mus_st.jpg" width="600" />

## Установка


### miniconda

Ставим miniconda отсюда: <https://docs.conda.io/en/latest/miniconda.html>

Нужен питон 3.9. Если у вас уже есть более старая миниконда, создаёте новое окружение: `conda create -n codex python=3.9` (на самом деле сейчас можно уже и 3.11, он новее и быстрее работает).

### git и репозиторий

Заходим в <https://gitlab.com/-/profile/personal_access_tokens>, создаём себе токен, отметив галки read_repository, write_repository, сохраняем куда-нибудь (его покажут только один раз). Далее его надо будет использовать вместо пароля при клонировании репозиториев.

#### Первый этап, Windows

Заходим на <https://git-scm.com/downloads>, скачиваем и ставим гит. На все вопросы при установке оставляем дефолтный выбор.

Запускаем git bash. Пишем в командной строке `git clone https://gitlab.com/peczony/studchr_ratings_v3`. Вас редиректнет в браузер для логина в гитлаб. В итоге появится папка `studchr_ratings_v3`.

#### Первый этап, Мак

Запускаем в терминале `git`.

```
usage: git [--version] [--help] [-C <path>] [-c <name>=<value>]
           [--exec-path[=<path>]] [--html-path] [--man-path] [--info-path]
           [-p | --paginate | -P | --no-pager] [--no-replace-objects] [--bare]
           [--git-dir=<path>] [--work-tree=<path>] [--namespace=<name>]
           [--super-prefix=<path>] [--config-env=<name>=<envvar>]
           <command> [<args>]

(далее длинное описание команд)
```

Если вместо этого вы увидели в терминале одну строчку, где написано что-то типа того, что гит не установлен, запустите в терминале `xcode-select --install`. Принимаем условия, ждём, пока поставятся инструменты командной строки.

Далее пишем в командной строке `git clone https://gitlab.com/peczony/studchr_ratings_v3`. Вводим логин и пароль. В итоге появится папка `studchr_ratings_v3`.

#### Второй этап, общий для Win и мака

Скачиваем и ставим Sublime Merge: <https://www.sublimemerge.com/>

Далее в ней можно будет открыть склонированный ранее репозиторий и делать коммиты. Этот процесс можно глянуть в конце видео про шаблоны: <https://youtu.be/Y43zf-mn9sk?t=586>

## Установка codex_processor

Введите в терминале (Anaconda Prompt, если Виндоус, обычный терминал на Маке): `cd studchr_ratings_v3`, чтобы оказаться в папке с репозиторием.

После этого: `pip install -e codex_processor` и `pip install -e studchr_utility`. Пройдёт приличное количество времени (минут 20), в процессе этого будет установлен, в том числе, `pandoc` и `latex`. Если будет выдавать ошибки, напишите мне.

После этого вы можете переместиться в папку `regulations` (`cd regulations`) и попробовать собрать какой-нибудь документ, например, Положение:

- `cpr -o docx polozhenie.md` — создаст `polozhenie.docx`
- `cpr -o latex polozhenie.md` — создаст `polozhenie.pdf`
- `cpr -o latex --toc polozhenie.md` — создаст `polozhenie.pdf` с оглавлением — полезно для длинных документов