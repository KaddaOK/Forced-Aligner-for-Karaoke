# NeMo Forced Aligner (NFA) Tools for Making Karaoke

This repo has some resources to make it easy to use NeMo Forced Aligner to auto-generate karaoke timing.

NFA will generate a token timing `.ctm` file, which can be imported into the Recognize tab of [Kadda OK Tools](https://github.com/KaddaOK/KaddaOKTools), and from there can be exported to YouTube Movie Maker or Karaoke Builder Studio.

(NFA also will generate a `.ass` subtitle file, though it does not use the smooth scrolling styles that the karaoke community expects. For this reason, if `.ass` is your target, I would recommend importing the `.ctm` into KOKT, exporting from there to KBS, and and then using `kbp2ass` or something similar. This information will likely become stale quickly, though, so for the most up-to-date guidance, feel free to ask in the [diveBar discord](https://discord.gg/divebar).)

---

## Usage

There are a couple ways to make use of this stuff.

### Option 1: Google Colab

The _easiest_ way to do it is to just [click here to launch the Google Colab notebook](https://colab.research.google.com/github/KaddaOK/NFA-Notebook/blob/main/NeMo%20Forced%20Aligner%20for%20general%20karaoke%20use%20v0.01.ipynb) stored in this repo and follow the instructions in it.

NFA doesn't appear to actually require a GPU, so this workload can run on the default free resources.

It's a bit of a pain to get the audio _onto_ the running instance, but I've provided a couple ways to do that.

The only problem with doing it this way is, each time you connect to a new instance, all of the setup has to run, and that takes upwards of 5 minutes. But it works, you just have to be patient.

You can, of course, avoid that by connecting to a locally-running jupyter notebook instance, because then it shouldn't have to install that stuff more than the first time you run it.

But unless that's a thing you already have set up and are used to that workflow, you might prefer to just:

### Option 2: Set up and run locally

Also in this repo are 2 bash scripts (`setup.sh` and `nfa.sh`) and a python script (`prepare.py`), which you can rub together vigorously to make it go on your own machine.

These are written with Ubuntu-on-Windows via [WSL2](https://learn.microsoft.com/en-us/windows/wsl/about) in mind, and I'm sure would work fine directly in Linux as well.  
(I do _not_ recommend trying to do any python ML directly on a Windows machine, you're gonna have a bad time.)  
I don't know about macOS either way, sorry, ymmv. (Report back!)

You may want to keep in mind that, no matter how you do it, all the various models and packages are going to take up a non-trivial amount of space. (My WSL2 vhdx for this is currently ~55 GB.)

#### Installation:

Put the 3 files in some appropriate folder, `cd` to it and run `./setup.sh`.  
This will apt-get install a whole bunch of dependencies, and then pip install a whole bunch more dependencies, and then clone the NeMo source into a subdir.  
(As of this writing, the version is locked to `1.21` because there's a bug in `1.22`, but that will change in the future I'm sure.)

#### Execution:

```
./nfa.sh -a "/path/to/vocals/audio.flac" -l "/path/to/lyrics/text.txt"
```

This can accept wav, flac, or mp3 audio, and it'll write the results below the path of the vocal audio.

It'll also write a couple of files like `audio.flac.prepared.wav` and `audio.flac.manifest.json`, and it doesn't clean up after itself because I'm lazy (hey man, like, pull requests are open), but you can delete them.

---

## Support

I mean, not really? Come chat with us in `#code-dungeon` or `#kadda-ok` on the [diveBar discord](https://discord.gg/divebar) I guess. Or open an issue in this repo.
