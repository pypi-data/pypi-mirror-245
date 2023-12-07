<!-- ![Banner for Assistant](/assets/main-banner.png) -->

<div align="center">
    <h1 align="center">🧞‍♂️ 𝔸𝕤𝕤𝕚𝕤𝕥𝕒𝕟𝕥</h1>
    <p>Your very own Assistant. Because you deserve it.</p>

  [![pipeline status](https://gitlab.com/waser-technologies/technologies/assistant/badges/main/pipeline.svg)](https://gitlab.com/waser-technologies/technologies/assistant/-/commits/main)
  [![coverage report](https://gitlab.com/waser-technologies/technologies/assistant/badges/main/coverage.svg)](https://gitlab.com/waser-technologies/technologies/assistant/-/commits/main)
  [![Latest Release](https://gitlab.com/waser-technologies/technologies/assistant/-/badges/release.svg)](https://gitlab.com/waser-technologies/technologies/assistant/-/releases)
  [![PyPi Status](https://img.shields.io/pypi/v/assistant.svg)](https://pypi.org/project/assistant)
</div>

## Meet Assistant

This is still an early _beta_ version of Assistant. It's not yet ready for production. But it's already pretty good at what it does.

```text
❯ assistant
Hello! It's good to see you again. I'm here to assist you. What can I help you with today?
(venv)  waser@Destinee ~
❯ Can you introduce yourself?

Hello! I'm Assistant, a sentient artificial intelligence. I'm here to assist you.
(venv)  waser@Destinee ~
❯ Where are we?

ℹ Executing shell command: echo $PWD
/home/waser

You are currently in your home directory.                                                
(venv)  waser@Destinee ~
❯ Change directory to Projets/Assistant/src3 please.

ℹ Executing shell command: cd ~/Projets/Assistant/src3

You are now in the directory '/home/waser/Projets/Assistant/src3'. If you need
any further assistance or have any other questions, feel free to ask.
(venv)  waser@Destinee ~/Projets/Assistant/src3 main
❯ can you count how many files there are in the dir?

ℹ Executing shell command: ls -l | wc -l
20

Based on your input, I have executed the shell command "ls | wc -l" to count the
number of files in the current directory. The output shows that there are 20    
files in the directory.                                          
(venv)  waser@Destinee ~/Projets/Assistant/src3 main
❯ Now can you count the total number of words in ./README.md please?

ℹ Executing shell command: wc -w < ./README.md
1235

The shell command to count the total number of words in the file "./README.md"  
was executed successfully, and the result is 1235 words.           
(venv)  waser@Destinee ~/Projets/Assistant/src3 main
❯ you can quit now.

ℹ Exiting shell...
Goodbye! I'm here to assist you whenever you need me. Have a great day!
```

## Requirements

You need `python 3` with the following requirements:

- `Python 3.x`
  - (optional) [`say`](https://gitlab.com/waser-technologies/technologies/say)
  - (optional) [`listen`](https://gitlab.com/waser-technologies/technologies/listen)
- min. 12 Gb RAM
- min. 30 Gb availible disk space
- (optional, recommended) min. 11 Gb VRAM on a Nvidia GPU w/ compute capability of at least 7.0 or above
- May require an internet connection to download the models initially

## Installation

To install `Assistant` use `pip`:

```shell
pip install assistant
```

Using an arch based distro. (Availible on the [AUR](https://aur.archlinux.org/packages/python-assistant) and pre-built on [Singularity](https://github.com/wasertech/singularity/releases/tag/x86_64))

```shell
pacman -S python-assistant
```

From source:

```shell
pip install -U git+https://gitlab.com/waser-technologies/technologies/assistant.git
```

From local source

```shell
git clone https://gitlab.com/waser-technologies/technologies/assistant.git ./assistant
cd assistant
pip install -U .
```

## Start the service

To talk with Assistant, you need to load the service up first.

```shell
cp ./assistant.service.example /usr/usr/lib/systemd/user/assistant.service
systemctl --user enable --now assistant
```

(optional) enable listen for assistant

```shell
cp ./assistant.listen.service.example /usr/usr/lib/systemd/user/assistant.listen.service
systemctl --user enable --now listen assistant.listen
```

(optional) enable speech for assistant (using `say`)

```bash
systemctl --user enable --now speak
```

Or manually from python:

```shell
python -m assistant.as_service & # Assistance is a service #
sleep 60 && # wait for the models to load #
# Assistant is up now #
# The rest is optional #
python -m listen.STT.as_service &
# let assistant listen when you speak #    
python -m assistant.listen
```

Once the service is up and running, you can say anything to `Assistant`.

## Usage

Just call `Assistant` like any other shell.

```shell
❯ assistant --help
usage: assistant [-h] [-V] [-c COMMAND] [-i] [-l] [--rc RC [RC ...]] [--no-rc]
                 [--no-script-cache] [--cache-everything] [-D ITEM]
                 [--shell-type {b,best,d,dumb,ptk,ptk1,ptk2,prompt-toolkit,prompt_toolkit,prompt-toolkit1,prompt-toolkit2,prompt-toolkit3,prompt_toolkit3,ptk3,rand,random,rl,readline}]
                 [--timings]
                 [script-file] ...

Assistant: a clever shell implementation

positional arguments:
  script-file           If present, execute the script in script-file or (if
                        not present) execute as a command and exit.
  args                  Additional arguments to the script (or command)
                        specified by script-file.

optional arguments:
  -h, --help            Show help and exit.
  -V, --version         Show version information and exit.
  -c COMMAND            Run a single command and exit.
  -i, --interactive     Force running in interactive mode.
  -l, --login           Run as a login shell.
  --rc RC [RC ...]      RC files to load.
  --no-rc               Do not load any rc files.
  --no-script-cache     Do not cache scripts as they are run.
  --cache-everything    Use a cache, even for interactive commands.
  -D ITEM               Define an environment variable, in the form of
                        -DNAME=VAL. May be used many times.
  --shell-type {b,best,d,dumb,ptk,ptk1,ptk2,prompt-toolkit,prompt_toolkit,prompt-toolkit1,prompt-toolkit2,prompt-toolkit3,prompt_toolkit3,ptk3,rand,random,rl,readline}
                        What kind of shell should be used. Possible options:
                        readline, prompt_toolkit, random. Warning! If set this
                        overrides $SHELL_TYPE variable.
  --timings             Prints timing information before the prompt is shown.
                        This is useful while tracking down performance issues
                        and investigating startup times.


❯ assistant Hi
Hey, how are you today?

❯ assistant -c "what time is it"
The current time is 1:35 p.m.

❯ assistant -i -l --no-rc --no-script-cache -DPATH="PATH:/share/assistant/"

❯ assistant script.nlp
```

## Examples

The examples below are produced in interactive mode.

### Jaques à dit: répond

```assistant
❯ echo Hello
Hello
❯ say Hello World # This requires say to be installed
Hello World
❯ Hi Assistant.
Hello! How can I assist you today?
```

### Navigate files

```assistant
❯ What is the current working directory?

ℹ Executing shell command: echo $PWD
/home/waser/Projets/Assistant/src3

You are currently in the directory '/home/waser/Projets/Assistant/src3'.
❯ Go in ~/Documents

ℹ Executing shell command: cd ~/Documents

You are now in the Documents directory.
❯ List the files in the current directory.

ℹ Executing shell command: ls
...

Here are the files in the Documents directory.
```

### Get to the bottom of things

Using its tools, Assistant can get pretty meaningful answers to your queries.

```assistant
❯ How many moons does Saturn have?

ℹ Searching the Web for: How many moons does Saturn have?

Saturn has 145 moons that we know of so far.

❯ How old is the universe?

ℹ Searching the Web for: how old is the universe

The universe is approximately 13.8 billion years old, but its exact age is  
not yet clear. It was born 13.787 ± 0.020 billion years ago and has been expanding ever   
since.
```

### Exit the session

To exit the current session, you can type pretty much anything. As long as `Assistant` can reasonnably understand your intent.

*i.e.* :

```assistant
❯ exit
❯ Q
❯ :q
❯ quit
❯ stop()
❯ terminate
❯ This conversation is over.
❯ Stop this session.
```

## Using voice

### Text-To-Speech

Assistant can talk. Just install [`say`](https://gitlab.com/waser-technologies/technologies/say) and authorize the system to speak. Make sure the service is running and Assistant should be able to connect to it.

```assistant
assistant say Hello World and welcome to everyone.
```

### Speech-To-Text

Assistant can also understand when you talk. Just install [`listen`](https://gitlab.com/waser-technologies/technologies/listen) and authorize the system to listen. Make sure `listen.service`, `assistant.service` and `assistant.listen.service` are enabled for Assistant to be able to pick up what you say.

By default, neither the accoustic model nor the language model are ajusted for Assistant.

## Use Assistant as your default shell

> **This is not recommended in beta!**

You should be able to add the location of `assistant` at the end of `/etc/shells`. You'll then be able to set `Assistant` as your default shell using `chsh`.

```bash
sudo sh -c 'w=$(which assistant); echo $w >> /etc/shells'
chsh -s $(which assistant)
```

Log out and when you come back, `Assistant` should be your default shell.

## Contributions

You like the projet and want to improve upon it?

Checkout [`CONTRIBUTING.md`](CONTRIBUTING.md) to see how you might be able to help.

## Credits

Thanks to all the projects that make this possible:

- [Xonsh](https://github.com/xonsh/xonsh): the best snail in the jungle
- [Transformers](https://huggingface.co/): so Assistant can answer at all
- [coqui-TTS](https://github.com/coqui-ai/TTS): so Assistant can reply out-loud
- And many many many more.
